import threading
import time
import datetime

# Estrutura para armazenar o valor do drift de forma thread-safe
class DriftEvent:
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()

# Gerenciamento do drift e aumento do contador
def manage_drift(clock, drift_event):
    drift = 0  # Inicialmente, sem drift
    while True:
        with drift_event.lock:
            drift = drift_event.value  # Atualiza o drift
        atraso = 1 + drift
        print(f"{datetime.datetime.now().strftime('%H:%M:%S')} - Meu drift value: {drift_event.value}, Aguardando por: {atraso} segundos")
        time.sleep(atraso)  # Tempo de tick ajustado pelo drift
        clock.tick()
        print(f"Vetor do relógio após tick: {clock.vector}")

# Função para atualizar o drift dinamicamente
def update_drift(drift_event):
    while True:
        new_drift = float(input("Digite o valor do drift (em segundos): "))
        with drift_event.lock:
            drift_event.value = new_drift

