from math import floor
import time 
from queue import Queue
import threading

class Config():
    def __init__(self, default_EAR, config_time):
        self.MEDIAN = default_EAR
        self.EAR_LOG = []
        self.last_time = 0
        self.LOG_FILLED_SIZE = 1000
        self.time_increment = config_time/self.LOG_FILLED_SIZE
        self.CONFIG_FINNISHED = False
        self.q_messured = Queue()

        t_config = threading.Thread(target=self.config)
        t_config.deamon = True
        t_config.start()

    def config(self):
        while len(self.EAR_LOG) < self.LOG_FILLED_SIZE:
            EAR_data = self.q_messured.get()
            self.EAR_LOG.append(EAR_data)
        self.set_median_log()
        self.CONFIG_FINNISHED = True

    def set_median_log(self):
        self.EAR_LOG.sort()
        self.MEDIAN = self.EAR_LOG[floor(self.LOG_FILLED_SIZE/2)]
  
    def get_config_parameter(self, DAMPED_EAR):
        if self.CONFIG_FINNISHED == False:
            self.messurement_to_config(DAMPED_EAR)
        return self.MEDIAN
    #return self.MEDIAN
  
    def messurement_to_config(self, DAMPED_EAR):
        real_time = time.time() ##MÅ ENDRES TIL NOE SOM ER STØTTET AV MAC
        if real_time - self.last_time > self.time_increment:
            self.q_messured.put(DAMPED_EAR)
            self.last_time = real_time
