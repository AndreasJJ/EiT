import playsound

def sound_alarm(path):
	# play an alarm sound
	path = path.replace(" ", "%20")
	playsound.playsound(path)