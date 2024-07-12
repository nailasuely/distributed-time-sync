import socket
import threading
import time
from vector_clock import VectorClock
from drift import DriftEvent, manage_drift, update_drift 

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
    server_socket.listen(5) # Coloca o socket em escuta

    def client_thread(client_socket):
        print("inside client_thread")
        message = client_socket.recv(1024).decode()
        print("message:", message)
        # depois daqui falha. os 3 relógios conectados param de processar. 
        # quando o relógio recebe a mensagem, ele não continua incrementando seu contador.
        handle_message(eval(message))
        client_socket.close()
    
    while True:
        print("am i receiving connection?")
        client_socket, addr = server_socket.accept() # Aceita conexão do cliente
        print("yes!")
        # Abre uma thread para cada novo cliente conectado
        threading.Thread(target=client_thread, args=(client_socket,)).start()

# Comunicação entre dispositivos - Envia vetor
def send_message(server_ip, port, message):
    retry_attempts = 10  # Número de tentativas de conexão
    for attempt in range(retry_attempts):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(1)  # Define um tempo limite para a conexão
            client_socket.connect((server_ip, port))
            client_socket.sendall(message.encode())
            client_socket.close()
            return  # Se a mensagem foi enviada com sucesso, sai da função
        except (ConnectionRefusedError, socket.timeout) as e:
            print(f"Erro ao enviar mensagem para {server_ip}:{port} - Tentativa {attempt+1}/{retry_attempts}: {e}")
            time.sleep(1)  # Espera 1 segundo antes de tentar novamente
    print(f"Falha ao conectar com {server_ip}:{port} após {retry_attempts} tentativas")


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
    process_id = int(input("Digite o ID deste processo (0, 1, ou 2): "))
    local_clock = VectorClock(num_processes, process_id)
    port = 12345 + process_id
    print("my port:", port)
    
    # Inicia servidor para receber vetores
    # Atualiza os vetores recebidos no vetor do relógio local caso seja novo máximo
    threading.Thread(target=start_server, args=(port, lambda msg: local_clock.update(msg))).start()
    
    # Gerenciamento do drift
    drift_event = DriftEvent()
    threading.Thread(target=manage_drift, args=(local_clock, drift_event)).start()
    threading.Thread(target=update_drift, args=(drift_event,)).start()
    
    # Enviar vetores periodicamente e executar eleição de líder
    other_clocks = [('127.0.0.1', 12346), ('127.0.0.1', 12347)]  # Outros relógios

    while True:
        time.sleep(2)
        vector_str = str(local_clock.get_time())
        for i in range(len(other_clocks)):
            send_message(other_clocks[i][0], other_clocks[i][1], vector_str)
        
        # Eleição do líder e sincronização
        #other_clocks = [local_clock] + [VectorClock(num_processes, i) for i in range(1, num_processes)]
        #leader = elect_leader(other_clocks)
        #synchronize_clocks(leader, other_clocks)
        #print(f"leader: {leader.get_time()}")
