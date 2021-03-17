from datetime import datetime
from datetime import timedelta
from dataclasses import dataclass
import os
import numpy as np
from scipy.stats import norm, ttest_ind


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
    can_register_new_blink = True
    configured = False
    periods = None
    durations = None

    def __init__(self):
        super(blink, self).__init__()

    # UPDATE BLINKING HISTORY WITH NEW INFORMATION
    def update_information(self, ear, damped_ear, first, name):
        close_thresh = 0.05
        open_thresh = 0.02
        new_blink_thresh = 0
        if name != "NN": 
            self.write_to_file("blinking", ear, first, name)
            self.write_to_file("damped_ear", damped_ear, first, name)
            self.write_to_file("thresh", damped_ear - close_thresh, first, name)
        self.blinking_history = list(filter(lambda x: x.get_timestamp() > datetime.now() - timedelta(minutes=30), self.blinking_history))
        if self.current_blink == None and damped_ear - ear > close_thresh and self.can_register_new_blink:
            if name != "NN": self.write_to_file("is_blinking", 0.05, first, name)
            self.current_blink = blink_instance(datetime.now(), 1)
            self.can_register_new_blink = False
        elif self.current_blink != None and damped_ear - ear > open_thresh:
            if name != "NN": self.write_to_file("is_blinking", 0.05, first, name)
            new_blink_length = self.current_blink.get_duration() + 1 
            setattr(self.current_blink, 'duration', new_blink_length)
        elif self.current_blink != None and damped_ear - ear < open_thresh: 
            if name != "NN": self.write_to_file("is_blinking", 0, first, name)
            if self.current_blink.duration < 30:
                self.blinking_history.append(self.current_blink)
            self.current_blink = None
        else:
            if name != "NN": self.write_to_file("is_blinking", 0, first, name)
        if damped_ear - ear < new_blink_thresh:
            self.can_register_new_blink = True
        self.last_ear = ear
        self.last_damped_ear = damped_ear

    # WRITE RESULTS TO FILE
    def write_to_file(self, file_name, value, first, name):
        path = "tests/{}".format(name)
        way_of_opening = "w" if first else "a"
        if not os.path.exists(path):
            os.makedirs(path)
        f = open("{}/{}.txt".format(path, file_name), way_of_opening)
        if first: f.write(name + ";")
        f.write("{:.3f}".format(value) + ";")
        f.close()

    def get_periods_and_durations(self, blinking_history):
        periods = []
        durations = []
        for i in range(len(blinking_history)):
            if i < len(blinking_history) - 1: 
                timedelta = blinking_history[i+1].get_timestamp() - blinking_history[i].get_timestamp()
                periods.append(timedelta.total_seconds())
            durations.append(blinking_history[i].get_duration())
        return periods, durations


    def configure_mean_and_sd(self):
        periods, durations = self.get_periods_and_durations(self.blinking_history)
        self.periods = periods
        self.durations = durations
        self.configured = True


    # CALCULATE THE SCORE OF TIREDNESS BASED ON BLINKING
    def get_blink_score(self, ear, damped_ear, first, name):
        self.update_information(ear, damped_ear, first, name)
        if not self.configured and len(self.blinking_history) > 1 and datetime.now() - timedelta(seconds=10) > self.blinking_history[0].get_timestamp():
            self.configure_mean_and_sd()

        if not self.configured: return 0, 0

        short_term_blinking_history = list(filter(lambda x: x.get_timestamp() > datetime.now() - timedelta(minutes=5), self.blinking_history))
        periods, durations = self.get_periods_and_durations(short_term_blinking_history)
        ttest_period = ttest_ind(self.periods, periods, equal_var=False, alternative='less')
        ttest_duration = ttest_ind(self.durations, durations, equal_var=False, alternative='greater')

        return float(ttest_period.pvalue), float(ttest_duration.pvalue)


    def reset_current_blink(self):
        self.current_blink = None


