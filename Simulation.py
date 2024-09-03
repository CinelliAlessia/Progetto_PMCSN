# Algoritmo 1 slide 9 per Next-Event Simulation
from libs.rngs import selectStream
from libs.rvgs import Exponential
from Class_definition import *
from utils import *


def initialize_globals():
    global times, event_list, area_list, accumSum, servers_state, num_client_in_service, queues_num, queues, \
        num_client_in_system, num_client_served, num_sampling, CLOSE_THE_DOOR_TIME, FINITE, INFINITE, SAMPLING_RATE_MIN

    # Inizializzazione delle variabili globali
    times = Times()  # Tempi di sistema
    event_list = EventList()  # Lista degli eventi del sistema
    area_list = [Area() for _ in range(QUEUES_NUM)]  # Lista delle aree di interesse per il calcolo delle prestazioni
    accumSum = [AccumSum() for _ in range(SERVER_NUM)]  # Accumulatore delle somme per il calcolo delle prestazioni

    # ------------------------------ Variabili per definire lo stato del sistema ------------------------------

    servers_state = [0 for _ in range(SERVER_NUM)]  # Array binario: 0 = IDLE, 1 = BUSY
    num_client_in_service = [0 for _ in range(QUEUES_NUM)]  # Numero di clienti in servizio.
    queues_num = [0 for _ in range(QUEUES_NUM)]  # Numero di clienti in coda per ogni tipo

    # ------------------------------ Variabili utilizzate  ------------------------------

    queues = [[] for _ in range(QUEUES_NUM)]  # Una lista di eventi per ogni coda
    num_client_in_system = [0 for _ in range(QUEUES_NUM)]  # Numero di clienti al momento nel sistema per ogni tipo
    num_client_served = [0 for _ in range(QUEUES_NUM)]  # Numero di clienti serviti per ogni tipo
    num_sampling = 0

    # ---------------------------------------------------------------------------------------

    CLOSE_THE_DOOR_TIME = 0  # Tempo di chiusura della simulazione
    FINITE = False
    INFINITE = False
    SAMPLING_RATE_MIN = 0


def initialize(end_time, type_simulation, sampling_rate=0):
    global CLOSE_THE_DOOR_TIME, FINITE, INFINITE, SAMPLING_RATE_MIN
    CLOSE_THE_DOOR_TIME = end_time

    if type_simulation == "finite":
        FINITE = True
    elif type_simulation == "infinite":
        INFINITE = True
    SAMPLING_RATE_MIN = sampling_rate


def start_simulation(end_time, type_simulation, sampling_rate=0, batch_num=0):
    """
    Inizializza la simulazione e gestisce il loop principale
    :return:
    """

    initialize_globals()
    initialize(end_time, type_simulation, sampling_rate)

    # Inizializza i tempi di arrivo per ogni tipo di evento
    event_list.arrivals = [0 for _ in range(QUEUES_NUM)]
    for i in range(QUEUES_NUM):
        generate_new_arrival(i)

    generate_sampling_event()

    if FINITE:
        # SIMULA FINO A CHE NON SI RAGGIUNGE IL TEMPO DI CHIUSURA O NON CI SONO PIÙ CLIENTI NEL SISTEMA
        while times.current <= CLOSE_THE_DOOR_TIME or sum(num_client_in_system) != 0:
            if VERBOSE: print_status()
            process_next_event()  # Processa l'evento più imminente
    elif INFINITE:
        # SIMULA FINO A CHE NON SI RAGGIUNGE IL NUMERO DI BATCH
        while num_sampling < batch_num:
            if VERBOSE: print_status()
            process_next_event() # Processa l'evento più imminente

    # ------------------ Condizione di terminazione raggiunta --------------------
    # Print delle statistiche finali
    if VERBOSE: print_final_stats()
    if FINITE: save_stats("finite")
    print("end time", times.current, " ore:", times.current / 60)


def get_next_event():
    """
    Trova l'evento più imminente nella lista degli eventi (Arrivo, Completamento, Sampling)
    :return: Restituisce l'evento più imminente e l'indice del server se esso è un completamento
    """
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


def process_next_event():
    """
    Processa l'evento più imminente e aggiorna lo stato del sistema
    :return:
    """
    # 1) Trova evento più imminente
    event, server_index_completed = get_next_event()
    if event is None:
        return
    times.next = event.event_time

    if VERBOSE: print(f"\n>>> Next Event: {event.event_type} | Client Type: {event.op_index}, "
                      f"Time: {event.event_time:.4f}")

    # 3) Processa l'evento e aggiorna lo stato del sistema
    if event.event_type == 'A':     # Se l'evento è un arrivo
        process_arrival(event)      # Processa l'arrivo
        times.last[event.op_index] = event.event_time  # TODO: times.last -> l'ultimo evento processato, giusto?
        generate_new_arrival(event.op_index)  # Genera nuovo evento di arrivo
    elif event.event_type == 'C':  # Se l'evento è un completamento
        process_completion(event, server_index_completed)
    elif event.event_type == 'S':  # Se l'evento è di campionamento
        process_sampling(event)
        generate_sampling_event()
    else:
        raise ValueError('Tipo di evento non valido')

    # 3) Aggiorna il tempo di sistema e le statistiche
    if not event.event_type == 'S':
        update_tip(area_list)   # Aggiorna le aree di interesse TODO: giusto?

    times.current = times.next  # Aggiorno il timer di sistema


def process_arrival(event):
    """
    Processa l'evento di arrivo e aggiorna lo stato del sistema
    :param event: Rappresenta l'evento di arrivo
    :return: None
    """
    if event.op_index in MULTI_SERVER_QUEUES:  # Se il cliente nelle code di tipo Operazione Classica
        id_s_idle = server_selection_equity(MULTI_SERVER_INDEX)  # Bisogna selezionare il server fermo da più tempo se c'è
    elif event.op_index in SR_SERVER_QUEUES:  # Se il cliente nelle code di tipo Spedizione e Ritiri
        id_s_idle = server_selection_equity(SR_SERVER_INDEX)  # Bisogna selezionare il server fermo da più tempo se c'è
    elif event.op_index in ATM_SERVER_QUEUES:  # Se il cliente è nelle code di tipo ATM
        id_s_idle = server_selection_equity(ATM_SERVER_INDEX)  # Bisogna selezionare il server fermo da più tempo se c'è
    elif event.op_index in LOCKER_SERVER_QUEUES:
        id_s_idle = server_selection_equity(LOCKER_SERVER_INDEX)
    else:
        raise ValueError('Tipo di cliente non valido')

    # Se abbiamo un server libero, il cliente viene servito immediatamente
    if id_s_idle is not None:

        # ---------------- Assegna il cliente al server -----------------
        service_time = generate_service_time(event.op_index)  # Genero il tempo di servizio

        event_list.completed[id_s_idle].event_time = event.event_time + service_time # Aggiorno il tempo di completamento
        event_list.completed[id_s_idle].op_index = event.op_index  # Aggiorno il tipo di cliente in servizio

        update_acc_sum(service_time, id_s_idle)

        if VERBOSE: print(f"Client served immediately by free server {id_s_idle}: "
                          f"Service completion time: {event_list.completed[id_s_idle].event_time:.4f}")

        # ---------------- Aggiorna lo stato del sistema ----------------
        servers_state[id_s_idle] = 1                # Imposto il server come occupato BUSY
        num_client_in_service[event.op_index] += 1  # Aggiorna il numero di clienti di questo tipo in servizio

    else:  # Non ci sono server liberi
        if VERBOSE: print(f"Client queued: Type {event.op_index}")
        queues[event.op_index].append(event)  # Aggiungi il cliente in coda

    num_client_in_system[event.op_index] += 1  # Aggiorna il numero di clienti nel sistema


def process_completion(event, id_server):
    """
    Processa l'evento di completamento e aggiorna lo stato del sistema
    :param event: Rappresenta l'evento di completamento
    :param id_server: L'indice del server che ha completato il servizio
    :return:
    """

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
    """
    Processa l'evento di campionamento utilizzato nella simulazione con batch means
    o nel calcolo delle prestazioni su necessità
    :param event:
    :return:
    """

    # TODO: Implementare il campionamento
    global num_sampling, FINITE, INFINITE
    if FINITE:
        pass
    elif INFINITE: # Campionamento per batch means
        save_stats("infinite")

    num_sampling += 1
    return


def select_client_from_queue(id_s):
    """
    Seleziona il prossimo cliente da servire in base alle specifiche di scheduling
    :param id_s: L'indice del server che deve selezionare il cliente in coda, dato che lui ha completato
    :return: None
    """

    if id_s in MULTI_SERVER_INDEX:  # Se il server è di tipo Operazione Classica
        queues_index = MULTI_SERVER_QUEUES
    elif id_s in SR_SERVER_INDEX:  # Se il server è di tipo Spedizione e Ritiri
        if IMPROVED_SIM: queues_index = SR_SERVER_QUEUES + MULTI_SERVER_QUEUES
        else: queues_index = SR_SERVER_QUEUES
    elif id_s in ATM_SERVER_INDEX:  # Se il server è di tipo ATM
        queues_index = ATM_SERVER_QUEUES
    elif id_s in LOCKER_SERVER_INDEX:
        queues_index = LOCKER_SERVER_QUEUES
    else:
        raise ValueError('Tipo di server non valido')

    # Possiamo andare a prendere il prossimo cliente in coda (se c'è)
    for i in queues_index:
        if len(queues[i]) > 0:  # Controllo dalla coda con priorità più alta

            next_client = queues[i].pop(0)  # Prendo il cliente in testa alla coda
            service_time = generate_service_time(next_client.op_index)  # Genero il tempo di servizio

            event_list.completed[id_s].event_time += service_time       # Aggiorno il tempo di completamento
            event_list.completed[id_s].op_index = next_client.op_index  # Aggiorno il tipo di cliente in servizio

            update_acc_sum(service_time, id_s)

            if VERBOSE: print(f"Server {id_s} took client from queue of type {next_client.op_index}: "
                              f"Service completion time: {event_list.completed[id_s].event_time:.4f}")

            # ---------------- Aggiorna lo stato del sistema ----------------
            servers_state[id_s] = 1                             # Imposto il server come occupato BUSY
            num_client_in_service[next_client.op_index] += 1    # Aggiorno il numero di clienti in servizio
            break


def generate_interarrival_time(index_type):
    """
    Genera il tempo di arrivo per un cliente di tipo index_type
    :param index_type: Indice del tipo di cliente, rappresenta la tipologia di coda in cui andrà
    :return: Il tempo di interarrivo del cliente
    """
    selectStream(index_type)
    if IMPROVED_SIM and LOCKER:
        if index_type == SR_DIFF_STREAM:
            return Exponential(1 / ((1-P_LOCKER) * P_SR * P_DIFF * (1-P_ON) * LAMBDA))
        elif index_type == SR_STREAM:
            return Exponential(1 / ((1-P_LOCKER) * P_SR * (1 - P_DIFF) * (1-P_ON) * LAMBDA))
        elif index_type == LOCKER_STREAM:
            return Exponential(1 / (P_LOCKER * P_SR * (1-P_DIFF) * (1-P_ON) * LAMBDA))

    if index_type == CLASSIC_ONLINE_STREAM:
        return Exponential(1 / (P_OC_ON * P_ON * LAMBDA))
    elif index_type == CLASSIC_DIFF_STREAM:
        return Exponential(1 / (P_OC * P_DIFF * (1-P_ON) * LAMBDA))
    elif index_type == CLASSIC_STREAM:
        return Exponential(1 / (P_OC * (1 - P_DIFF) * (1-P_ON) * LAMBDA))
    elif index_type == SR_ONLINE_STREAM:
        return Exponential(1 / (P_SR_ON * P_ON * LAMBDA))
    elif index_type == SR_DIFF_STREAM:
        return Exponential(1 / (P_SR * P_DIFF * (1 - P_ON) * LAMBDA))
    elif index_type == SR_STREAM:
        return Exponential(1 / (P_SR * (1 - P_DIFF) * (1-P_ON) * LAMBDA))
    elif index_type == ATM_DIFF_STREAM:
        return Exponential(1 / (P_ATM * P_DIFF * (1-P_ON) * LAMBDA))
    elif index_type == ATM_STREAM:
        return Exponential(1 / (P_ATM * (1 - P_DIFF) * (1-P_ON) * LAMBDA))
    else:
        raise ValueError(f'Tipo di cliente ({index_type}) non valido in GetArrival')


def generate_service_time(queue_index):
    """
    Genera il tempo di servizio per un cliente di tipo index_type, in base alla tipologia di server (OC, SR, ATM)
    :param queue_index: Indice del tipo di cliente, rappresenta la tipologia di coda in cui andrebbe
    :return: Il tempo di servizio del cliente
    """

    if queue_index in MULTI_SERVER_QUEUES:
        selectStream(CLASSIC_SERVICE_STREAM)    # Stream 8 per servizi dei clienti OC
        return truncate_normal(1 / MU_OC, SIGMA_OC, 10 ** -6, float('inf'))
        # return Exponential(1 / MU_OC)
    elif queue_index in SR_SERVER_QUEUES:
        selectStream(SR_SERVICE_STREAM)         # Stream 9 per servizi dei clienti SR
        return truncate_normal(1 / MU_SR, SIGMA_SR, 10 ** -6, float('inf'))
        # return Exponential(1 / MU_SR)
    elif queue_index in ATM_SERVER_QUEUES:
        selectStream(ATM_SERVICE_STREAM)        # Stream 10 per servizi dei clienti ATM
        return truncate_normal(1 / MU_ATM, SIGMA_ATM, 10 ** -6, float('inf'))
        # return Exponential(1 / MU_ATM)
    elif queue_index in LOCKER_SERVER_QUEUES:
        selectStream(LOCKER_SERVICE_STREAM)
        return truncate_normal(1 / MU_LOCKER, SIGMA_LOCKER, 10 ** -6, float('inf'))
    else:
        raise ValueError('Tipo di cliente non valido')


def generate_new_arrival(queue_index):
    """
    Genera un nuovo arrivo per il tipo di coda specificato
    :param queue_index: Indice della coda per cui generare un nuovo arrivo
    :return: None
    """

    # TODO
    # p_loss = calculate_p_loss()
    # if random() < p_loss:
      #  return

    """current_time = times.next

    stop = True
    while(stop):
        p_loss = calculate_p_loss()
        if random() < p_loss:
            stop = False
            break"""

    new_time = generate_interarrival_time(queue_index) + times.next   # last[queue_index]
    if new_time <= CLOSE_THE_DOOR_TIME:
        event_list.arrivals[queue_index] = new_time
    else:
        times.last[queue_index] = times.next     # Memorizziamo l'ultimo arrivo
        event_list.arrivals[queue_index] = None


def generate_sampling_event():
    """
    Genera il prossimo evento di campionamento in base al tipo di campionamento (minuti o job)
    Se non ci sono più eventi di campionamento (TIME_LIMIT), viene impostato None
    :return: None
    """
    # Minuti
    event_list.sampling += SAMPLING_RATE_MIN
    if event_list.sampling > CLOSE_THE_DOOR_TIME:
        event_list.sampling = None


def server_selection_equity(servers_index):
    """
    Seleziona il server libero da più tempo tra quelli nella lista. Equity
    Questo evita situazioni in cui è sempre il server con id più basso a prendere il cliente
    Se la lista dei server è composta da un solo server, lo restituisce se IDLE
    Se nessun server nella lista è IDLE, restituisce None
    :param servers_index: Lista degli indici dei server da valutare per la scelta
    :return:
    """
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


# ---------------- Funzioni di supporto ----------------
def calculate_p_loss():
    """
    Calcola la probabilità di perdita in base al numero di clienti nel sistema
    :return: La probabilità di perdita
    """
    prob = sum(num_client_in_system) / MAX_PEOPLE   #TODO: forse va normalizzata su uno
    if prob > P_MAX_LOSS:
        return P_MAX_LOSS
    return prob


def update_tip(area_list):
    """
    Aggiorna le aree di interesse per il calcolo delle prestazioni
    :param area_list:
    :return:
    """
    for i in range(QUEUES_NUM):
        if num_client_in_system[i] > 0:
            area_list[i].customers += (times.next - times.current) * num_client_in_system[i]
            area_list[i].queue += (times.next - times.current) * (num_client_in_system[i] - num_client_in_service[i])
            area_list[i].service += (times.next - times.current) # * num_client_in_service[i]


def print_status():
    """
    Stampa lo stato del sistema
    :return:
    """
    formatted_queues = format_queues(queues)  # Usa la funzione di supporto per formattare le code
    print(f"\n{'=' * 30}\n"
          f"Searching for the next event...\n"
          f"System Timer: {times.current:.4f} | "
          f"Clients in system: {num_client_in_system} | "
          f"Clients in service: {num_client_in_service} | "
          f"Clients served: {num_client_served} | "
          f"Queues: {formatted_queues}\n{'=' * 30}")


def print_final_stats():
    """
    Stampa le statistiche finali del sistema
    :return:
    """
    index = sum(num_client_served)
    if index == 0:
        print("Non sono stati serviti clienti")
        return
    print(f"# job serviti: {index}")
    print(f"average interarrival time = {max(times.last) / index:6.8f}")  # Interarrival = Tempo tra due arrivi successivi

    print("    server     utilization     avg service        share\n")
    for s in range(SERVER_NUM):
        print("{0:8d} {1:14.3f} {2:15.2f} {3:15.3f}".format(
            s + 1,
            accumSum[s].service / times.current,
            accumSum[s].service / accumSum[s].served,
            float(accumSum[s].served) / index
        ))

    print("{0:8} {1:14} {2:14} {3:16} {4:17} {5:17} {6:15}".format(
        "queue", "avg wait t", "avg delay t",  "avg service t",
        "avg # in node", "avg # in queue", "avg # in service"))
    for c in range(QUEUES_NUM):
        if num_client_served[c] == 0:
            continue

        # Job-average statistics
        avg_wait = area_list[c].customers / num_client_served[c]    # Tempo di risposta
        avg_delay = area_list[c].queue / num_client_served[c]       # Tempo di attesa in coda
        avg_service_time = area_list[c].service / num_client_served[c]  # Tempo di servizio

        # Time-average statistics
        avg_num_in_sys = area_list[c].customers / times.current
        avg_num_in_queue = area_list[c].queue / times.current
        avg_num_in_service = area_list[c].service / times.current

        print("{0:8d} {1:12.8f} {2:12.8f} {3:14.8f} {4:17.8f} {5:17.8f} {6:14.8f}".format(
            c + 1,
            avg_wait,
            avg_delay,
            avg_service_time,
            avg_num_in_sys,
            avg_num_in_queue,
            avg_num_in_service
        ))

    print(f"\nSimulation complete. Clients served: {num_client_served}")
    print("num sampling: ", num_sampling)


def update_acc_sum(service_time, id_s):
    accumSum[id_s].service += service_time
    accumSum[id_s].served += 1


def save_stats(tipo):
    """
    Calcola e salva le statistiche finali su file CSV per ogni run.

    :param tipo: Il tipo di statistica ('finito' o 'infinito') che determina il percorso dei file e il calcolo.
    :return: None
    """
    csv_utilization = CSV_UTILIZATION
    csv_delay = CSV_DELAY
    csv_waiting_time = CSV_WAITING_TIME

    if tipo == 'finite':
        directory = DIRECTORY_FINITE_H
    elif tipo == 'infinite':
        directory = DIRECTORY_INFINITE_H
    else:
        raise ValueError("Tipo non valido. Utilizzare 'finito' o 'infinito'.")

    # Nome del file CSV
    rho_csv = directory + csv_utilization

    for s in range(SERVER_NUM):
        # Calcolo dell'utilizzo del server
        rho = accumSum[s].service / times.current

        # Scrive direttamente il valore rho nel file CSV, separando con una virgola
        save_stats_on_file(rho_csv, f"{rho}, ")
    # Aggiunge una nuova linea per separare le statistiche del prossimo run
    save_stats_on_file(rho_csv, "\n")

    for c in range(QUEUES_NUM):
        if num_client_served[c] == 0:
            continue

        # Job-average statistics
        avg_wait = area_list[c].customers / num_client_served[c]  # Tempo di risposta
        avg_delay = area_list[c].queue / num_client_served[c]  # Tempo di attesa in coda

        # Scrive direttamente i valori avg_delay e avg_wait nel file CSV, separando con una virgola
        save_stats_on_file(directory + csv_delay, f"{avg_delay}, ")
        save_stats_on_file(directory + csv_waiting_time, f"{avg_wait}, ")

    save_stats_on_file(directory + csv_delay, "\n")
    save_stats_on_file(directory + csv_waiting_time, "\n")

    # Tempo di fine lavoro, solo per il tipo 'finite'
    if tipo == 'finite':
        save_stats_on_file(directory + CSV_END_WORK_TIME_FINITE, f"{times.current}\n")