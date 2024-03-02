# Copyright 2022 Trossen Robotics
import numpy as np
from interbotix_xs_modules.xs_robot.arm import InterbotixManipulatorXS

def moveDirection(direction):
    joint_positions = [0, 0, 0, 0]

    bot = InterbotixManipulatorXS(
        robot_model='px100',
        group_name='arm',
        gripper_name='gripper'
    )

    bot.arm.go_to_home_pose()
    #bot.arm.set_joint_positions(joint_positions)

    if (direction == "right"):
        bot.arm.set_single_joint_position(joint_name='waist', position=-np.pi/2.0)

    if (direction == "left"):
        bot.arm.set_single_joint_position(joint_name='waist', position=np.pi/2.0)

    #bot.arm.go_to_sleep_pose()
    #bot.arm.go_to_home_pose()

    #bot.arm.go_to_sleep_pose()
    bot.shutdown()
    #print(using)

if __name__ == '__main__':  
    moveDirection("left")