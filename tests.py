import os
import subprocess
from utils import *


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


def run_create_single_column(file, num_column):
    get_and_write_column_data(file, num_column)
    return file.replace('.csv', f'_column{num_column}.csv')



# Per ogni file che termina con delay.csv, esegue il comando estimate.py
# per calcolare l'intervallo di confidenza della media
for file in os.listdir('finite_horizon/Samp_1000_8H/'):
    if file.endswith('delay.csv'):
        new_file = run_create_single_column(file, 2)
        run_estimate(new_file)


# Esempio di utilizzo
# run_estimate('finite_horizon/rho_ms_1000.csv')
