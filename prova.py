from Server import Server
from libs.rngs import putSeed, getSeed, plantSeeds, selectStream
from libs.rvgs import Exponential

# Parametri della simulazione
TEMPO_SIMULAZIONE = 8 * 60  # 8 ore
TASSO_ARRIVO = 0.25
TASSO_SERVIZIO = 0.75

NUM_SERVER = 2

def processing_job(num_job):
    servers = [Server(i) for i in range(NUM_SERVER)]

    file_arrivi = open('tempi_arrivo.txt', 'r', newline="")
    file_arrivi.seek(0)

    file_servizio = open('tempi_servizio.txt', 'r', newline="")
    file_servizio.seek(0)

    for i in range(num_job):
        tempo_arrivo = float(file_arrivi.readline())
        tempo_servizio = float(file_servizio.readline())

        do = True
        while do:
            for j, server in enumerate(servers):
                if server.get_current_time() <= tempo_arrivo:
                    tempo_fine = server.process_job(tempo_arrivo, tempo_servizio)
                    print(f'Fine Servente {server.id}: {tempo_fine:.2f}')
                    do = False
                    break
            if do:
                # Se tutti i server sono occupati, trova il server che si libera prima
                server = min(servers, key=lambda s: s.get_current_time())
                tempo_fine = server.process_job(server.get_current_time(), tempo_servizio)
                print(f'Fine Servente {server.id}: {tempo_fine:.2f}')
                do = False

def generate_arrival_time():
    file_arrivi = open('tempi_arrivo.txt', 'w')
    tempo_corrente = 0
    while tempo_corrente < TEMPO_SIMULAZIONE:
        tempo_arrivo = Exponential(1 / TASSO_ARRIVO)
        tempo_corrente += tempo_arrivo
        if tempo_corrente < TEMPO_SIMULAZIONE:
            file_arrivi.write(f'{tempo_corrente:.2f}\n')
    file_arrivi.close()

def count_jobs():
    with open('tempi_arrivo.txt', 'r', newline="") as file:
        file.seek(0)
        return len(file.readlines())

def generate_service_time():
    file_servizio = open('tempi_servizio.txt', 'w')
    num_job = count_jobs()
    for i in range(num_job):
        tempo_servizio = Exponential(1 / TASSO_SERVIZIO)
        file_servizio.write(f'{tempo_servizio:.2f}\n')
    file_servizio.close()

# Generazione dei tempi di arrivo e di fine servizio
plantSeeds(123456789)
selectStream(0)
generate_arrival_time()

selectStream(1)
generate_service_time()

processing_job(count_jobs())