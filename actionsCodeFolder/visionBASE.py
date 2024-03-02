from interbotix_perception_modules.armtag import InterbotixArmTagInterface
from interbotix_perception_modules.pointcloud import InterbotixPointCloudInterface
from interbotix_xs_modules.xs_robot.arm import InterbotixManipulatorXS
#if getting errors of missing IK, try changing relative path
#this means commenting line below, uncommenting 2 lines down
from .IK import ourAPI
#from IK import ourAPI
import numpy as np
from math import atan2, sin, cos, pi
import time

"""
This script uses a color/depth camera to get the arm to find objects and pick them up. The IK custom
API developed in the IK lesson lab will be used here to convert the cube coordinates to a desired 
end-effector transformation. Following that we would use Interbotix APIs for position manipulation and
gripping. You will pick a cube from an arbitrary location then throw it in a basket. For this
demo, the arm is placed to the left of the camera facing outward. When the end-effector is located
at x=0, y=-0.3, z=0.2 w.r.t. the 'px100/base_link' frame, the AR tag should be clearly visible to
the camera. A small basket should also be placed in front of the arm. The camera should see both the cube
and the Apriltag clearly. 

Possible challenges:
- when the light changes the color of the cubes change. they seem a different shade from the 
camera's point of view so the code cannot find the cluster. make sure to adjust the color.
- the april tag and the cube should be completely visible to the camera
- in the debug mode, see the variables and see how many clusters the camera finds and make sure that
the measurements are correct and you are picking the right cluster
- when the numerical solution fails it means that the pose is unreachable by the robot
- when ik does not fail but the robot does not do anything it means that the clusters
are not found

debug and run after line 65 --> this way you can see clusters variable
in the workspace on the left hand side
from here you can read the characteristics of clusters 

put breakpoints on line 88 and see that the position of the clusers are correct
"""

# Start by defining some constants such as robot model, visual perception frames, basket transform, etc.
ROBOT_MODEL = 'px100'
ROBOT_NAME = ROBOT_MODEL
REF_FRAME = 'camera_color_optical_frame'
ARM_TAG_FRAME = f'{ROBOT_NAME}/ar_tag_link'
ARM_BASE_FRAME = f'{ROBOT_NAME}/base_link'

colorDict = {"red": [(120, 60, 70), (160, 100, 110)],
            "blue": [(40, 65, 105), (70, 100, 130)],
            "green": [(50, 90, 90), (80, 110, 120)]}

def visionPickUpColor(color):
    # Initialize the arm module along with the pointcloud, armtag modules and IK custom API
    bot = InterbotixManipulatorXS(
        robot_model=ROBOT_MODEL,
        robot_name=ROBOT_NAME,
        group_name='arm',
        gripper_name='gripper'
    )
    pcl = InterbotixPointCloudInterface(node_inf=bot.core)
    armtag = InterbotixArmTagInterface(
        ref_frame=REF_FRAME,
        arm_tag_frame=ARM_TAG_FRAME,
        arm_base_frame=ARM_BASE_FRAME,
        node_inf=bot.core
    )
    my_api = ourAPI()

    # set initial arm and gripper pose
    #bot.arm.go_to_home_pose()
    bot.arm.go_to_sleep_pose()
    bot.gripper.release()

    # get the ArmTag pose
    armtag.find_ref_to_arm_base_transform() # Comment this line if you have already used the arm tag tuner GUI to compute the transformations
    #bot.arm.set_ee_pose_components(x=0.3, z=0.2)
    

    # get the cluster positions
    # sort them from max to min 'x' position w.r.t. the ARM_BASE_FRAME
    success, clusters = pcl.get_cluster_positions(
        ref_frame=ARM_BASE_FRAME,
        sort_axis='x',
        reverse=True
    )

    # Create a blue color bound
    #lower_red = (140, 70, 80)
    #upper_red = (160, 90, 100)
    lower = colorDict[color][0]
    upper = colorDict[color][1]
    print('with color', color)
    print('we got lower', lower)
    print('we got upper', upper)

    if success:
        print('got here!!')
        bot.arm.go_to_home_pose()
        # pick up all the objects and drop them in a virtual basket in front of the robot
        for cluster in clusters:
            print('at cluster', cluster)
            if all(lower[i] <= cluster['color'][i] <= upper[i] for i in range(3)):
                print('doing the cluster', cluster)
                # Get the first cube location
                x, y, z = cluster['position']; z = z + 0.02 # Fingers link offset
                #assuming this probs position of the cluster
                print(x, y, z)

                # Go on top of the selected cube
                theta_base = atan2(y,x)
                new_x = x/cos(theta_base)-0.01
                Td_grasp = np.array([[1,  0,  0,  new_x],
                        [0,  1,  0,  0],
                        [0,  0,  1,  z],
                        [0,  0,  0,  1]])
                #Td_grasp = np.array([[0.0, -sin(theta), cos(theta), x],
                #                     [0.0, cos(theta), sin(theta), y],
                #                     [-1.0, 0.0, 1.0, z + 0.05],
                #                     [0.0, 0.0, 0.0, 1.0]]) # Hold on end-effector transformation
                joint_positions = my_api.num_IK(Td_grasp, np.array([0,0,0,0])) # Geometric inverse kinematics
                bot.arm.set_joint_positions(np.append(theta_base,joint_positions[1:])) # Set position 
                time.sleep(3) 
                bot.gripper.grasp()      
    else:
        print('Could not get cluster positions.')

    # Go to sleep
    bot.arm.go_to_home_pose()
    time.sleep(3) 
    bot.gripper.release()
    bot.arm.go_to_sleep_pose()
    bot.shutdown()

if __name__ == '__main__':
    visionPickUpColor('red')