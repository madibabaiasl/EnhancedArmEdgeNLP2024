from math import atan2, sqrt, pi, acos, sin, cos
from scipy.linalg import logm, expm
import numpy as np
import sys

class ourAPI:
    def __init__(self):
        # Robot parameters
        self.L1 = 0.08945
        self.L2 = 0.1
        self.Lm = 0.035
        self.L3 = 0.1
        self.L4 = 0.08605
        self.S = np.array([[0, 0, 1, 0, 0, 0],
                            [0, 1, 0, -0.08945, 0, 0],
                            [0, 1, 0, -0.18945, 0, 0.035],
                            [0, 1, 0, -0.18945, 0, 0.135]]) # Screw axes
        self.M = np.array([[1, 0, 0, 0.22105],
                            [0, 1, 0, 0],
                            [0, 0, 1, 0.18945],
                            [0, 0, 0, 1]]) # End-effector M matrix

    def geom_IK(self, Td):
        """
        Gets joint angles using geometric method.
        """ 
        # Get the end-effector coordinates
        Xt = Td[0,3]; Yt = Td[1,3]; Zt = Td[2,3]

        # Get the end-effector approach vector
        ax = Td[0,0]; ay = Td[1,0]; az = Td[2,0]

        # Get the wrist vector
        wx = Xt - self.L4 * ax
        wy = Yt - self.L4 * ay
        wz = Zt - self.L4 * az
        
        # Calculate some intermediate variables
        r = sqrt(wx**2 + wy**2); h = wz - self.L1
        c = sqrt(r**2 + h**2); beta = atan2(self.Lm, self.L2)
        epsi = (pi/2) - beta; Lr = sqrt(self.Lm**2+self.L2**2)
        phi = acos((c**2-self.L3**2-Lr**2)/(-2*Lr*self.L3))
        gamma = atan2(h,r)
        alpha = acos((self.L3**2-Lr**2-c**2)/(-2*Lr*c))
        theta_a = atan2(sqrt(ax**2+ay**2),az)

        # Get corresponding joint angles using geometry (elbow-up solution)
        q1 = atan2(Yt, Xt) # Waist angle
        q2 = pi/2 - beta - alpha - gamma # Shoulder angle
        q3 = pi - epsi - phi # Elbow angle
        q4 = theta_a - q2 - q3 - pi/2 # Wrist angle

        # Return angles
        return [q1, q2, q3, q4]
    
    def num_IK(self, Tsd, InitGuess):
        """
        Gets joint angles using numerical method.
        """
        for i in range(1000):
            # Get end-effector transform (Tsb)
            Tsb = self.screw_axis_to_transformation_matrix(self.S[0,:], InitGuess[0]) @ \
            self.screw_axis_to_transformation_matrix(self.S[1,:], InitGuess[1]) @ \
            self.screw_axis_to_transformation_matrix(self.S[2,:], InitGuess[2]) @ \
            self.screw_axis_to_transformation_matrix(self.S[3,:], InitGuess[3]) @ self.M

            # Compute the body twist
            skew_sym_Vb = logm(np.linalg.inv(Tsb)@Tsd); Vb = self.twist_vector_from_skew_symmetric_matrix(skew_sym_Vb)

            # Compute new angles
            NewGuess = InitGuess + np.linalg.pinv(self.body_jacobian(InitGuess))@Vb
            print(f"Iteration number: {i} \n")

            # Check if we're done and update initial guess
            if(np.linalg.norm(abs(NewGuess-InitGuess)) <= 0.001):
                return [NewGuess[0], NewGuess[1], NewGuess[2], NewGuess[3]]
            else:
                InitGuess = NewGuess
        print('Numerical solution failed!!')
        sys.exit()

    def body_jacobian(self, angles):
        # Calculate the body jacobian
        J = np.array([[-sin(angles[1]+angles[2]+angles[3]), 0.0, 0.0, 0.0],
                        [0.0, 1.0, 1.0, 1.0],
                        [cos(angles[1]+angles[2]+angles[3]), 0.0, 0.0, 0.0],
                        [0.0, self.L3*cos(angles[2])*sin(angles[2]+angles[3])+self.L4*cos(angles[2]+angles[3])*sin(angles[2]+angles[3]), self.L3*sin(angles[3])+self.L4*sin(angles[3])*cos(angles[3]), 0.0],
                        [self.Lm*cos(angles[1])+self.L2*sin(angles[1]), 0.0, 0.0, 0.0],
                        [0.0, -self.L3*cos(angles[2])*cos(angles[2]+angles[3])-self.L4*cos(angles[2]+angles[3])**2, -self.L3*cos(angles[3])-self.L4*cos(angles[3])**2, -self.L4]])
        return J
    
    def twist_vector_from_skew_symmetric_matrix(self, skew_symmetric_matrix):
        """
        Compute the original 6D twist vector from a 4x4 skew-symmetric matrix.

        Parameters:
        - skew_symmetric_matrix: A 4x4 skew-symmetric matrix representing a screw
                                motion in homogeneous coordinates.

        Returns:
        - twist_vector: The 6D twist vector [w, v] corresponding to the input
                        skew-symmetric matrix.
        """
        assert skew_symmetric_matrix.shape == (4, 4), "Input matrix must be 4x4"

        w = np.array([skew_symmetric_matrix[2, 1], skew_symmetric_matrix[0, 2], skew_symmetric_matrix[1, 0]])
        v = skew_symmetric_matrix[:3, 3]

        return np.concatenate((w, v))
    
    def screw_axis_to_transformation_matrix(self, screw_axis, angle):
        """
        Convert a screw axis and angle to a homogeneous transformation matrix.

        Parameters:
        - screw_axis: A 6D screw axis [w, v], where w is the rotational component
                    (3D angular velocity vector) and v is the translational
                    component (3D linear velocity vector).
        - angle: The angle of rotation in radians.

        Returns:
        - transformation_matrix: The 4x4 homogeneous transformation matrix
                                corresponding to the input screw axis and angle.
        """
        assert len(screw_axis) == 6, "Input screw axis must have six components"

        # Extract rotational and translational components from the screw axis
        w = screw_axis[:3]
        v = screw_axis[3:]

        # Skew-symmetric matrix of the screw axis
        skew_matrix = np.zeros((4, 4))
        skew_matrix[:3, :3] = np.array([[0, -w[2], w[1]],
                                        [w[2], 0, -w[0]],
                                        [-w[1], w[0], 0]])
        skew_matrix[:3, 3] = v

        # Exponential map to get the transformation matrix
        exponential_map = expm(angle * skew_matrix)
        
        return exponential_map