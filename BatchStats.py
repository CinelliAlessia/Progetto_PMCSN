from Class_definition import *


class Batch_Stats:

    def __init__(self):
        self.num_batch = 0
        self.last_batch_time = 0
        self.client_served = [0 for _ in range(QUEUES_NUM)]


    def reset_state(self, times):
        # Reset delle variabili di stato per la simulazione a tempo infinito
        self.num_batch += 1
        self.last_batch_time = times
        self.client_served = [0 for _ in range(QUEUES_NUM)]
