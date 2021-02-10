from datetime import datetime
from datetime import timedelta

class blink():
    eye_closed_thresh = 0.19
    eye_open_thresh = 0.24
    blinking_history_short = []
    blinking_history_long = []
    eyes_open = True
    blinks = 0
    blink_length = 0
    last_blink_length = 0
    average_blink_length = 0

    def __init__(self):
        super(blink, self).__init__()

    def get_updated_history(self, blinking_history, delta):
        if len(blinking_history) > 0 and blinking_history[0] < datetime.now() - timedelta(minutes=delta):
            return blinking_history[1:]
        else:
            return blinking_history

    def update_history(self):
        self.blinking_history_short = self.get_updated_history(self.blinking_history_short, 5)
        self.blinking_history_long = self.get_updated_history(self.blinking_history_long, 30)

    def detect(self, ear):
        self.update_history()
        if (not self.eyes_open) and ear > self.eye_open_thresh:
            self.blinks += 1
            self.blinking_history_short.append(datetime.now())
            self.blinking_history_long.append(datetime.now())
            self.eyes_open = True
            self.average_blink_length = self.blink_length if self.blinks == 1 else (self.average_blink_length * (self.blinks-1) / self.blinks + self.blink_length / self.blinks)
            print("blinks: {}".format(self.blinks))
            print("blink length: {}".format(self.blink_length))
            print("average blink length: {}".format(self.average_blink_length))
            print("short term frequency: {}".format(len(self.blinking_history_short)))
            print("long term frequency: {}".format(len(self.blinking_history_long)))
            self.blink_length = 0
        elif ear < self.eye_closed_thresh:
            self.blink_length += 1
            self.eyes_open = False


