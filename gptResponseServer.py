from openai import OpenAI
from dotenv import load_dotenv
import os
import gptSpeech

load_dotenv()
client = OpenAI()

instructions = str()
instructions = """
Objective: Parse spoken commands related to moving an arm or interacting with objects into structured JSON data. The data should include actions, directions, distances, objects, and colors as applicable.

Instructions:

Identify the Action: Determine the main verb in the command, which indicates the action to be taken. Common actions include "move," "grab," "place," etc. Convert these verbs into their standardized form (e.g., "grab" to "retrieve").

Extract Direction (if applicable): If the command involves movement, identify the direction. Standard directions include "up," "down," "left," "right," "forward," "backward."

Determine Distance (if applicable): For movement commands, extract the distance specified, including the units (e.g., cm, inches).

Identify Objects and Colors (if applicable): When the command involves interacting with an object, identify the object and its color.

Return Structured JSON: Based on the identified components, return the information in a JSON structure. Use a consistent schema for all commands. For actions involving movement, include "action," "direction," and "distance." For actions involving object interaction, include "action," "object," and "color."

Example Outputs:

For the command "Move the arm up 5cm," return:

json Copy code { "action": "move", "direction": "up", "distance": "5 cm" } 

For the command "Grab the red square," return:

json Copy code { "action": "retrieve", "object": "square", "color": "red" } 

For the command "Pick up the red cube, then drop it on the right," return:

json Copy code { "action": "retrieve", "object": "cube", "color": "red" }, { "action": "drop", "object": "cube", "color": "red", "location": "right"}

It is very important that when a sequence of multiple outputs are returned, there is a comma inbetween responses, formatted above such as {...}, {...}

Additional Notes:

Ensure all distances include a space between the number and the unit. Convert all actions into a base or infinitive form for consistency. If an element (direction, distance, object, color) is not mentioned in the command, omit it from the JSON output. Prioritize clarity and specificity in parsing commands. When in doubt, request clarification from the user with response "Please try again". Do not add any new lines to the output.
"""

def parsedGPT():
    userInput = gptSpeech.speechToText()
    if (userInput == None):
        return None

    completion = client.chat.completions.create(
        #model="gpt-3.5-turbo",
        model="gpt-4",
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": "Here is the input: " + userInput}
        ]   
    )
    serverMessage = completion.choices[0].message.content
    formattedServerMessage = f"[{serverMessage}]"

    return formattedServerMessage


if __name__ == "__main__":

    serverRecieved = parsedGPT()
    print(serverRecieved)
    print(type(serverRecieved))