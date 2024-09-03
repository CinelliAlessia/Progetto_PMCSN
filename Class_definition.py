from Costant import *


class Times:
    def __init__(self):
        self.current = 0  # System clock - Avanzamento del tempo solo all'occorrenza di un next event
        self.next = 0  # Occurrence of the next event
        self.last = [0 for _ in range(QUEUES_NUM)]  # Last arrival time for each flow - NUMBER_OF_QUEUES elements


class EventList:
    def __init__(self):
        self.arrivals = []  # Arrival events list, each element is a type of operation
        self.completed = [Event('C') for _ in range(SERVER_NUM)]  # Completed events list
        self.sampling = 0  # Sampling event


class Event:
    def __init__(self, event_type=None):
        self.event_time = None          # Event time
        self.event_type = event_type    # Arrivo o Completamento (A o C)
        self.op_index = None            # Operation Index - Tipo di operazione - Da 0 a 7
        # self.serving_time = None        # Tempo di servizio


# Struttura dati per mantenere le aree per il calcolo delle medie
class Area:
    def __init__(self):
        self.customers = 0  # clienti nel sistema [Area unità di misura: (total customers) * time]
        self.queue = 0      # clienti in coda queues [Area unità di misura: (customers in queue) * time]
        self.service = 0    # Clienti in servizio [Area unità di misura: (customers in service) * time]


class AccumSum:
    def __init__(self):
        # accumulated sums of
        self.service = 0          #  Tempo di servizio accumulato
        self.served = 0           #  Numero clienti serviti
