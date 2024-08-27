# Algoritmo 1 slide 9 per Next-Event Simulation
from libs.rngs import selectStream, plantSeeds
from libs.rvgs import Exponential
from utils import *

VERBOSE = True

# Inizializzazione delle variabili globali
times = Times()  # Tempi di sistema
event_list = EventList()  # Lista degli eventi del sistema
area = Area()  # Area di interesse per il calcolo delle prestazioni

# ------------------- Variabili per definire lo stato del sistema -----------------------

servers_state = [0 for _ in range(N)]  # Array binario: 0 = IDLE, 1 = BUSY
num_client_in_system = [0 for _ in range(QUEUES_NUM)]  # Numero di clienti al momento nel sistema per ogni tipo
num_client_in_service = [0 for _ in range(QUEUES_NUM)]  # Numero di clienti in servizio.
num_client_served = [0 for _ in range(QUEUES_NUM)]  # Numero di clienti serviti per ogni tipo
queues = [[] for _ in range(QUEUES_NUM)]  # Una lista di eventi per ogni coda
queues_state = [0 for _ in range(QUEUES_NUM)]  # Array binario: 0 = Empty, 1 = Not Empty


# ---------------------------------------------------------------------------------------


# Inizializza la simulazione
def start():
    plantSeeds(SEED)

    # Inizializza i tempi di arrivo per ogni tipo di evento
    event_list.arrivals = [generate_arrival_time(i) for i in range(QUEUES_NUM)]

    while times.current < TEMPO_SIMULAZIONE or sum(num_client_in_system) != 0:
        if VERBOSE: print_stats()

        process_next_event()  # Processa l'evento più imminente

    # Print delle statistiche finali
    if VERBOSE: print_final_stats()


# quello che andrà in loop
def process_next_event():
    # 1) Trova evento più imminente
    event = get_next_event()
    if event is None:
        return
    times.next = event.event_time

    # 2) Aggiorna il tempo di sistema e le statistiche
    update_tip(area)  # Aggiorna le aree di interesse
    times.current = times.next  # Aggiorno il timer di sistema

    if VERBOSE: print(f"\n>>> Next Event: {event.event_type} | Client Type: {event.client_type}, "
                      f"Time: {event.event_time:.4f}")

    # 3) Processa l'evento e aggiorna lo stato del sistema
    if event.event_type == 'A':  # Se l'evento è un arrivo
        process_arrival(event)  # Processa l'arrivo
        times.last[event.client_type] = event.event_time  # TODO: times.last -> l'ultimo evento processato, giusto?
        generate_new_arrival(event.client_type)  # Genera nuovo evento di arrivo

    elif event.event_type == 'C':  # Se l'evento è un completamento
        process_completion(event)

    else:
        raise ValueError('Tipo di evento non valido')

    update_queue_state()  # Aggiorna lo stato della coda


# Processa l'evento di arrivo e aggiorna lo stato del sistema
def process_arrival(event):
    id_s_idle = server_selection_equity()

    # Se ci sono server liberi, il cliente viene servito immediatamente
    if id_s_idle is not None:

        # ---------------- Assegna il cliente al server -----------------
        service_time = generate_service_time(event.client_type)  # Genero il tempo di servizio

        event_list.completed[id_s_idle].event_time = event.event_time + service_time  # Aggiorno il tempo di completamento
        event_list.completed[id_s_idle].client_type = event.client_type  # Aggiorno il tipo di cliente in servizio

        if VERBOSE: print(f"Client served immediately by free server {id_s_idle}: "
                          f"Service completion time: {event_list.completed[id_s_idle].event_time:.4f}")

        # ---------------- Aggiorna lo stato del sistema ----------------
        servers_state[id_s_idle] = 1  # Imposto il server come occupato BUSY
        num_client_in_service[event.client_type] += 1  # Aggiorna il numero di clienti di questo tipo in servizio

    else:  # Non ci sono server liberi
        if VERBOSE: print(f"Client queued: Type {event.client_type}")
        queues[event.client_type].append(event)  # Aggiungi il cliente in coda

    num_client_in_system[event.client_type] += 1  # Aggiorna il numero di clienti nel sistema


# Processa l'evento di completamento e aggiorna lo stato del sistema
def process_completion(event):
    id_server = None
    # Bisogna trovare il server che ha completato il servizio
    for i, s in enumerate(servers_state):
        if event == event_list.completed[i]:
            id_server = i
            # ---------------- Aggiorna lo stato del sistema ----------------
            servers_state[i] = 0  # Imposto il server come libero (IDLE)
            num_client_in_service[event.client_type] -= 1  # Rimuovo un cliente in servizio
            num_client_in_system[event.client_type] -= 1  # Rimuovo un cliente nel sistema
            num_client_served[event.client_type] += 1  # Incremento il numero di clienti serviti

            if VERBOSE: print(f"Server {id_server} completed request for client type {event.client_type}")

    # Seleziona il prossimo cliente da servire (se ce ne sono in coda)
    select_client_from_queue(id_server)
    # Se non c'è nessuno in coda, il server rimane libero


# Seleziona il prossimo cliente da servire in base alle specifiche di scheduling
def select_client_from_queue(id_s):
    # Possiamo andare a prendere il prossimo cliente in coda (se c'è)
    for i in range(QUEUES_NUM):
        if len(queues[i]) > 0:  # Controllo dalla coda con priorità più alta

            next_client = queues[i].pop(0)  # Prendo il cliente in coda
            service_time = generate_service_time(next_client.client_type)  # Genero il tempo di servizio

            event_list.completed[id_s].event_time += service_time  # Aggiorno il tempo di completamento
            event_list.completed[id_s].client_type = next_client.client_type  # Aggiorno il tipo di cliente in servizio

            if VERBOSE: print(f"Server {id_s} took client from queue of type {next_client.client_type}: "
                              f"Service completion time: {event_list.completed[id_s].event_time:.4f}")

            # ---------------- Aggiorna lo stato del sistema ----------------
            servers_state[id_s] = 1  # Imposto il server come occupato BUSY
            num_client_in_service[next_client.client_type] += 1  # Aggiorno il numero di clienti in servizio
            break


# Trova l'evento più imminente nella lista degli eventi (Arrivo o Completamento)
# Restituisce il tempo dell'evento e il tipo di evento
def get_next_event():
    event = Event()

    # Cerca l'evento di arrivo più imminente
    # (Tutti i valori devono essere maggiori di current, altrimenti problema serio)
    for i in range(QUEUES_NUM):
        if event_list.arrivals[i] is not None:
            if ((event.event_time is None or event_list.arrivals[i] < event.event_time)
                    and event_list.arrivals[i] > times.current):
                event.event_time = event_list.arrivals[i]
                event.client_type = i
                event.event_type = 'A'

    # Cerca l'evento completamento più imminente (Se il valore è 0, non va considerato)
    for i in range(N):
        if event_list.completed[i].event_time is not None and event_list.completed[i].event_time != 0:
            if (event.event_time is None or event_list.completed[i].event_time < event.event_time) and \
                    event_list.completed[i].event_time > times.current:
                event = event_list.completed[i]

    if event.event_time is None:
        return None

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
def generate_new_arrival(client_type):
    new_time = generate_arrival_time(client_type) + times.last[client_type]
    if new_time <= TEMPO_SIMULAZIONE:
        event_list.arrivals[client_type] = new_time
    else:
        event_list.arrivals[client_type] = None


# ------------------------------- Funzioni di supporto --------------------------------
def update_tip(area):
    for i in range(QUEUES_NUM):
        if num_client_in_system[i] > 0:
            area.customers[i] += (times.next - times.current) * num_client_in_system[i]
            area.queue[i] += (times.next - times.current) * (num_client_in_system[i] - num_client_in_service[i])
            area.service[i] += (times.next - times.current) * num_client_in_service[i]


# Formatta le code per la stampa
def format_queues(queues):
    formatted_queues = []
    for q in queues:
        formatted_queue = [event.event_time for event in q]  # Estrai solo i tempi da ciascun oggetto evento
        formatted_queues.append(formatted_queue)
    return formatted_queues


def print_stats():
    formatted_queues = format_queues(queues)  # Usa la funzione di supporto per formattare le code
    print(f"\n{'=' * 30}\n"
          f"Searching for the next event...\n"
          f"System Timer: {times.current:.4f} | "
          f"Clients in system: {num_client_in_system} | "
          f"Clients in service: {num_client_in_service} | "
          f"Clients served: {num_client_served} | "
          f"Queues: {formatted_queues}\n{'=' * 30}")


def print_final_stats():
    index = sum(num_client_served)
    print(f"for {index} jobs")
    # job-average statistics
    print(f"   average interarrival time = {sum(times.last) / index:6.2f}") # Interarrival = Tempo tra due arrivi successivi
    print(f"   average wait ............ = {sum(area.customers) / index:6.2f}") # Wait = Tempo di risposta = Tempo di attesa in coda + Tempo di servizio
    print(f"   average delay ........... = {sum(area.queue) / index:6.2f}") # Delay = Tempo di attesa in coda
    print(f"   average service time .... = {sum(area.service) / index:6.2f}")
    # time-average statistics: Sono statistiche step wise perche sono popolazioni, incrementano e decrementano di uno
    print(f"   average # in the node ... = {sum(area.customers) / times.current:6.2f}") # l(t)
    print(f"   average # in the queue .. = {sum(area.queue) / times.current:6.2f}") # q(t)
    print(f"   utilization ............. = {sum(area.service) / times.current:6.2f}")
    print(f"\nSimulation complete. Clients served: {num_client_served}")
    # x(t) = numero di job in servizio
    # l(t) = q(t) + x(t) = numero di job nel sistema

    # La relazione tra job-average e time-average è data dalla legge di Little

    # Intensità di traffico: rapporto tra freq. di arrivo e di completamento:
    # s/r = (c_n/ a_n)*x -> s : tempo di servizio


# Quando più server sono in idle, seleziona il server che è fermo da più tempo
# Questo evita situazioni in cui è sempre il server con id più basso a prendere il cliente
def server_selection_equity():
    # Cerco i server liberi
    server_id_idle = [i for i, s in enumerate(servers_state) if s == 0]

    if not server_id_idle:
        return None  # Nessun server libero

    min_completion_time = float('inf')
    selected_server = None

    # Trovo il server libero con il tempo di completamento minore
    for i in server_id_idle:
        if event_list.completed[i].event_time is not None:
            if event_list.completed[i].event_time < min_completion_time:
                min_completion_time = event_list.completed[i].event_time
                selected_server = i
        else:
            return i    # None -> non ha mai lavorato
    return selected_server


start()
