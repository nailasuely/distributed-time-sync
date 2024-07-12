import threading
import time

# Estrutura para armazenar o valor do drift de forma thread-safe
class DriftEvent:
    def __init__(self):
        # Valor a ser atualizado via inserção do usuário
        self.value = 0
        self.lock = threading.Lock()

# Gerenciamento do drift e aumento do contador
def manage_drift(clock, drift_event):
    drift = 0  # Inicialmente, sem drift
    while True:
        print('estou dentro do manage_drift:', clock.get_time())
        with drift_event.lock:
            drift = drift_event.value  # Atualiza o drift
        time.sleep(1 + drift)  # Tempo de tick ajustado pelo drift
        clock.tick()
        print(clock.vector)

# Função para atualizar o drift dinamicamente
def update_drift(drift_event):
    while True:
        new_drift = float(input("Digite o valor do drift (em segundos): "))
        with drift_event.lock:
            drift_event.value = new_drift

