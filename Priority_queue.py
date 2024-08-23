# Implementazione di N serventi con due code con priorità
# Coda 1: Vecchi ecc
# Coda 2: Classica
from Costant import *
from Server import Server
from Simulation import generate_arrival_time
from libs.rngs import plantSeeds, selectStream
from libs.rvgs import Exponential

# ------------------- Variabili per definire lo stato del sistema -----------------------

num_client_in_sys = [0 for _ in range(QUEUES_NUM)]  # Numero di clienti al momento nel sistema per ogni tipo

num_client_in_service = [0 for _ in range(QUEUES_NUM)]  # Numero di clienti in servizio.

num_client_served = [0 for _ in range(QUEUES_NUM)]

servant_state = [0 for _ in range(QUEUES_NUM)]  # Array binario: 0 = IDLE, 1 = BUSY

servers = [Server(i) for i in range(N)]  # Creazione dei serventi

# ---------------------------------------------------------------------------------------

def start():
    arrivals = []
    system_time = 0
    total_queue = [0 for _ in range(QUEUES_NUM)]

    # Inizio degli arrivi nel sistema
    for i in range(QUEUES_NUM):
        arrivals.append(generate_arrival_time(i))

    while system_time < TEMPO_SIMULAZIONE or (any(arrivals) is not None):

        # Schedulo il prossimo cliente da servire
        in_serving_arrival_time, index_type = get_next(arrivals)
        if in_serving_arrival_time is None:
            break

        total_queue[index_type] += serve_client(in_serving_arrival_time, index_type)

        num_client_served[index_type] += 1  # Aggiorna il numero di clienti totali serviti

        # Inserisce il prossimo arrivo nel sistema
        arrivals[index_type] += generate_arrival_time(index_type)
        if arrivals[index_type] > TEMPO_SIMULAZIONE:
            arrivals[index_type] = None

        # Aggiorna il tempo di sistema
        system_time = get_max_last_time()

    mean_queue_time = sum(total_queue) / sum(num_client_served)
    print(f'Tempo medio in coda di tutte le classi: {mean_queue_time:.2f}')




# Ritorna il prossimo evento nell'array che deve essere servito, rispettando le priorità.
# [Type1, Type2] con Type1 = priorità alta, Type2 = priorità bassa
# TODO: se i server sono tutti occupati e arriva prima un giovane e dopo un vecchio,
#  il vecchio deve essere servito prima appena si libera un server.
#  Invece, se arriva prima un giovane e dopo un vecchio, il giovane deve essere servito prima solo se quando
#  lui arriva trova un server libero.
def get_next(arrivals):
    last_serving_time = get_min_last_time()  # è il tempo di completamento minore dei server

    # Caso 1: arrivals[i] è minore o uguale di last_serving_time, c'è qualcuno da servire, servo coda con più prio
    # Caso 2: arrivals[0] è maggiore di last_serving_time, ergo non è arrivato, vedo prossima coda
    # Caso 3: tutti sono maggiori di sys_time, servirò per primo il valore piu piccolo

    # Caso 1 e 2:
    for i in range(QUEUES_NUM):
        # Se il tempo di arrivo è maggiore o uguale al tempo di completamento minore tra i server
        # Equivale a dire che il cliente quando arriva trova un server libero
        if arrivals[i] is not None and arrivals[i] <= last_serving_time:
            # Può essere servito subito
            return arrivals[i], i

    # Caso 3:
    non_none_array = [a for a in arrivals if a is not None] # Creo un nuovo array con solo i valori non None
    if not non_none_array:
        return None, None

    min_time = min(non_none_array)
    return min_time, arrivals.index(min_time)


# Assegnazione del cliente a un server per servirlo
def serve_client(next_arrival, index_type):
    # Scelta del server a cui associare la richiesta
    for server in servers:
        if server.get_last_time() <= next_arrival:  # Caso in cui il server è libero all'arrivo del cliente
            server.process_job(next_arrival, generate_service_time(index_type))
            return 0
    else:
        # Se tutti i server sono occupati, il job va al primo server che si libera
        server = min(servers, key=lambda s: s.get_last_time())
        server.process_job(next_arrival, generate_service_time(index_type))
        queue_time = server.get_last_time() - next_arrival
        return queue_time


# Restituisci il minimo tempo di completamento tra i server
def get_min_last_time():
    return min([server.get_last_time() for server in servers])


# Ritorna il massimo tempo di completamento tra i server
def get_max_last_time():
    return max([server.get_last_time() for server in servers])


def main():
    # Inizializzazione del generatore di numeri casuali
    plantSeeds(SEED)
    start()


main()