from Costant import *


class Times:
    def __init__(self):
        self.current = 0
        self.next = 0  # Tempo del prossimo evento
        self.last = [0 for _ in range(QUEUES_NUM)]  # L'ultimo evento di arrivo per ogni classe di utenza


class EventList:
    def __init__(self):
        self.arrivals = []  # Lista degli eventi di arrivo, uno per ogni classe di utenza
        self.completed = [Event('C') for _ in range(SERVER_NUM)]  # Lista degli eventi di completamento
        self.sampling = 0  # Evento di campionamento


class Event:
    def __init__(self, event_type=None):
        self.event_time = None          # Tempo in cui l'evento si verificherà
        self.event_type = event_type    # Arrivo o Completamento (A o C)
        self.op_index = None            # Tipo di operazione
        self.serving_time = None        # Tempo di servizio


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
