from datetime import datetime
from datetime import timedelta
from dataclasses import dataclass
import os


@dataclass
class blink_instance:
    timestamp: datetime
    duration: int

    def get_duration(self) -> int:
        return self.duration

    def get_timestamp(self) -> datetime:
        return self.timestamp

class blink():
    blinking_history = []
    current_blink = None
    just_blinked = False # ONLY USED FOR PRINTING ONLY WHEN A NEW BLINKING OCCUR 

    def __init__(self):
        super(blink, self).__init__()

    # UPDATE BLINKING HISTORY WITH NEW INFORMATION
    def update_information(self, ear, ear_thresh):
        eye_open_thresh = 0.8 * ear_thresh
        eye_closed_thresh = 0.8 * ear_thresh
        self.blinking_history = list(filter(lambda x: x.get_timestamp() > datetime.now() - timedelta(minutes=30), self.blinking_history))
        if self.current_blink == None and ear < eye_closed_thresh:
            self.current_blink = blink_instance(datetime.now(), 1)
        elif self.current_blink != None and ear < eye_open_thresh:
            new_blink_length = self.current_blink.get_duration() + 1 
            setattr(self.current_blink, 'duration', new_blink_length)
        elif self.current_blink != None and ear > eye_open_thresh: 
            if self.current_blink.duration < 30:
                self.blinking_history.append(self.current_blink)
                self.just_blinked = True
            self.current_blink = None

    # WRITE RESULTS TO FILE
    def write_to_file(self, ear, first, name):
        f = open("blinking.txt", "a")
        fileIsEmpty = os.stat("blinking.txt").st_size == 0
        if first: f.write(("" if fileIsEmpty else "\n") + name + ";")
        f.write("{:.3f}".format(ear) + ";")
        f.close()

    # CALCULATE THE SCORE OF TIREDNESS BASED ON BLINKING
    def get_blink_score(self, ear, ear_thresh, first, name):
        if name != "NN": self.write_to_file(ear, first, name)
        self.update_information(ear, ear_thresh)
        short_term_blinking_history = list(filter(lambda x: x.get_timestamp() > datetime.now() - timedelta(minutes=5), self.blinking_history))
        if len(self.blinking_history) == 0 or len(short_term_blinking_history) == 0: return 0
        short_term_average_blink_duration = sum(list(map(lambda x: x.duration, short_term_blinking_history))) / len(short_term_blinking_history)
        long_term_average_blink_duration = sum(list(map(lambda x: x.duration, self.blinking_history))) / len(self.blinking_history)
        short_term_duration = (datetime.now() - short_term_blinking_history[0].get_timestamp()).total_seconds() * 1/60
        long_term_duration = (datetime.now() - self.blinking_history[0].get_timestamp()).total_seconds() * 1/60
        if short_term_duration == 0 or long_term_duration == 0: return 0
        short_term_frequency = len(short_term_blinking_history) / short_term_duration
        long_term_frequency = len(self.blinking_history) / long_term_duration

        shift_in_average_blink_duration_in_percent_of_long_term = (short_term_average_blink_duration - long_term_average_blink_duration) / long_term_average_blink_duration
        shift_in_blink_frequency_in_percent_of_long_term = (short_term_frequency - long_term_frequency) / long_term_frequency

        # ONLY FOR PRINTING, CAN BE REMOVED LATER ON
        if self.just_blinked:
            print("SHORT TERM")
            print("Duration: {:.2f} frames pr blink".format(short_term_average_blink_duration))
            print("Frequncy: {:.2f} blink pr minute".format(short_term_frequency))
            print("LONG TERM")
            print("Duration: {:.2f} frames pr blink".format(long_term_average_blink_duration))
            print("Frequncy: {:.2f} blink pr minute".format(long_term_frequency))
            print("----------------------------------")
            self.just_blinked = False
        
        shift_percentage_sum = shift_in_average_blink_duration_in_percent_of_long_term + shift_in_blink_frequency_in_percent_of_long_term

        if shift_percentage_sum < 0: return 0
        if shift_percentage_sum > 1: return 1
        return shift_percentage_sum


