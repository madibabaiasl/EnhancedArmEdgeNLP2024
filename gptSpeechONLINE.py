# THIS IS OLD ONLINE BASED SPEECH TO TEXT
# USE VOSK BASED MODEL, USE gptSpeech.py

import speech_recognition as sr
import pyttsx3 
import numpy as np

def ONLINE():
    r = sr.Recognizer()  

    while(1):    
        try:
            with sr.Microphone() as source2:
                
                # adjust to surrounding noise level 
                r.adjust_for_ambient_noise(source2, duration=0.2)
                
                audio2 = r.listen(source2)
                
                # use google api for translation
                MyText = r.recognize_google(audio2)
                MyText = MyText.lower()
            
                return MyText
                
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            
        except sr.UnknownValueError:
            print("unknown error occurred")

if __name__ == '__main__':
    print(ONLINE())