import numpy as np
from Simulation import truncate_normal
import matplotlib.pyplot as plt
import pandas as pd
import os
from utils import get_and_write_column_data, my_estimate

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

# Esempio di utilizzo con n = 1000
#plot_truncated_normal(mu=15, sigma=3, inf=1e-6, sup=float('inf'), n=1000)
#plot_truncated_lognormal(mu=15, sigma=3, inf=1e-6, n=1000)

def plot_graphs(csv_file, x_label='Time', y_label='Value', title = ''):
    """
    Legge un file CSV e salva i grafici in funzione dell'indice di riga in una cartella specificata.
    Crea un grafico per ogni colonna del file CSV
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


def one_graph_one_plot_for_file(lista_file_csv, colonna, x_label='Tempo di simulazione (minuti)', y_label='E(tq)', title='Confronto tra file', legend = []):
    # Crea un singolo grafico per tutte le curve
    plt.figure(figsize=(10, 6))

    for i, csv_file in enumerate(lista_file_csv):
        # Leggi il file CSV
        df = pd.read_csv(csv_file)

        # Controlla se l'indice della colonna è valido
        if colonna >= len(df.columns):
            print(f"Errore: l'indice di colonna {colonna} è fuori dal range per il file {csv_file}!")
            continue

        # Estrai i dati dalla colonna specificata, prendendo solo due cifre decimali
        dati_colonna = df.iloc[:, colonna].round(2)

        # Crea una lista di numeri per l'asse delle x (numero di riga)
        asse_x = range(len(dati_colonna))

        # Aggiungi la linea al grafico, con etichetta basata sul nome del file
        plt.plot(asse_x, dati_colonna, label=f'{legend[i]}', linewidth=0.5)

        # Aggiungi un puntino per ogni valore
        plt.scatter(asse_x, dati_colonna, s=10)  # s è la dimensione del puntino

    # Configura gli assi
    plt.xlabel(x_label, fontsize=14)
    plt.ylabel(y_label, fontsize=14)

    # Aumenta la dimensione del font dei numeri sugli assi x e y
    plt.tick_params(axis='x', labelsize=14)
    plt.tick_params(axis='y', labelsize=14)

    # Mostra solo una label ogni 20 valori sull'asse x
    max_x = max(len(pd.read_csv(f)) for f in lista_file_csv)  # Trova la lunghezza massima tra i file
    # Calcolo dei tick includendo l'ultimo valore
    ticks = np.arange(0, max_x, 20)

    # Aggiungi l'ultimo tick se non è già incluso
    if max_x % 20 != 0:
        ticks = np.append(ticks, max_x+1)

    # Imposta i tick e le etichette
    #plt.xticks(ticks=ticks, labels=ticks)

    # Mostra griglia per l'asse y
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)

    # Aggiungi un titolo unico per il grafico
    plt.title(title, fontsize=14)

    # Mostra la legenda con i parametri passati come argomento
    plt.legend(legend)

    # Mostra il grafico
    plt.show()

def plot_multiple_blocks(file_list, num_sample, x_label, y_label, title, legend_labels, y_column_index):
    plt.figure(figsize=(10, 6))  # Inizializza un'unica figura per il grafico finale

    for file_idx, file in enumerate(file_list):
        # Carica il file CSV senza header
        df = pd.read_csv(file, header=None)

        # Stampa per controllare quante righe ha il file CSV
        print(f"Il file {file} contiene {len(df)} righe.")

        # Utilizza la colonna specificata da y_column_index per l'asse Y
        y_values = df.iloc[:, y_column_index]  # Colonna specificata per Y

        # Conta il numero di blocchi
        num_blocks = len(df) // num_sample  # Arrotonda in alto per considerare eventuali righe rimanenti
        print(f"Numero di blocchi per il file {file}: {num_blocks}")

        # Assicurati che la lunghezza di `legend_labels` corrisponda al numero di blocchi
        if len(legend_labels) < num_blocks:
            raise ValueError(f"La lista dei nomi nella legenda deve contenere almeno {num_blocks} elementi, ma ne ha {len(legend_labels)}.")

        # Aggiungi un plot per ogni blocco di `num_sample` righe
        for i in range(num_blocks):
            # Calcola gli indici per il blocco corrente
            start_idx = i * num_sample
            end_idx = min((i + 1) * num_sample, len(df))  # Assicura di non andare oltre l'ultima riga

            # Genera l'indice per l'asse X, che deve ripartire da 0 a num_sample per ogni blocco
            x_block = range(0, end_idx - start_idx)
            y_block = y_values[start_idx:end_idx]

            # Aggiungi il plot per il blocco corrente e usa i nomi dalla lista legend_labels
            plt.plot(x_block, y_block, label=legend_labels[i])

        # Imposta etichette e titolo con font size più grande
        plt.xlabel(x_label, fontsize=16)
        plt.ylabel(y_label, fontsize=16)
        plt.title(title, fontsize=16)

        # Imposta una griglia con linee sull'asse X ogni 5 valori
        plt.xticks(range(0, num_sample + 1, 20))  # Setta i tick ogni 5 unità sull'asse X
        plt.grid(True, which='both', axis='x', linestyle='--', linewidth=0.7)

        # Aumenta la dimensione del font dei numeri sugli assi x e y
        plt.tick_params(axis='x', labelsize=18)
        plt.tick_params(axis='y', labelsize=18)

        # Aumenta la dimensione della legenda
        plt.legend(fontsize=14)
    # Mostra il grafico
    plt.show()

# Chiamate delle funzioni
# plot_graphs("./infinite_horizon/utilization.csv")
#one_graph_one_plot_for_file(["finite_horizon/delay.csv"],2, 'Tempo di simulazione (minuti)', 'E(Tq3)', f'123456789')

DIR = "finite_horizon/Lambda_orig/"
list = [f"{DIR}123456789_S1/delay.csv",f"{DIR}1054618708_S1/delay.csv",f"{DIR}1675617763_S1/delay.csv"]
legend = ['123456789','1054618708', '1675617763']

list = ["finite_horizon/Lambda_orig/123456789_S1/delay.csv", "finite_horizon/Lambda_min/123456789_S1/delay.csv","finite_horizon/Lambda_max/123456789_S1/delay.csv" ]
legend = ['Lambda = 1/(1.5)','Lambda = 1/3', 'Lambda = 1']

# one_graph_one_plot_for_file(list,2,'Tempo di simulazione (minuti)', 'E(Tq3)', 'seed = 123456789', legend)
ANDREA = False
if ANDREA:
    legend_labels = ['123456789', '1054618708', '1675617763', '1884610308','1677438794']  # Nomi per la legenda
    for i in range(8):
        plot_multiple_blocks(
            ["finite_horizon/pop_queue.csv"],
            240,  # 240 righe per blocco
            'Tempo di simulazione (minuti)',  # Etichetta per asse X
            f'E[Nq{i+1}]',  # Etichetta per asse Y
            f'Coda {i+1}',  # Titolo del grafico
            legend_labels,  # Etichette per la legenda
            y_column_index=i  # Indice della colonna da usare per Y
        )



def plt_end_time(file_csv, end_time, qos_max, mean_csv, conf_interval):
    """
    Crea un grafico dell'ultimo tempo di completamento per ogni replica.
    :param file_csv: Il file CSV contenente i tempi di completamento.
    :param end_time: Il tempo di completamento target.
    :param qos_max: Il tempo massimo di completamento.
    :param mean_csv: La media dei tempi di completamento.
    :param conf_interval: L'intervallo di confidenza.
    """
    # Leggi il file CSV in un DataFrame
    df = pd.read_csv(file_csv, header=None)

    # Plotta ciascun valore letto
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df, label='Tempo di completamento')
    plt.axhline(y=end_time, color='r', linestyle='--', label='End Time Target')
    plt.axhline(y=qos_max, color='b', linestyle='--', label='Goal')
    plt.axhline(y=mean_csv, color='g', linestyle='--', label='Mean')

    # Aggiungi bande di errore per l'intervallo di confidenza
    # plt.fill_between(df.index, mean_csv - conf_interval, mean_csv + conf_interval, color='yellow', alpha=0.5, label='Confidence Interval')

    # Etichette degli assi
    plt.xlabel('Replica', fontsize=16)
    plt.ylabel('Tempo di completamento', fontsize=16)

    # Aumenta la dimensione del font dei numeri sugli assi x e y
    plt.tick_params(axis='x', labelsize=18)
    plt.tick_params(axis='y', labelsize=18)

    plt.title('Tempo di Completamento per Replica, n = 1000', fontsize=16)
    plt.legend()
    plt.grid(True)
    plt.show()


PLOT_END_TIME = False
if PLOT_END_TIME:
    mean_FF, conf_interval_FF = my_estimate('finite_horizon/1000_F_F_4H/end_work_time_finite.csv', 0)
    mean_TF, conf_interval_TF = my_estimate('finite_horizon/1000_T_F_4H/end_work_time_finite.csv', 0)
    mean_TT, conf_interval_TT = my_estimate('finite_horizon/1000_T_T_4H/end_work_time_finite.csv', 0)

    plt_end_time('finite_horizon/1000_F_F_4H/end_work_time_finite.csv', 240, 240+30, mean_FF, conf_interval_FF)
    plt_end_time('finite_horizon/1000_T_F_4H/end_work_time_finite.csv', 240, 240+30, mean_TF, conf_interval_TF)
    plt_end_time('finite_horizon/1000_T_T_4H/end_work_time_finite.csv', 240, 240+30, mean_TT, conf_interval_TT)


def plt_mean_for_more_files(end_name_csv, index_column, dir, sampling_rate, max_rate, title='Mean for different Sampling Rate', ylabel='Mean'):
    actual_sampling = sampling_rate

    data = [0]
    conf_data = [0]
    while actual_sampling <= max_rate:
        current_file = str(actual_sampling) + end_name_csv
        actual_sampling += sampling_rate

        mean, conf_interval = my_estimate(dir + current_file, index_column)
        data.append(mean)
        conf_data.append(conf_interval)

    # Plotta ciascun valore letto
    plt.figure(figsize=(10, 6))

    # Create the x values to match the length of data
    x_values = range(0, max_rate + sampling_rate, sampling_rate)

    # Ensure x_values and data have the same length
    if len(x_values) != len(data):
        raise ValueError(f"x and y must have same first dimension, but have shapes {len(x_values)} and {len(data)}")

    # Plot each value read
    plt.figure(figsize=(10, 6))
    plt.plot(x_values, data, label='Media')
    plt.fill_between(x_values, np.array(data) - np.array(conf_data), np.array(data) + np.array(conf_data), color='g', alpha=0.2, label='Intervallo di confidenza')
    grid_color = plt.rcParams['grid.color']
    plt.axhline(y=0, color=grid_color, linestyle='-')
    plt.axvline(x=240, color='r', linestyle='--', label='4 Ore')

    plt.xlabel('Tempo di simulazione (minuti)', fontsize=16)
    plt.ylabel(ylabel, fontsize=16)
    plt.title(title, fontsize=16)
    plt.legend(fontsize=14)
    plt.grid(True)

    plt.tick_params(axis='x', labelsize=18)
    plt.tick_params(axis='y', labelsize=18)

    plt.show()


PLOT_MEAN = False
if PLOT_MEAN:
    #for i in range(9):
    i = 2
    plt_mean_for_more_files('delay.csv', i, 'finite_horizon/', 1000 , 600000, f'Tempo medio in coda {i+1}', f'Tempo in coda (minuti)')
        # plt_mean_for_more_files('utilization.csv', i, 'finite_horizon/Samp_1000_4H/TF_S1/', 1, 240, f'Popolazione in coda {i+1}', 'Numero di persone')

PLOT_MEAN_UTIL = False
if PLOT_MEAN_UTIL:
    pass

INF_HORIZON = False
if INF_HORIZON:
    output_dir = 'infinite_horizon/512_1024_TT/'
    one_graph_one_plot_for_file([output_dir+"delay.csv"], 2, 'Num. di Batch', 'Tempo in coda', f'Tempo medio in coda 3', ['Tempo in coda'])
    one_graph_one_plot_for_file([output_dir+"delay.csv"], 5, 'Num. di Batch', 'Tempo in coda', 'Tempo medio in coda 6', ['Tempo in coda'])
    one_graph_one_plot_for_file([output_dir+"delay.csv"], 7, 'Num. di Batch', 'Tempo in coda', 'Tempo medio in coda 8', ['Tempo in coda'])
other = False
if other:
    one_graph_one_plot_for_file(["infinite_horizon/512_1024_FF/delay.csv"], 5, 'Num. di Batch', 'Tempo in coda', 'Tempo medio in coda 6', ['Tempo in coda'])
    one_graph_one_plot_for_file(["infinite_horizon/512_1024_FF/delay.csv"], 7, 'Num. di Batch', 'Tempo in coda', 'Tempo medio in coda 8', ['Tempo in coda'])

    one_graph_one_plot_for_file(["infinite_horizon/512_1024_TF/delay.csv"], 2, 'Num. di Batch', 'Tempo in coda', f'Tempo medio in coda 3', ['Tempo in coda'])
    one_graph_one_plot_for_file(["infinite_horizon/512_1024_TF/delay.csv"], 5, 'Num. di Batch', 'Tempo in coda', 'Tempo medio in coda 6', ['Tempo in coda'])
    one_graph_one_plot_for_file(["infinite_horizon/512_1024_TF/delay.csv"], 7, 'Num. di Batch', 'Tempo in coda', 'Tempo medio in coda 8', ['Tempo in coda'])

    one_graph_one_plot_for_file(["infinite_horizon/512_1024_TT/delay.csv"], 2, 'Num. di Batch', 'Tempo in coda', f'Tempo medio in coda 3', ['Tempo in coda'])
    one_graph_one_plot_for_file(["infinite_horizon/512_1024_TT/delay.csv"], 5, 'Num. di Batch', 'Tempo in coda', 'Tempo medio in coda 6', ['Tempo in coda'])
    one_graph_one_plot_for_file(["infinite_horizon/512_1024_TT/delay.csv"], 7, 'Num. di Batch', 'Tempo in coda', 'Tempo medio in coda 8', ['Tempo in coda'])
    one_graph_one_plot_for_file(["infinite_horizon/512_1024_TT/delay.csv"], 8, 'Num. di Batch', 'Tempo in coda', 'Tempo medio in coda 9', ['Tempo in coda'])


def utilization_multiserver(input_csv, output_csv):
    # Leggi il file CSV originale
    df = pd.read_csv(input_csv, header=None)

    # Inizializza una lista per le medie
    means = []

    # Itera su ogni riga del DataFrame
    for index, row in df.iterrows():
        # Estrai le prime cinque colonne
        values = row.iloc[:5].values

        # Crea un file CSV temporaneo per la riga corrente con i valori in colonna
        temp_csv = 'temp_row.csv'
        # Converti i valori in un DataFrame e salvali come file CSV in una sola colonna
        for value in values:
            pd.DataFrame([value]).to_csv(temp_csv, mode='a', index=False, header=False)

        # Calcola la media usando my_estimate
        mean, _ = my_estimate(temp_csv, 0)
        means.append(mean)

        # Rimuovi il file CSV temporaneo
        os.remove(temp_csv)

    # Aggiungi le medie come nuova colonna al DataFrame
    df['mean'] = means

    # Scrivi le medie in un nuovo file CSV
    df[['mean']].to_csv(output_csv, index=False, header=False)


UTILIZATION_MULTISERVER = True
if UTILIZATION_MULTISERVER:

    input_csv = 'finite_horizon/Samp_1000_4H/FF_S20/240utilization.csv'
    output_csv = 'finite_horizon/Samp_1000_4H/FF_S20/240utilizationMULTI_FF.csv'
    utilization_multiserver(input_csv, output_csv)

    # Utilizza la funzione my_estimate sul nuovo file CSV
    mean, conf_interval = my_estimate(output_csv, 0)
    print(f'Mean MFF: {mean}, Confidence Interval: {conf_interval}')

    input_csv = 'finite_horizon/Samp_1000_4H/TF_S20/240utilization.csv'
    output_csv = 'finite_horizon/Samp_1000_4H/TF_S20/240utilizationMULTI_TF.csv'
    utilization_multiserver(input_csv, output_csv)

    # Utilizza la funzione my_estimate sul nuovo file CSV
    mean, conf_interval = my_estimate(output_csv, 0)
    print(f'Mean MTF: {mean}, Confidence Interval: {conf_interval}')

    input_csv = 'finite_horizon/Samp_1000_4H/TT_S20/240utilization.csv'
    output_csv = 'finite_horizon/Samp_1000_4H/TT_S20/240utilizationMULTI_TT.csv'
    utilization_multiserver(input_csv, output_csv)

    # Utilizza la funzione my_estimate sul nuovo file CSV
    mean, conf_interval = my_estimate(output_csv, 0)
    print(f'Mean MTF: {mean}, Confidence Interval: {conf_interval}')

    output_csv = 'finite_horizon/Samp_1000_4H/FF_S20/240utilization.csv'
    mean, conf_interval = my_estimate(output_csv, 5)
    print(f'Mean 5 FF: {mean}, Confidence Interval: {conf_interval}')
    mean, conf_interval = my_estimate(output_csv, 6)
    print(f'Mean 6 FF: {mean}, Confidence Interval: {conf_interval}')

    output_csv = 'finite_horizon/Samp_1000_4H/TF_S20/240utilization.csv'
    mean, conf_interval = my_estimate(output_csv, 5)
    print(f'Mean 5 TF: {mean}, Confidence Interval: {conf_interval}')
    mean, conf_interval = my_estimate(output_csv, 6)
    print(f'Mean 6 TF: {mean}, Confidence Interval: {conf_interval}')

    output_csv = 'finite_horizon/Samp_1000_4H/TT_S20/240utilization.csv'
    # Utilizza la funzione my_estimate sul nuovo file CSV
    mean, conf_interval = my_estimate(output_csv, 5)
    print(f'Mean 5 TT: {mean}, Confidence Interval: {conf_interval}')
    mean, conf_interval = my_estimate(output_csv, 6)
    print(f'Mean 6 TT: {mean}, Confidence Interval: {conf_interval}')
    mean, conf_interval = my_estimate(output_csv, 7)
    print(f'Mean 7 TT: {mean}, Confidence Interval: {conf_interval}')