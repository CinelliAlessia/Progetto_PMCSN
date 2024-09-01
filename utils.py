from libs.rvgs import Uniform
from libs.rvms import idfStudent, cdfNormal, idfNormal
import numpy as np
from Costant import *
from Simulation import times, num_client_in_system, queues, num_client_in_service, num_client_served, accumSum, area_list, num_sampling

# ------------------------------- Funzioni di supporto --------------------------------
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


def format_queues(queues):
    """
    Formatta le code per la stampa di debug
    :param queues:
    :return:
    """
    formatted_queues = []
    for q in queues:
        formatted_queue = [event.event_time for event in q]  # Estrai solo i tempi da ciascun oggetto evento
        formatted_queues.append(formatted_queue)
    return formatted_queues


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


def truncate_normal(mu, sigma, inf, sup):
    """
    Tronca la distribuzione normale tra inf e sup - Lezione 28-05 (numero 31)
    :param mu:
    :param sigma:
    :param inf:
    :param sup:
    :return:
    """
    alpha = cdfNormal(mu, sigma, inf)
    # beta = 1 - cdfNormal(mu, sigma, sup)  # Se siamo interessati a limitare la distribuzione superiormente
    u = Uniform(alpha, 1.0)
    return idfNormal(mu, sigma, u)


def update_acc_sum(service_time, id_s):
    accumSum[id_s].service += service_time
    accumSum[id_s].served += 1


# ------------------------------ Funzioni per la scrittura su file ------------------------------


def save_stats_on_file(file_csv, data):
    """
    Salva le statistiche finali su file CSV.

    :param file_csv: Percorso del file CSV.
    :param data: Dati da scrivere nel file (può essere una stringa formattata CSV).
    :return: None
    """

    # Utilizza il contesto 'with' per assicurare che il file venga chiuso correttamente
    try:
        with open(file_csv, 'a') as csv_file:
            csv_file.write(data)
    except Exception as e:
        print(f"Errore durante la scrittura su file: {e}")


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

# ------------------------------ Funzioni per il calcolo di medie e intervalli ------------------------------
def confidence_interval(alpha, n, l) -> float:
    sigma = np.std(l, ddof=1)
    if n > 1:
        t = idfStudent(n - 1, 1 - alpha / 2)
        return (t * sigma) / np.sqrt(n - 1)
    else:
        return 0.0


def batch_means(data, batch_size):
    n = len(data)
    num_batches = n // batch_size
    batch_means = []

    for i in range(num_batches):
        batch = data[i * batch_size: (i + 1) * batch_size]
        batch_means.append(np.mean(batch))

    return batch_means


def cumulative_mean(data):
    # Computes the cumulative mean for an array of data
    return np.cumsum(data) / np.arange(1, len(data) + 1)