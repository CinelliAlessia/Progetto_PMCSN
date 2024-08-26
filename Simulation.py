# Algoritmo 1 slide 9 di Next-Event Simulation
from Update_state import update_state_compl_event, add_event_in_service
from libs.rngs import selectStream, plantSeeds
from libs.rvgs import Exponential
from utils import *

# Inizializzazione delle variabili globali
times = Times()  # Tempi di sistema
event_list = EventList()  # Lista degli eventi del sistema


# ------------------- Variabili per definire lo stato del sistema -----------------------

servers_state = [0 for _ in range(N)]  # Array binario: 0 = IDLE, 1 = BUSY
num_client_in_system = [0 for _ in range(QUEUES_NUM)]  # Numero di clienti al momento nel sistema per ogni tipo
num_client_in_service = [0 for _ in range(QUEUES_NUM)]  # Numero di clienti in servizio.
num_client_served = [0 for _ in range(QUEUES_NUM)]  # Numero di clienti serviti per ogni tipo
queues = [[] for _ in range(QUEUES_NUM)]  # Una lista di eventi per ogni coda
queues_state = [0 for _ in range(QUEUES_NUM)]  # Array binario: 0 = Empty, 1 = Not Empty

# ---------------------------------------------------------------------------------------


# Inizializza la simulazione
def initialize():
    plantSeeds(SEED)
    # Inizializza i tempi di arrivo per ogni tipo di evento
    event_list.arrivals = [generate_arrival_time(i) for i in range(QUEUES_NUM)]
    # TODO e il last? di times che fine fa?

    while times.current < TEMPO_SIMULAZIONE or num_client_in_system != 0:
        process_current_event()


# quello che andrà in loop
def process_current_event():
    # 1) Trova evento più imminente e rimozione dalla lista?
    event = get_next_event()
    times.next = event.event_time

    # 2) Processa l'evento e aggiorna lo stato del sistema
    if event.event_type == 'A':  # Se l'evento è un arrivo
        # TODO:aggiorniamo times.last? giusto?

        process_arrival(event)
        times.last[event.client_type] = event.event_time  # times.last -> l'ultimo evento processato
        get_arrival(event.client_type)   # Genera nuovo evento di arrivo

    elif event.event_time == 'C':  # Se l'evento è un completamento
        process_completion(event)

    else:
        raise ValueError('Tipo di evento non valido')

    # 3) Aggiorna il tempo di sistema e lo stato della coda
    times.current = times.next  # Aggiorno il timer di sistema
    update_queue_state()        # Aggiorna lo stato della coda


# Processa l'evento di arrivo e aggiorna lo stato del sistema
def process_arrival(event):
    # Se ci sono server liberi, il cliente viene servito immediatamente
    for i, s in enumerate(servers_state):
        if s == 0:  # TODO: Problema, meglio far lavorare quello fermo da più tempo (Equity), ci serve last
            # TODO completion time di ogni servente. Definition 2 pag 313 Alessia

            # ---------------- Assegna il cliente al server -----------------
            service_time = generate_service_time(event.client_type)  # Genero il tempo di servizio
            # Aggiorna il tempo di completamento del server
            event_list.completed[i].event_time = event.event_time + service_time
            # Aggiorna il tipo di cliente in servizio
            event_list.completed[i].client_type = event.client_type

            # ---------------- Aggiorna lo stato del sistema ----------------
            servers_state[i] = 1  # Imposto il server come occupato BUSY
            add_event_in_service(event)  # Aggiorna il numero di clienti di questo tipo in servizio

            break
    # Non ci sono server liberi
    else:
        # Il cliente viene accodato nell'apposita coda
        queues[event.client_type].append(event)

    # Aggiorna il numero di clienti nel sistema
    num_client_in_system[event.client_type] += 1


# Processa l'evento di completamento e aggiorna lo stato del sistema
def process_completion(event):
    id_server = None
    # Bisogna trovare il server che ha completato il servizio
    for i, s in enumerate(servers_state):
        if event == event_list.completed[i]:
            id_server = i
            # ---------------- Aggiorna lo stato del sistema ----------------
            servers_state[i] = 0  # Imposto il server come libero (IDLE)
            update_state_compl_event(event)  # Aggiorno lo stato del sistema

    select_client_from_queue(id_server)
    # Se non c'è nessuno in coda, il server riane libero


# Seleziona il prossimo cliente da servire in base alle specifiche di scheduling
def select_client_from_queue(id_server):
    # Possiamo andare a prendere il prossimo cliente in coda (se c'è)
    for i in range(QUEUES_NUM):
        if len(queues[i]) > 0:  # Controllo dalla coda con priorità più alta

            next_client = queues[i].pop(0)  # Prendo il cliente in coda
            service_time = generate_service_time(next_client.client_type)  # Genero il tempo di servizio

            # Aggiorno il tempo di completamento del server che si è liberato
            event_list.completed[id_server].event_time += service_time
            # Aggiorno il tipo di cliente in servizio
            event_list.completed[id_server].client_type = next_client.client_type

            # ---------------- Aggiorna lo stato del sistema ----------------
            servers_state[id_server] = 1  # Imposto il server come occupato BUSY
            add_event_in_service(next_client)  # Aggiorno il numero di clienti in servizio


# Trova l'evento più imminente nella lista degli eventi (Arrivo o Completamento)
# Restituisce il tempo dell'evento e il tipo di evento
def get_next_event():
    event = Event()

    # Cerca l'evento di arrivo più imminente (Tutti i valori devono essere maggiori di current, altrimenti problema)
    # serio
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


# Aggiorno il nuovo arrivo di client_type, basandomi sul tempo di arrivo precedente
def get_arrival(client_type):
    new_time = generate_arrival_time(client_type) + times.last[client_type]
    if new_time <= TEMPO_SIMULAZIONE:
        event_list.arrivals[client_type] = new_time
    else:
        event_list.arrivals[client_type] = None
        