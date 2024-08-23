class Server:
    def __init__(self, id):
        self.id = id
        self.state = 'IDLE'
        self.last_compl_time = 0  # Tempo dell'ultimo completamento

    def process_job(self, tempo_arrivo, tempo_servizio):
        # il job servito non era in coda
        if self.last_compl_time < tempo_arrivo:
            self.last_compl_time = tempo_arrivo + tempo_servizio
        else:
            self.last_compl_time += tempo_servizio
        return self.last_compl_time

    def set_idle(self):
        self.state = 'IDLE'

    def is_idle(self):
        return self.state == 'IDLE'

    def set_busy(self):
        self.state = 'BUSY'

    def is_busy(self):
        return self.state == 'BUSY'

    def get_last_time(self):
        return self.last_compl_time
