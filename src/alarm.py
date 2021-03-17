import playsound

def sound_warnings(path):
	# play an alarm sound
	path = path.replace(" ", "%20")
	playsound.playsound(path)

def sound_notification(path):
	# play an alarm sound
	path = path.replace(" ", "%20")
	playsound.playsound(path)
