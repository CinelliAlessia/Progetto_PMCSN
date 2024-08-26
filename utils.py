from Costant import *


class Times:
    def __init__(self):
        self.current = 0  # System clock - Avanzamento del tempo solo all'occorrenza di un next event
        self.next = 0  # Occurrence of the next event
        self.last = [0 for _ in range(QUEUES_NUM)]  # Last arrival time for each flow - NUMBER_OF_QUEUES elements


class EventList:
    def __init__(self):
        self.arrivals = []  # Arrival events list, each element is a type of operation
        self.completed = [Event('C') for _ in range(N)]  # Completed events list


class Event:
    def __init__(self, event_type=None):
        self.event_time = None  # Event time
        self.event_type = event_type  # Arrivo o Completamento (A o C)
        self.client_type = None  # Client type - Tipo di operazione (da 0 a CLIENT_TYPE*OPERATION_TYPE)


class ComplEvent:
    def __init__(self):
        self.event = Event('C')
        self.id_server = None  # Server ID


class Area:
    def __init__(self):
        self.customers = []  # "Area" of customers [unità di misura: (total customers) * time]
        self.queue = []  # "Area" of queues [unità di misura: (customers in queue) * time]
        self.service = []  # "Area" of service [unità di misura: (customers in service) * time]
