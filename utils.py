from libs.rvgs import Uniform
from libs.rvms import idfStudent, cdfNormal, idfNormal
import numpy as np

# ------------------------------- Funzioni di supporto --------------------------------


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