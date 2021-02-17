from datetime import datetime
from datetime import timedelta
from dataclasses import dataclass


@dataclass
class blink_instance:
    timestamp: datetime
    duration: int

    def get_duration(self) -> int:
        return self.duration

    def get_timestamp(self) -> datetime:
        return self.timestamp

class blink():
    eye_closed_thresh = 0.19
    eye_open_thresh = 0.24
    blinking_history = []
    current_blink = None
    just_blinked = False

    def __init__(self):
        super(blink, self).__init__()

    def update_information(self, ear):
        self.blinking_history = list(filter(lambda x: x.get_timestamp() > datetime.now() - timedelta(minutes=30), self.blinking_history))
        if self.current_blink == None and ear < self.eye_closed_thresh:
            self.current_blink = blink_instance(datetime.now(), 1)
        elif self.current_blink != None and ear < self.eye_open_thresh:
            new_blink_length = self.current_blink.get_duration() + 1 
            setattr(self.current_blink, 'duration', new_blink_length)
        elif self.current_blink != None and ear > self.eye_open_thresh: 
            self.blinking_history.append(self.current_blink)
            # print(self.current_blink.get_duration())
            # short_term_blinking_history = list(filter(lambda x: x.get_timestamp() > datetime.now() - timedelta(seconds=15), self.blinking_history))
            # long_term_average_blink_duration = sum(list(map(lambda x: x.duration, self.blinking_history))) / len(self.blinking_history)
            # short_term_average_blink_duration = sum(list(map(lambda x: x.duration, short_term_blinking_history))) / len(short_term_blinking_history)
            # print("short number: {}".format(len(short_term_blinking_history)))
            # print("long number: {}".format(len(self.blinking_history)))
            # print("short average: {}".format(short_term_average_blink_duration))
            # print("long average: {}".format(long_term_average_blink_duration))
            self.current_blink = None
            self.just_blinked = True

    def get_blink_score(self, ear):
        self.update_information(ear)
        short_term_blinking_history = list(filter(lambda x: x.get_timestamp() > datetime.now() - timedelta(minutes=5), self.blinking_history))
        if len(self.blinking_history) == 0: return 0
        short_term_average_blink_duration = sum(list(map(lambda x: x.duration, short_term_blinking_history))) / len(short_term_blinking_history)
        long_term_average_blink_duration = sum(list(map(lambda x: x.duration, self.blinking_history))) / len(self.blinking_history)
        short_term_duration = (datetime.now() - short_term_blinking_history[0].get_timestamp()).total_seconds() * 1/60
        long_term_duration = (datetime.now() - self.blinking_history[0].get_timestamp()).total_seconds() * 1/60
        short_term_frequency = len(short_term_blinking_history) / short_term_duration
        long_term_frequency = len(self.blinking_history) / long_term_duration
        if self.just_blinked:
            print("SHORT TERM")
            print("Duration: {:.2f} seconds pr blink".format(short_term_average_blink_duration))
            print("Frequncy: {:.2f}\n blink pr minute".format(short_term_frequency))
            print("LONG TERM")
            print("Duration: {:.2f} seconds pr blink".format(long_term_average_blink_duration))
            print("Frequncy: {:.2f} blink pr minute".format(long_term_frequency))
            print("----------------------------------")
            self.just_blinked = False


