import threading
import time 

class VectorClock:
    def __init__(self, num_processes, process_id):
        # Lista inicializada com 0s
        self.vector = [0] * num_processes 
        # Identifica a posição no vetor que representa o tempo deste processo
        self.process_id = process_id
        # Evita condições de corrida quando vários threads acessam e modificam o vetor
        self.lock = threading.Lock()
    
    # Incrementa o valor da posição deste processo no vetor
    def tick(self):
        print(f"Meu valor: {self.vector[self.process_id]} - {self.vector}")
        self.vector[self.process_id] += 1
    
    # Atualiza o vetor do processo com base em um vetor recebido de outro processo
    """def update(self, received_vector):
        with self.lock:
            for i in range(len(self.vector)):
                if self.vector[i] < received_vector[i]:
                    self.vector[i] = received_vector[i]
    """

    def update(self, received_vector):
        with self.lock:
            for i in range(len(self.vector)):
                self.vector[i] = max(self.vector[i], received_vector[i])

    def get_time(self):
        with self.lock:
            # Retorna uma cópia do vetor
            return self.vector[:]
    
    def __str__(self):
        with self.lock:
            return str(self.vector)