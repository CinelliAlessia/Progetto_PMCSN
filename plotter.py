import os
from matplotlib import pyplot as plt
from Simulation import truncate_normal
import matplotlib.pyplot as plt
import pandas as pd
import os

from utils import truncate_lognormal

output_dir = "./output_plots"


def plot_truncated_normal(mu, sigma, inf, sup, n=1000):
    """Genera un grafico della distribuzione di probabilità usando la funzione truncate_normal."""
    samples = [truncate_normal(mu, sigma, inf, sup) for _ in range(n)]

    plt.figure(figsize=(10, 6))
    plt.hist(samples, bins=50, density=True, alpha=0.6, color='g', label='Campioni')

    plt.title(f'Distribuzione Normale Troncata (media={mu}, sigma={sigma})')
    plt.xlabel('Valori')
    plt.ylabel('Densità di probabilità')
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_truncated_lognormal(mu, sigma, inf, n=10000):
    """
    Genera un grafico della distribuzione lognormale troncata usando la funzione truncate_lognormal.
    :param mu: Media della distribuzione lognormale (riferita al logaritmo dei dati)
    :param sigma: Deviazione standard della distribuzione lognormale (riferita al logaritmo dei dati)
    :param inf: Valore minimo per il troncamento
    :param sup: Valore massimo per il troncamento
    :param n: Numero di campioni da generare
    """
    # Genera i campioni troncati
    samples = [truncate_lognormal(mu, sigma, inf) for _ in range(n)]

    plt.figure(figsize=(10, 6))
    plt.hist(samples, bins=50, density=True, alpha=0.6, color='g', label='Campioni')

    plt.title(f'Distribuzione LogNormale Troncata (media={mu}, sigma={sigma})')
    plt.xlabel('Valori')
    plt.ylabel('Densità di probabilità')
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_cumulative_means(cumulative_means, stationary_value, ylabel, title, filename):
    plt.figure(figsize=(10, 6))
    plt.plot(cumulative_means, label=ylabel)
    plt.xlabel('Batch Number')

    # Plot a horizontal line for the stationary value
    plt.axhline(stationary_value, color='orange', label='Mean of means')

    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid(True)

    # Create folder 'plots' if it doesn't exist
    if not os.path.exists('plots'):
        os.makedirs('plots')

    # Save plots
    plt.savefig(f'plots/{filename}.png')
    plt.close()


def plot_graphs(csv_file, x_label='Time', y_label='Value', title = ''):
    """
    Legge un file CSV e salva i grafici in funzione dell'indice di riga in una cartella specificata.

    :param title:
    :param x_label:
    :param y_label:
    :param csv_file: Percorso del file CSV.
    :param output_dir: Cartella di output per i grafici.
    """
    try:
        # Leggi il file CSV in un DataFrame
        df = pd.read_csv(csv_file, header=None)
        print(f"File {csv_file} letto correttamente. Colonne trovate: {df.columns}")

        # Usa l'indice del DataFrame come asse x
        time = df.index

        # Estrai il nome del file CSV senza estensione
        file_name = os.path.splitext(os.path.basename(csv_file))[0]

        # Crea la cartella di output se non esiste
        os.makedirs(output_dir, exist_ok=True)

        # Crea un grafico per ogni colonna
        for column in df.columns:
            plt.figure()
            plt.plot(time, df[column])
            plt.xlabel(x_label)
            plt.ylabel(y_label)
            plt.title(title)
            plt.legend()
            plt.grid(True)
            output_file = os.path.join(output_dir, f'{file_name}_colonna_{column}_plot.png')
            plt.savefig(output_file)  # Salva il grafico come file PNG
            print(f"Grafico salvato come {output_file}")

            plt.show()
            plt.close()  # Chiudi la figura per liberare memoria
    except Exception as e:
        print(f"Errore durante la lettura del file o la creazione dei grafici: {e}")


def one_graph_one_plot_for_file(lista_file_csv, colonna, x_label='Tempo di simulazione (minuti)', y_label='E(tq)', title='Confronto tra file'):
    # Crea un singolo grafico per tutte le curve
    plt.figure(figsize=(10, 6))

    for csv_file in lista_file_csv:
        # Leggi il file CSV
        df = pd.read_csv(csv_file)

        # Controlla se l'indice della colonna è valido
        if colonna >= len(df.columns):
            print(f"Errore: l'indice di colonna {colonna} è fuori dal range per il file {csv_file}!")
            continue

        # Estrai i dati dalla colonna specificata
        dati_colonna = df.iloc[:, colonna]

        # Crea una lista di numeri per l'asse delle x (numero di riga)
        asse_x = range(len(dati_colonna))

        # Aggiungi la linea al grafico, con etichetta basata sul nome del file
        plt.plot(asse_x, dati_colonna, label=f'{csv_file.split("/")[-1]}: Colonna {df.columns[colonna]}')

    # Configura gli assi
    plt.xlabel(x_label, fontsize=12)
    plt.ylabel(y_label, fontsize=12)

    # Mostra solo una label ogni 20 valori sull'asse x
    max_x = max(len(pd.read_csv(f)) for f in lista_file_csv)  # Trova la lunghezza massima tra i file
    plt.xticks(ticks=range(0, max_x, 20), labels=range(0, max_x, 20))

    # Mostra griglia per l'asse y
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)

    # Aggiungi un titolo unico per il grafico
    plt.title(title, fontsize=14)

    # Mostra la legenda con i nomi dei file
    plt.legend()

    # Mostra il grafico
    plt.show()


# Chiamate delle funzioni
# plot_graphs("./infinite_horizon/utilization.csv")
#one_graph_one_plot_for_file(["finite_horizon/delay123456789.csv","finite_horizon/delay1359796324.csv","finite_horizon/delay.csv"],6, 'Tempo di simulazione (minuti)', 'E(tq)', f'Grafico della colonna 2')


# Esempio di utilizzo con n = 1000
plot_truncated_normal(mu=15, sigma=3, inf=1e-6, sup=float('inf'), n=1000)
plot_truncated_lognormal(mu=15, sigma=3, inf=1e-6, n=1000)

