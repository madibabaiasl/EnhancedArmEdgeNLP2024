from openai import OpenAI
from dotenv import load_dotenv
import json
import os
import gptResponseServer

def parseJsonToDict(jsonString):
    if (jsonString == None):
        return None
    try:
        dictionary = json.loads(jsonString)
        return dictionary
    except json.JSONDecodeError as e:
        print(f"cannot decode JSON-like string:\n {e}")
        print(f"ChatGPT got: {jsonString}")
        return None

if __name__ == "__main__":
    jsonLikeString = gptResponseServer.parsedGPT()
    myDict = parseJsonToDict(jsonLikeString)
    print("This is full dict:")
    print(myDict)

    if (len(myDict) == 1):
        print("found one")
        print(myDict[0])
    else:
        print("found more than one")
        for usingDict in myDict:
            print(usingDict)
