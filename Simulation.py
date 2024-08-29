# Algoritmo 1 slide 9 per Next-Event Simulation
from libs.rngs import selectStream, plantSeeds
from libs.rvgs import Exponential, Uniform
from libs.rvms import cdfNormal, idfNormal
from utils import *

VERBOSE = True

# Inizializzazione delle variabili globali
times = Times()  # Tempi di sistema
event_list = EventList()  # Lista degli eventi del sistema
area = Area()  # Area di interesse per il calcolo delle prestazioni

# ------------------------------ Variabili per definire lo stato del sistema ------------------------------

servers_state = [0 for _ in range(SERVER_NUM)]  # Array binario: 0 = IDLE, 1 = BUSY
num_client_in_service = [0 for _ in range(QUEUES_NUM)]  # Numero di clienti in servizio.
queues_num = [0 for _ in range(QUEUES_NUM)]  # Numero di clienti in coda per ogni tipo

# ------------------------------ Variabili utilizzate  ------------------------------

queues = [[] for _ in range(QUEUES_NUM)]  # Una lista di eventi per ogni coda
num_client_in_system = [0 for _ in range(QUEUES_NUM)]  # Numero di clienti al momento nel sistema per ogni tipo
num_client_served = [0 for _ in range(QUEUES_NUM)]  # Numero di clienti serviti per ogni tipo
queues_state = [0 for _ in range(QUEUES_NUM)]  # Array binario: 0 = Empty, 1 = Not Empty
num_sampling = 0
# ---------------------------------------------------------------------------------------


# Inizializza la simulazione
def start():
    plantSeeds(SEED)

    # Inizializza i tempi di arrivo per ogni tipo di evento
    event_list.arrivals = [generate_arrival_time(i) for i in range(QUEUES_NUM)]
    generate_sampling_event()

    while times.current <= CLOSE_THE_DOOR_TIME or sum(num_client_in_system) != 0:
        if VERBOSE: print_status()

        process_next_event()  # Processa l'evento più imminente

        # Aggiungere evento di campionamento per le statistiche. Ogni # job completati si campiona
        # Va usato uvs per non memorizzare tutto il campione
        if sum(num_client_served) % SAMPLING_RATE_JOB == 0:
            # Evento di campionamento
            pass

    # Print delle statistiche finali
    if VERBOSE: print_final_stats()


# quello che andrà in loop
def process_next_event():
    # 1) Trova evento più imminente
    event, server_index_completed = get_next_event()
    if event is None:
        return
    times.next = event.event_time

    # 2) Aggiorna il tempo di sistema e le statistiche
    update_tip(area)  # Aggiorna le aree di interesse TODO: giusto?

    times.current = times.next  # Aggiorno il timer di sistema

    if VERBOSE: print(f"\n>>> Next Event: {event.event_type} | Client Type: {event.op_index}, "
                      f"Time: {event.event_time:.4f}")

    # 3) Processa l'evento e aggiorna lo stato del sistema
    if event.event_type == 'A':  # Se l'evento è un arrivo
        process_arrival(event)  # Processa l'arrivo
        times.last[event.op_index] = event.event_time  # TODO: times.last -> l'ultimo evento processato, giusto?
        generate_new_arrival(event.op_index)  # Genera nuovo evento di arrivo

    elif event.event_type == 'C':  # Se l'evento è un completamento
        process_completion(event, server_index_completed)

    elif event.event_type == 'S':  # Se l'evento è di campionamento
        process_sampling(event)
        generate_sampling_event()
    else:
        raise ValueError('Tipo di evento non valido')

    update_queue_state()  # Aggiorna lo stato della coda


# Trova l'evento più imminente nella lista degli eventi (Arrivo o Completamento)
# Restituisce il tempo dell'evento e il tipo di evento
def get_next_event():
    event = Event()
    server_index_completed = None

    # Cerca l'evento di arrivo più imminente
    # (Tutti i valori devono essere maggiori di current, altrimenti problema serio)
    for i in range(QUEUES_NUM):
        if event_list.arrivals[i] is not None:
            if ((event.event_time is None or event_list.arrivals[i] < event.event_time)
                    and event_list.arrivals[i] > times.current):
                event.event_time = event_list.arrivals[i]
                event.op_index = i
                event.event_type = 'A'

    # Cerca l'evento completamento più imminente (Se il valore è 0, non va considerato)
    for i in range(SERVER_NUM):
        if event_list.completed[i].event_time is not None and event_list.completed[i].event_time != 0:
            if (event.event_time is None or event_list.completed[i].event_time < event.event_time) and \
                    event_list.completed[i].event_time > times.current:
                event.event_time = event_list.completed[i].event_time
                event.op_index = event_list.completed[i].op_index
                event.event_type = 'C'
                server_index_completed = i

    # Verifico imminenza dell'evento di sampling
    if event_list.sampling is not None and event.event_time is not None:

        if event_list.sampling < event.event_time:
            event.event_time = event_list.sampling
            event.event_type = 'S'
            event.op_index = None

    if event.event_time is None:
        return None, None

    return event, server_index_completed


# Processa l'evento di arrivo (Generico)
def process_arrival(event):
    if event.op_index in MULTI_SERVER_QUEUES:  # Se il cliente nelle code di tipo Operazione Classica
        id_s_idle = server_selection_equity(MULTI_SERVER_INDEX)  # Bisogna selezionare il server fermo da più tempo se c'è
    elif event.op_index in SR_SERVER_QUEUES:  # Se il cliente nelle code di tipo Spedizione e Ritiri
        id_s_idle = server_selection_equity(SR_SERVER_INDEX)  # Bisogna selezionare il server fermo da più tempo se c'è
    elif event.op_index in ATM_SERVER_QUEUES:  # Se il cliente è nelle code di tipo ATM
        id_s_idle = server_selection_equity(ATM_SERVER_INDEX)  # Bisogna selezionare il server fermo da più tempo se c'è
    else:
        raise ValueError('Tipo di cliente non valido')

    # Se id_s_idle è libero, il cliente viene servito immediatamente
    if id_s_idle is not None:

        # ---------------- Assegna il cliente al server -----------------
        service_time = generate_service_time(event.op_index)  # Genero il tempo di servizio

        event_list.completed[id_s_idle].event_time = event.event_time + service_time # Aggiorno il tempo di completamento
        event_list.completed[id_s_idle].op_index = event.op_index  # Aggiorno il tipo di cliente in servizio

        if VERBOSE: print(f"Client served immediately by free server {id_s_idle}: "
                          f"Service completion time: {event_list.completed[id_s_idle].event_time:.4f}")

        # ---------------- Aggiorna lo stato del sistema ----------------
        servers_state[id_s_idle] = 1                # Imposto il server come occupato BUSY
        num_client_in_service[event.op_index] += 1  # Aggiorna il numero di clienti di questo tipo in servizio

    else:  # Non ci sono server liberi
        if VERBOSE: print(f"Client queued: Type {event.op_index}")
        queues[event.op_index].append(event)  # Aggiungi il cliente in coda

    num_client_in_system[event.op_index] += 1  # Aggiorna il numero di clienti nel sistema


# Processa l'evento di completamento e aggiorna lo stato del sistema
# id_server è l'indice del server che ha completato il servizio
def process_completion(event, id_server):

    # ---------------- Aggiorna lo stato del sistema ----------------
    servers_state[id_server] = 0                # Imposto il server come libero (IDLE)
    num_client_in_service[event.op_index] -= 1  # Rimuovo un cliente in servizio
    num_client_in_system[event.op_index] -= 1   # Rimuovo un cliente nel sistema
    num_client_served[event.op_index] += 1      # Incremento il numero di clienti serviti

    if VERBOSE: print(f"Server {id_server} completed request for client type {event.op_index}")

    # Seleziona il prossimo cliente da servire (se ce ne sono in coda)
    select_client_from_queue(id_server)
    # Se non c'è nessuno in coda, il server rimane libero


def process_sampling(event):
    # TODO: Implementare il campionamento
    global num_sampling
    num_sampling += 1
    return


# Seleziona il prossimo cliente da servire in base alle specifiche di scheduling
# id_s è l'indice del server che deve selezionare il cliente in coda, dato che lui ha completato.
def select_client_from_queue(id_s):

    if id_s in MULTI_SERVER_INDEX:  # Se il server è di tipo Operazione Classica
        queues_index = MULTI_SERVER_QUEUES
    elif id_s in SR_SERVER_INDEX:  # Se il server è di tipo Spedizione e Ritiri
        queues_index = SR_SERVER_QUEUES
    elif id_s in ATM_SERVER_INDEX:  # Se il server è di tipo ATM
        queues_index = ATM_SERVER_QUEUES
    else:
        raise ValueError('Tipo di server non valido')

    # Possiamo andare a prendere il prossimo cliente in coda (se c'è)
    for i in queues_index:
        if len(queues[i]) > 0:  # Controllo dalla coda con priorità più alta

            next_client = queues[i].pop(0)  # Prendo il cliente in testa alla coda
            service_time = generate_service_time(next_client.op_index)  # Genero il tempo di servizio

            event_list.completed[id_s].event_time += service_time       # Aggiorno il tempo di completamento
            event_list.completed[id_s].op_index = next_client.op_index  # Aggiorno il tipo di cliente in servizio

            if VERBOSE: print(f"Server {id_s} took client from queue of type {next_client.op_index}: "
                              f"Service completion time: {event_list.completed[id_s].event_time:.4f}")

            # ---------------- Aggiorna lo stato del sistema ----------------
            servers_state[id_s] = 1                             # Imposto il server come occupato BUSY
            num_client_in_service[next_client.op_index] += 1    # Aggiorno il numero di clienti in servizio
            break


# Aggiorna lo stato della coda
def update_queue_state():
    for i in range(QUEUES_NUM):
        if len(queues[i]) == 0:
            queues_state[i] = 0
        else:
            queues_state[i] = 1


# Dato l'indice del tipo di cliente, genera un tempo di interarrivo relativo alla tipologia di cliente
def generate_arrival_time(index_type):
    selectStream(index_type)
    if index_type == CLASSIC_ONLINE_STREAM:
        return Exponential(1 / (P_OC_ON * LAMBDA_ON))
    elif index_type == CLASSIC_DIFF_STREAM:
        return Exponential(1 / (P_OC * P_DIFF * LAMBDA))
    elif index_type == CLASSIC_STREAM:
        return Exponential(1 / (P_OC * (1 - P_DIFF) * LAMBDA))
    elif index_type == SR_ONLINE_STREAM:
        return Exponential(1 / (P_SR_ON * LAMBDA_ON))
    elif index_type == SR_DIFF_STREAM:
        return Exponential(1 / (P_SR * P_DIFF * LAMBDA))
    elif index_type == SR_STREAM:
        return Exponential(1 / (P_SR * (1 - P_DIFF) * LAMBDA))
    elif index_type == ATM_DIFF_STREAM:
        return Exponential(1 / (P_ATM * P_DIFF * LAMBDA))
    elif index_type == ATM_STREAM:
        return Exponential(1 / (P_ATM * (1 - P_DIFF) * LAMBDA))
    else:
        raise ValueError('Tipo di cliente (index_type) non valido in GetArrival')


# Dato l'indice del tipo di cliente, genera il tempo di servizio relativo alla tipologia di server (OC, SR, ATM)
def generate_service_time(index_type):
    # Meglio usare una nomale Normal(15 minuti, 5 minuti) -> 15 minuti di media centro campana, 5 minuti di
    # deviazione standard
    # return truncate_normal(15, 5,  10 ** -6, float('inf'))

    if index_type in MULTI_SERVER_QUEUES:
        selectStream(CLASSIC_SERVICE_STREAM)    # Stream 8 per servizi dei clienti OC
        return Exponential(1 / MU_OC)
    elif index_type in SR_SERVER_QUEUES:
        selectStream(SR_SERVICE_STREAM)         # Stream 9 per servizi dei clienti SR
        return Exponential(1 / MU_SR)
    elif index_type in ATM_SERVER_QUEUES:
        selectStream(ATM_SERVICE_STREAM)        # Stream 10 per servizi dei clienti ATM
        return Exponential(1 / MU_ATM)
    else:
        raise ValueError('Tipo di cliente non valido')


# Aggiorno il nuovo arrivo di client_type, basandomi sul tempo di arrivo precedente
def generate_new_arrival(queue_index):
    new_time = generate_arrival_time(queue_index) + times.current   # last[queue_index]
    if new_time <= CLOSE_THE_DOOR_TIME:
        event_list.arrivals[queue_index] = new_time
    else:
        times.last[queue_index] = times.current     # Memorizziamo l'ultimo arrivo
        event_list.arrivals[queue_index] = None


# Aggiorno il valore di event_list.sampling con il prossimo evento di campionamento (minuto o num job)
# Se non ci sono più eventi di campionamento, lo imposto a None
def generate_sampling_event():
    # Minuti
    if SAMPLING_TYPE == 0:
        event_list.sampling += SAMPLING_RATE_MIN
        if event_list.sampling > CLOSE_THE_DOOR_TIME:
            event_list.sampling = None
    # Job
    elif SAMPLING_TYPE == 1:
        event_list.sampling += SAMPLING_RATE_JOB
        if event_list.sampling > SIMULATION_JOB_NUM:
            event_list.sampling = None
    else:
        raise ValueError('Tipo di campionamento non valido')


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


def print_status():
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
    print(
        f"   average interarrival time = {sum(times.last) / index:6.2f}")  # Interarrival = Tempo tra due arrivi successivi
    print(
        f"   average wait ............ = {sum(area.customers) / index:6.2f}")  # Wait = Tempo di risposta = Tempo di attesa in coda + Tempo di servizio
    print(f"   average delay ........... = {sum(area.queue) / index:6.2f}")  # Delay = Tempo di attesa in coda
    print(f"   average service time .... = {sum(area.service) / index:6.2f}")
    # time-average statistics: Sono statistiche step wise perche sono popolazioni, incrementano e decrementano di uno
    print(f"   average # in the node ... = {sum(area.customers) / times.current:6.2f}")  # l(t)
    print(f"   average # in the queue .. = {sum(area.queue) / times.current:6.2f}")  # q(t)
    print(f"   utilization ............. = {sum(area.service) / times.current:6.2f}")
    print(f"\nSimulation complete. Clients served: {num_client_served}")
    print("num sampling: ", num_sampling)
    # x(t) = numero di job in servizio
    # l(t) = q(t) + x(t) = numero di job nel sistema

    # La relazione tra job-average e time-average è data dalla legge di Little

    # Intensità di traffico: rapporto tra freq. di arrivo e di completamento:
    # s/r = (c_n/ a_n)*x -> s : tempo di servizio


# Quando più server sono in idle, seleziona il server che è IDLE da più tempo
# Questo evita situazioni in cui è sempre il server con id più basso a prendere il cliente
# Se la lista dei server è composta da un solo server, lo restituisce se IDLE
# Se nessun server nella lista è IDLE, restituisce None
def server_selection_equity(servers_index):
    # Cerco i server liberi
    server_id_idle = []
    for i in servers_index:
        if servers_state[i] == 0:
            server_id_idle.append(i)

    if len(server_id_idle) == 0:
        return None  # Nessun server libero
    elif len(server_id_idle) == 1:
        return server_id_idle[0]

    # Se ci sono più server da valutare
    min_completion_time = float('inf')
    selected_server = None

    # Trovo il server libero con il tempo di completamento minore
    for i in server_id_idle:
        if event_list.completed[i].event_time is not None:
            if event_list.completed[i].event_time < min_completion_time:
                min_completion_time = event_list.completed[i].event_time
                selected_server = i
        else:
            return i  # None -> non ha mai lavorato
    return selected_server


# Tronca la distribuzione normale tra inf e sup - Lezione 28-05 (numero 31) SBAGLIATA
def truncate_normal(mu, sigma, inf, sup):
    alpha = cdfNormal(inf, mu, sigma)
    beta = 1 - cdfNormal(sup, mu, sigma)

    u = Uniform(alpha, 1 - beta)
    return idfNormal(u, mu, sigma)


start()
