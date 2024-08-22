from Costant import N, TASSO_SERVIZIO, TEMPO_SIMULAZIONE, TASSO_ARRIVO, SEED
from Server import Server
from libs.rngs import plantSeeds, selectStream
from libs.rvgs import Exponential


def processing_job(num_job):
    servers = [Server(i) for i in range(N)]
    total_queue_time = 0  # Variabile per il tempo totale in coda

    file_arrivi = open('tempi_arrivo.txt', 'r', newline="")
    file_arrivi.seek(0)

    for i in range(num_job):

        tempo_arrivo = float(file_arrivi.readline())
        selectStream(1)
        tempo_servizio = Exponential(1 / TASSO_SERVIZIO)

        do = True
        while do:
            for j, server in enumerate(servers):
                if server.get_last_time() <= tempo_arrivo:
                    # BUSY
                    tempo_fine = server.process_job(tempo_arrivo, tempo_servizio)
                    print(f'Fine Servente {server.id}: {tempo_fine:.2f}')
                    # IDLE
                    do = False
                    break
            if do:
                # Se tutti i server sono occupati, trova il server che si libera prima
                server = min(servers, key=lambda s: s.get_last_time())
                queue_time = server.get_last_time() - tempo_arrivo
                total_queue_time += queue_time  # Aggiungi il tempo in coda
                tempo_fine = server.process_job(server.get_last_time(), tempo_servizio)
                print(f'Fine Servente {server.id}: {tempo_fine:.2f}')
                do = False

            # Calcola il tempo medio in coda
            average_queue_time = total_queue_time / num_job
            print(f'Tempo medio in coda: {average_queue_time:.2f}')


def generate_arrival_time():
    selectStream(0)
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


# Generazione dei tempi di arrivo e di fine servizio
plantSeeds(SEED)
generate_arrival_time()
processing_job(count_jobs())
