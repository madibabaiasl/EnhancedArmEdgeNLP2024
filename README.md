# Enhanced Robot Arm at the Edge with NLP and Vision Systems

<a href="https://github.com/Paskul">Pascal Sikorski</a>, Kaleb Yu, Lucy Billadeau, Flavio Esposito, Hadi Akbarpour, <a href="https://github.com/madibabaiasl">Madi Babaiasl</a>

This repository houses the code and data for our project that integrates edge computing, Natural Language Processing (NLP), and computer vision to create an enhanced robot arm system. Our work demonstrates a new approach to assistive robotics, leveraging the power of large language models (LLMs) alongside advanced vision systems to interpret and execute complex commands conveyed through natural language. This project aims to improve the intuitiveness, responsiveness, and accessibility of robotic systems, making them more adaptable to the nuanced needs of users, especially those with disabilities.

## Dependencies 

Our implementation was developed and tested on Ubuntu 22.04.4/Python 3.10.12.

Libraries and their resepctive dependencies build from:

Vision and Robotic Control:
scipy (1.8.0)
numpy (1.25.2)
as well as latest updated Interbotix ROS Toolbox -- (FILL IN)

OpenAI Implementation:
openai (1.12.0)
json (2.0.9)

Offline Speech Recogniton:
vosk (0.3.45)
pyaudio (0.2.11)

(Optional) Online Speech Recogntion:
speech_recognition (3.10.1)
pyttsx3 (2.90)

## Usage

To use the system, follow these steps:

- Robotic Setup and Configuration: Ensure the robotic arm and vision system are correctly set up and connected to your computing environment. Adjust the system configuration files to match your setup, including ROS (Robot Operating System) commands and vision system parameters. A complete guide can be found here: https://github.com/madibabaiasl/modern-robotics-course/wiki
- Audio Speech-to-Text Configuration: We will provide instruction assuming implementation of the offline speech-to-text model, VOSK. After installing the required packages listed above, navigate to the <a href="https://alphacephei.com/vosk/models">VOSK model webpage</a> and download a model best suited for your system. Our implementation utilized vosk-model-en-us-0.22, finding high performance and efficiency in testing. After installation, navigate to our repo file "gptSpeech.py", and configure the path location to the now downloaded location of the VOSK model.
- OpenAI API Key Configuration: Again, after installing the required packages listed, navigate to <a href="https://alphacephei.com/vosk/models">OpenAI API webpage</a>. If prompted to log in or create an account for the service, do so. Afterward, follow the prompts to generate an agent key, and save this key as we will need it for API use within our program. If you have not already, create a ".env" file. Add the line "OPENAI_API_KEY = < YOUR KEY HERE >" as the only related key needed for our program to follow. Replace < YOUR KEY HERE > with your key generated from the Open AI key generation step. You have now connected your personal Open AI account for use in our framework. Note, that only GPT-3.5 will be supported on the starting free plan.
- Execution: Following correct setup of the steps above, we now will be able to connect to our robot and begin use. We have split the robot into operations within two pipelines. One pipeline relies only on positional movement, while the other relies only on vision. Below are lines to execute in the Linux terminal that will connect to the robot through ROS, and allow for use of the remainder of our code.

Positional pipeline:
~~~ 
ros2 launch interbotix_xsarm_control xsarm_control.launch.py robot_model:=px100
~~~ 

Vision pipeline:
~~~
ros2 launch interbotix_xsarm_perception xsarm_perception.launch.py robot_model:=px100 use_armtag_tuner_gui:=true use_pointcloud_tuner_gui:=true 
~~~

In doing so, you should see ROS enabled, and live connection to the robot, ready for execution of our code.

Our program is developed with the intention of using one file to test and execute on the robot, increasing user-friendliness and future modularity. This file is "gptRepeatInput.py". When the robot is connected, ROS enabled, and the microphone found, we can run this file and begin execution. When running the file, you may get a string of "JackShmReadWritePtr" or "ALSA" errors. When this occurs, program operation is not hindered and can be ignored for now, these stem from microphone configuration errors within Linux.

You should now see the robot power up, and the arm move towards the home position. Here, you should see from the terminal if all modules were able to successfully compile, and if so you can begin to ask the robot a prompt and seek a response. As a baseline setup test, try asking the robot to move right. This example from the paper should have guaranteed success - with success here indicating the success of the implementation of the robot. Now try other commands and their execution.

## Example Results 

## Citation (BibTeX)




