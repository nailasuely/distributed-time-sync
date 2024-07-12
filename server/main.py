import socket
import threading
import time
from vector_clock import VectorClock
from drift import DriftEvent, manage_drift, update_drift 

# Comunicação entre dispositivos - Recebe vetor
def start_server(port, handle_message):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5) # Coloca o socket em escuta

    def client_thread(client_socket):
        message = client_socket.recv(1024).decode()
        handle_message(eval(message))
        client_socket.close()
    
    while True:
        client_socket, addr = server_socket.accept() # Aceita conexão do cliente
        # Abre uma thread para cada novo cliente conectado
        threading.Thread(target=client_thread, args=(client_socket,)).start()

# Comunicação entre dispositivos - Envia vetor
def send_message(server_ip, port, message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, port))
    client_socket.sendall(message.encode())
    client_socket.close()

# Eleição do líder
def elect_leader(clocks):
    leader = None
    for clock in clocks:
        if leader is None or clock.get_time() > leader.get_time():
            leader = clock
    return leader

# Sincronização dos relógios
def synchronize_clocks(leader_clock, follower_clocks):
    leader_time = leader_clock.get_time()
    for clock in follower_clocks:
        clock.update(leader_time)

# Código principal
if __name__ == "__main__":
    num_processes = 3  # Exemplo de três processos
    process_id = 0  # ID deste processo
    local_clock = VectorClock(num_processes, process_id)
    port = 12345  # Porta do servidor
    
    # Iniciar servidor para receber vetores
    threading.Thread(target=start_server, args=(port, lambda msg: local_clock.update(msg))).start()
    
    # Gerenciamento do drift
    drift_event = DriftEvent()
    threading.Thread(target=manage_drift, args=(local_clock, drift_event)).start()
    threading.Thread(target=update_drift, args=(drift_event,)).start()
    
    # Enviar vetores periodicamente e executar eleição de líder
    other_devices = [('localhost', 12346), ('localhost', 12347)]  # Exemplo de outros dispositivos
    while True:
        time.sleep(2)
        vector_str = str(local_clock.get_time())
        for device in other_devices:
            send_message(device[0], device[1], vector_str)
        
        # Eleição do líder e sincronização
        other_clocks = [local_clock] + [VectorClock(num_processes, i) for i in range(1, num_processes)]
        leader = elect_leader(other_clocks)
        synchronize_clocks(leader, other_clocks)
        print(f"Líder: {leader.get_time()}")
