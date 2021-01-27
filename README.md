# EiT
Drowsiness Detection

# Installation
## Mac
This might work on windows and linux too, but no guarantees.

Command: `pip install -r requirements-mac.txt`

Command: `pip3 install -r requirements-mac.txt`

# Run
Be in the EiT folder

Command: `python src --shape-predictor src/datasets/shape_predictor_68_face_landmarks.dat --alarm src/audio/alarm.wav`

Command: `python3 src --shape-predictor src/datasets/shape_predictor_68_face_landmarks.dat --alarm src/audio/alarm.wav`

# Information
The face is divided up into 68 points as seen in the picture below:
![face](https://github.com/andreasjj/EiT/blob/main/facial_landmarks_68markup.jpg?raw=true)
## MAR
The mar is calculated from points 49-60 By getting the length of A, B, and C as seen below:
![face](https://github.com/andreasjj/EiT/blob/main/MAR.jpg?raw=true)