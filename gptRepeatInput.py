import gptParse
import gptResponseServer
from actionsCodeFolder import visionBASE, directionBASE

# SET UP DEFAULT BOT
import numpy as np
from interbotix_xs_modules.xs_robot.arm import InterbotixManipulatorXS

joint_positions = [0, 0, 0, 0]

bot = InterbotixManipulatorXS(
    robot_model='px100',
    group_name='arm',
    gripper_name='gripper'
)
bot.arm.go_to_home_pose()
bot.gripper.release()

bot.shutdown()

pickUpActions = ['pick up', 'retrieve']
moveActions = ['move', 'go', 'turn']

gptAnswer = gptResponseServer.parsedGPT()
allDicts = gptParse.parseJsonToDict(gptAnswer)

while (allDicts != None):
    for dicts in allDicts:
        print(dicts)

    for tempDict in allDicts:
        print(type(tempDict))
        print(tempDict['action'])
        if tempDict['action'] in pickUpActions:
            visionBASE.visionPickUpColor(tempDict['color'])
        elif tempDict['action'] in moveActions:
            # temp for demo, easily develped to be universal direction after
            if tempDict['direction'] == "left":
                directionBASE.moveDirection(tempDict['direction'])
            elif tempDict['direction'] == "right":
                directionBASE.moveDirection(tempDict['direction'])

    print("READY FOR NEW INPUT")
    gptAnswer = gptResponseServer.parsedGPT()
    allDicts = gptParse.parseJsonToDict(gptAnswer)

print("WE SUCCESSFULLY QUIT")
bot = InterbotixManipulatorXS(
    robot_model='px100',
    group_name='arm',
    gripper_name='gripper'
)
bot.arm.go_to_sleep_pose()
bot.shutdown()
print("BOT SHUTDOWN")