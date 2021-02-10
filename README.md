# EiT
Drowsiness Detection

# Installation
## Mac
This might work on windows and linux too, but no guarantees.

Command: `pip install -r requirements-mac.txt`

Command: `pip3 install -r requirements-mac.txt`

# Run
Be in the EiT folder

Command: `python src/__main__.py --shape-predictor src/datasets/shape_predictor_68_face_landmarks.dat -a src/audio/alarm.wav -n src/audio/notification.wav`

Command: `python3 src/__main__.py --shape-predictor src/datasets/shape_predictor_68_face_landmarks.dat -a src/audio/alarm.wav -n src/audio/notification.wav`
