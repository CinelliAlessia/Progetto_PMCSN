from math import sqrt
import pandas as pd
from libs.rvgs import Uniform
from libs.rvms import idfStudent, cdfLognormal, idfLognormal, idfNormal, cdfNormal
import numpy as np
import subprocess

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


def truncate_lognormal(mu, sigma, inf):
    """
    Tronca la distribuzione lognormale tra inf e sup.
    Utilizza le funzioni cdfLognormal e idfLognormal.

    :param mu: Media della distribuzione lognormale (riferita al logaritmo dei dati)
    :param sigma: Deviazione standard della distribuzione lognormale (riferita al logaritmo dei dati)
    :param inf: Valore minimo per il troncamento
    :param sup: Valore massimo per il troncamento
    :return: Un campione dalla distribuzione lognormale troncata
    """
    # Calcola la CDF della lognormale a inf e sup
    alpha = cdfLognormal(mu, sigma, inf)

    # Genera un valore uniforme tra alpha e beta
    u = Uniform(alpha, 1)

    # Inversa della CDF (quantile) per ottenere il valore lognormale troncato
    return idfLognormal(mu, sigma, u)


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


def get_and_write_column_data(file_csv, column):
    """
    Estrae i dati di una colonna da un file CSV.
    E li salva in un nuovo file chiamato con nome del file originale + _column + indice della colonna.

    :param file_csv: Percorso del file CSV.
    :param column: Indice della colonna da estrarre.
    :return: None
    """
    new_file = file_csv.replace('.csv', f'_column{column}.csv')

    try:
        with open(file_csv, 'r') as csv_file:
            data = csv_file.readlines()
            column_data = []
            for row in data:
                columns = row.strip().split(',')
                if len(columns) > column:
                    column_data.append(columns[column])
                else:
                    column_data.append('')  # Handle missing columns
    except Exception as e:
        print(f"Errore durante la lettura del file: {e}")
        column_data = []

    try:
        with open(new_file, 'w') as csv_file:
            for value in column_data:
                csv_file.write(f"{value}\n")
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


def format_time(total_minutes):
    # Calculate whole hours
    hours = int(total_minutes // 60)

    # Calculate remaining minutes
    remaining_minutes = total_minutes % 60

    # Extract whole minutes from the remaining minutes
    minutes = int(remaining_minutes)

    # Calculate centiseconds (fractional part of the minute converted to hundredths of a minute)
    centiseconds = (remaining_minutes - minutes) * 100

    # Format the time as HH:MM:CC
    formatted_time = f"{hours:02}:{minutes:02}:{centiseconds:02.0f}"

    return formatted_time


def run_estimate(csv_file):
    # Esegue il comando in shell per chiamare lo script Python estimate.py
    try:
        result = subprocess.run(
            ['python3', 'libs/estimate.py', f'<', csv_file],  # Comando da eseguire
            stdout=subprocess.PIPE,  # Cattura l'output standard
            stderr=subprocess.PIPE,  # Cattura eventuali errori
            text=True  # Decodifica l'output in stringhe
        )

        # Controllo se il comando ha avuto successo
        if result.returncode == 0:
            print(f"Comando eseguito con successo:\n{result.stdout}")
        else:
            print(f"Errore durante l'esecuzione:\n{result.stderr}")

    except Exception as e:
        print(f"Si è verificato un errore: {e}")


def my_estimate(csv_file, column_index):
    LOC = 0.95  # livello di confidenza
    n = 0  # conta i punti dati
    sum = 0.0
    mean = 0.0

    # Leggi il file CSV
    df = pd.read_csv(csv_file, header=None)
    data_column = df.iloc[:, column_index]

    for data in data_column:
        n += 1  # usa il metodo one-pass di Welford
        diff = float(data) - mean  # per calcolare la media campionaria
        sum += diff * diff * (n - 1.0) / n
        mean += diff / n

    stdev = sqrt(sum / n)

    if n > 1:
        u = 1.0 - 0.5 * (1.0 - LOC)  # parametro dell'intervallo
        t = idfStudent(n - 1, u)  # valore critico di t
        w = t * stdev / sqrt(n - 1)  # larghezza dell'intervallo
        print("\nBasato su {0:1d} punti dati e con {1:d}% di confidenza".format(n, int(100.0 * LOC + 0.5)))
        print("Il valore atteso è nell'intervallo {0:10.8f} +/- {1:6.8f}".format(mean, w))
        return mean, w
    else:
        print("ERRORE - dati insufficienti\n")


# Preso un file csv, dell'utilizzazione, calcola la media dei 5 server nel multiserver, creando un nuovo file csv
def calculate_mean_utilization(csv_file):
    # Leggi il file CSV
    df = pd.read_csv(csv_file, header=None)

    # Calcola la media delle colonne 1, 2, 3, 4 e 5
    mean_utilization = df.iloc[:, 1:6].mean(axis=1)

    # Salva la media su un nuovo file
    new_file = csv_file.replace('.csv', '_mean.csv')
    mean_utilization.to_csv(new_file, index=False, header=False)

    return new_file