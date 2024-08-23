# Algoritmo 1 slide 9 di Next-Event Simulation
from Costant import *
from utils import *
from libs.rngs import selectStream, plantSeeds
from libs.rvgs import Exponential

# Inizializzazione delle variabili globali
times = Times() # Tempi di sistema
event_list = EventList() # Lista degli eventi del sistema

# ------------------- Variabili per definire lo stato del sistema -----------------------
servers_state = [0 for _ in range(N)]  # Array binario: 0 = IDLE, 1 = BUSY
numero_clienti_in_sistema = [0 for _ in range(QUEUES_NUM)]  # Numero di clienti al momento nel sistema per ogni tipo
numero_clienti_in_servizio = [0 for _ in range(QUEUES_NUM)]  # Numero di clienti in servizio.
numero_clienti_serviti = [0 for _ in range(QUEUES_NUM)]  # Numero di clienti serviti per ogni tipo
queues = [[] for _ in range(QUEUES_NUM)]  #  Una lista di eventi per ogni coda
queues_state = [0 for _ in range(QUEUES_NUM)]  # Array binario: 0 = Empty, 1 = Not Empty
# ---------------------------------------------------------------------------------------

# Inizializza la simulazione
def initialize():
    plantSeeds(SEED)
    # Inizializza i tempi di arrivo per ogni tipo di evento
    event_list.arrivals = [generate_arrival_time(i) for i in range(QUEUES_NUM)]
    # TODO e il last? di times che fine fa?


def process_current_event():    
    # 1) Trova evento più imminente e rimozione dalla lista?
    event = get_next_event()
    times.next = event.event_time
    
    # 2) Aggiorna il tempo di sistema 
    times.next = event.event_time # TODO: o current?

    # 3) Aggiorna lo stato del sistema
    if event.event_type == 'A':
        process_arrival(event)

        times.last[event.client_type] = event.event_time  # TODO:aggiorniamo times.last? giusto?
        # Genera nuovo evento di arrivo
        GetArrival(event.client_type)

    else:
        process_completion(event)

# Processa l'evento di completamento e aggiorna lo stato del sistema
def process_arrival(event):
    # Se ci sono server liberi, il cliente viene servito immediatamente
    for s in servers_state:
        if s == 0: # TODO: Problema, meglio far lavorare quello fermo da più tempo (Equity), ci serve last
            # TODO completion time di ogni servente. Definition 2 pag 313 Alessia
            # Assegna il cliente al server
            s = 1  # BUSY
            # Genero il tempo di servizio
            service_time = generate_service_time(event.client_type)
            # Aggiorna il tempo di completamento del server
            event_list.completed[s].event_time = times.next + service_time
            # Aggiorna il tipo di cliente in servizio
            event_list.completed[s].client_type = event.client_type

            # Aggiorna il numero di clienti in servizio e nel sistema
            numero_clienti_in_sistema[event.client_type] += 1
            numero_clienti_in_servizio[event.client_type] += 1

            break
    # Non ci sono server liberi
    else:
        # Il cliente va in coda
        queues[event.client_type].append(event)
        # Aggiorna lo stato della coda
        queues_state[event.client_type] = 1 # (1 = Not Empty)

# Trova l'evento più imminente nella lista degli eventi (Arrivo o Completamento)
# Restituisce il tempo dell'evento e il tipo di evento
def get_next_event():
    
    event = Event()
    
    # Cerca l'evento di arrivo più imminente (Tutti i valori devono essere maggiori di current, altrimenti problema) serio
    for i in range(QUEUES_NUM):
        if event_list.arrivals[i] is not None:
            if event.event_time is None or event_list.arrivals[i] < event.event_time:
                event.event_time = event_list.arrivals[i]
                event.client_type = i
                event.event_type = 'A'
    
    # Cerca l'evento completamento più imminente (Se il valore è 0, non va considerato)
    for i in range(N):
        if event_list.completed[i].event_time != 0:
            if event.event_time is None or event_list.completed[i].event_time < event.event_time:
                event = event_list.completed[i]
                
    return event


# Aggiorna lo stato della coda
def update_queue_state():
    for i in range(QUEUES_NUM):
        if len(queues[i]) == 0:
           queues_state[i] = 0
        else:
            queues_state[i] = 1


# Dato l'indice del tipo di cliente, genera il tempo di arrivo
def generate_arrival_time(index_type):
    selectStream(index_type)
    return Exponential(1 / TASSO_ARRIVO[index_type])


# Dato l'indice del tipo di cliente, genera il tempo di servizio
def generate_service_time(index_type):
    selectStream(QUEUES_NUM + index_type)
    return Exponential(1 / TASSO_SERVIZIO[index_type])


def GetArrival(client_type):
    new_time = generate_arrival_time(client_type)
    event_list.arrivals[client_type] = times.last[client_type] + new_time
