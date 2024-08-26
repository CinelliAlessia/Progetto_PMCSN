from Simulation import *


def update_state_compl_event(event):
    # Rimuovo un cliente in servizio
    num_client_in_service[event.client_type] -= 1
    # Rimuovo un cliente nel sistema
    num_client_in_system[event.client_type] -= 1
    # Incremento il numero di clienti serviti
    num_client_served[event.client_type] += 1


def add_event_in_service(event):
    num_client_in_service[event.client_type] += 1

