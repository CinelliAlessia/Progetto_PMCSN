# Implementazione di N serventi con due code con priorità
# Coda 1: Vecchi ecc
# Coda 2: Classica
from Costant import *
from Server import Server
from libs.rngs import plantSeeds, selectStream
from libs.rvgs import Exponential

# ------------------- Variabili per definire lo stato del sistema -----------------------

num_client_in_sys = [0 for _ in range(TYPE_CLIENT)]  # Numero di clienti al momento nel sistema per ogni tipo

num_client_in_service = [0 for _ in range(TYPE_CLIENT)]  # Numero di clienti in servizio.

num_client_served = [0 for _ in range(TYPE_CLIENT)]

servant_state = [0 for _ in range(TYPE_CLIENT)]  # Array binario: 0 = IDLE, 1 = BUSY

servers = [Server(i) for i in range(N)]  # Creazione dei serventi

# ---------------------------------------------------------------------------------------

def start():
    arrivals = []
    system_time = 0
    total_queue = [0 for _ in range(TYPE_CLIENT)]

    # Inizio degli arrivi nel sistema
    for i in range(TYPE_CLIENT):
        arrivals.append(generate_arrival_time(i))

    while system_time < TEMPO_SIMULAZIONE or (any(arrivals) is not None):

        # Scelgo il cliente da servire
        serving_arrival_time, index_type = get_next(arrivals)
        if serving_arrival_time is None:
            break

        total_queue[index_type] += serve_client(serving_arrival_time, index_type)

        num_client_served[index_type] += 1  # Aggiorna il numero di clienti totali serviti

        # Inserisce il prossimo arrivo nel sistema
        arrivals[index_type] += generate_arrival_time(index_type)
        if arrivals[index_type] > TEMPO_SIMULAZIONE:
            arrivals[index_type] = None

        # Aggiorna il tempo di sistema
        system_time = serving_arrival_time

    mean_queue_time = sum(total_queue) / sum(num_client_served)
    print(f'Tempo medio in coda di tutte le classi: {mean_queue_time:.2f}')


# Dato l'indice del tipo di cliente, genera il tempo di arrivo
def generate_arrival_time(index_type):
    selectStream(index_type)
    return Exponential(1 / TASSO_ARRIVO[index_type])


# Dato l'indice del tipo di cliente, genera il tempo di servizio
def generate_service_time(index_type):
    selectStream(TYPE_CLIENT + index_type)
    return Exponential(1 / TASSO_SERVIZIO[index_type])


# Ritorna il prossimo evento nell'array che deve essere servito, rispettando le priorità.
# [Type1, Type2] con Type1 = priorità alta, Type2 = priorità bassa
# TODO: se i server sono tutti occupati e arriva prima un giovane e dopo un vecchio,
#  il vecchio deve essere servito prima appena si libera un server.
#  Invece, se arriva prima un giovane e dopo un vecchio, il giovane deve essere servito prima solo se quando
#  lui arriva trova un server libero.
def get_next(array):
    sys_time = get_min_last_time()  # sys_time è il tempo di completamento minore dei server

    # Caso 1: arrivals[0] è minore o uguale di sys_time, c'è qualcuno da servire, servo coda con più prio
    # Caso 2: arrivals[0] è maggiore di sys_time, ergo non è arrivato, vedo prossima coda
    # Caso 3: tutti sono maggiori di sys_time, servirò per primo il valore piu piccolo

    for i in range(TYPE_CLIENT):
        if array[i] is not None and array[i] <= sys_time:
            return array[i], i

    non_none_array = [a for a in array if a is not None]
    if not non_none_array:
        return None, None

    min_time = min(non_none_array)
    return min_time, array.index(min_time)


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
        queue_time = server.get_last_time() - next_arrival
        server.process_job(server.get_last_time(), generate_service_time(index_type))
        return queue_time


def get_min_last_time():
    return min([server.get_last_time() for server in servers])


def main():
    # Inizializzazione del generatore di numeri casuali
    plantSeeds(SEED)
    start()


main()