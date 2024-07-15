import socket
import threading
import time
from vector_clock import VectorClock
from drift import DriftEvent, manage_drift, update_drift 
import datetime

### O que este código precisa fazer?
## - Enviar vetor para todos os relógios.
## - Receber os vetores de todos os relógios.
## - Atualizar valores máximos no vetor.
## - Verificar se tem alguém com um valor maior e eleger novo líder. -> Como?
##

# Comunicação entre dispositivos - Recebe vetor
def start_server(port, handle_message):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)  # Coloca o socket em escuta
    print(f"Servidor ouvindo na porta {port}...")

    def client_thread(client_socket):
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(f"{datetime.datetime.now().strftime('%H:%M:%S')}: Recebido: {message}")
                received_vector = eval(message)
                local_clock.update(received_vector)  # Atualiza o vetor de relógio local com o recebido
                handle_message(received_vector)  # Passa a mensagem recebida para handle_message
                client_socket.sendall(b'ACK')  # Envia confirmação de recebimento
        except Exception as e:
            print(f"Erro ao receber mensagem: {e}")
            pass
        finally:
            client_socket.close()

    while True:
        client_socket, i = server_socket.accept()  # Aceita conexão do cliente
        print(f"Conexão recebida de {i}")
        # Abre uma thread para cada novo cliente conectado
        threading.Thread(target=client_thread, args=(client_socket,)).start()


# Comunicação entre dispositivos - Envia vetor
# Comunicação entre dispositivos - Envia vetor
def send_message(server_ip, port, message):
    retry_attempts = 10  # Número de tentativas de conexão
    for attempt in range(retry_attempts):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(1)  # Define um tempo limite para a conexão
            client_socket.connect((server_ip, port))
            client_socket.sendall(message.encode())
            ack = client_socket.recv(1024)  # Aguarda confirmação de recebimento
            if ack == b'ACK':
                client_socket.close()
                return  # Se a mensagem foi enviada com sucesso e recebida, sai da função
        except (ConnectionRefusedError, socket.timeout) as e:
            print(f"Erro ao enviar mensagem para {server_ip}:{port} - Tentativa {attempt+1}/{retry_attempts}: {e}")
            time.sleep(1)  # Espera 1 segundo antes de tentar novamente
    print(f"Falha ao conectar com {server_ip}:{port} após {retry_attempts} tentativas")


"""# Eleição do líder (doug)
def elect_leader(vector):
    vector = list(vector)
    leader_index = 0
    leader_value = 0
    for i in range(len(vector)):
        if int(vector[i]) > leader_value:
            leader_value = vector[i]
            leader_index = i
    return leader_index, leader_value
"""

def elect_leader(vectors, active_processes):
    max_vector = None
    leader_index = -1
    for i in active_processes:
        if max_vector is None or vectors[i] > max_vector:
            max_vector = vectors[i]
            leader_index = i
    return leader_index


# Sincronização dos relógios
def synchronize_clocks(leader_vector, follower_clocks):
    for clock in follower_clocks:
        clock.update(leader_vector)

# Código principal
if __name__ == "__main__":
    num_processes = 3  # Exemplo de três processos
    process_id = int(input("Digite o ID deste processo (0, 1, ou 2): "))
    local_clock = VectorClock(num_processes, process_id)
    port = 12345 + process_id

    # Gerenciamento do drift
    drift_event = DriftEvent()
    threading.Thread(target=manage_drift, args=(local_clock, drift_event)).start()
    threading.Thread(target=update_drift, args=(drift_event,)).start()
    
    threading.Thread(target=start_server, args=(port, lambda msg: local_clock.update(msg))).start()
    
    # Enviar vetores periodicamente e executar eleição de líder
    all_clocks_i = [('127.0.0.1', 12345), ('127.0.0.1', 12346), ('127.0.0.1', 12347)]  # Outros relógios

    # controle p vetores e proceso que estão ativos 
    vectors = [None] * num_processes
    active_processes = set(range(num_processes))

    # Envio dos vetores
    while True:
        time.sleep(1)
        vector_str = str(local_clock.get_time())
         # vetor de relógio local com o vetor atual
        vectors[process_id] = local_clock.get_time()

        # aqui eh pra enviar o vetor de relógio para todos os outros processos
        for i in all_clocks_i:
            if i[1] != port:
                print(f"{datetime.datetime.now().strftime('%H:%M:%S')}: Enviando para: {i[0]}, {i[1]}, {vector_str}")
                send_message(i[0], i[1], vector_str)
                time.sleep(1)
        # verificação p ver se todos os vetores foram recebidos
        if all(v is not None for v in vectors):
            ## eleição aqui 
            leader_index = elect_leader(vectors, active_processes)
            print(f"{datetime.datetime.now().strftime('%H:%M:%S')} - Líder: {leader_index}")
            # sincroniza os relógios com o líder
            if process_id == leader_index:
                synchronize_clocks(local_clock, [local_clock])
            else:
                synchronize_clocks(VectorClock(num_processes, leader_index), [local_clock])
