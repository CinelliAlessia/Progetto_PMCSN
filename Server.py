class Server:
    def __init__(self, id):
        self.id = id
        self.stato = 'IDLE'
        self.tempo_corrente = 0

    def process_job(self, tempo_arrivo, tempo_servizio):
        # il job servito non era in coda
        if self.tempo_corrente < tempo_arrivo:
            self.tempo_corrente = tempo_arrivo + tempo_servizio
        else:
            self.tempo_corrente += tempo_servizio
        return self.tempo_corrente

    def set_idle(self):
        self.stato = 'IDLE'

    def is_idle(self):
        return self.stato == 'IDLE'

    def update_state(self, current_time):
        if self.tempo_corrente <= current_time:
            self.set_idle()

    def get_current_time(self):
        return self.tempo_corrente