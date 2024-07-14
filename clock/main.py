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

### Problema encontrado:
## Sequência de execução: relógio 0 -> relógio 1 -> relógio 2.
## Vetor 0 consegue incrementar seu índice no vetor.
## Vetor 0 consegue enviar seu vetor para os outros relógios (1 e 2)
## Vetor 1 consegue receber o vetor do relógio 0.
## Vetor 2 consegue receber o vetor do relógio 0.
## Vetor 1 entra no while True na primeira vez. Nas outras, não entra. Fica só recebendo o vetor do relógio 0.
## Vetor 2 entra no while True na primeira vez. Nas outras, não entra. Fica só recebendo o vetor do relógio 0.
## Vetor 1 não incrementa seu índice no seu vetor.
## Vetor 2 não incrementa seu índice no seu vetor.

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
                print(f"Recebido: {message}")
                handle_message(eval(message))  # Passa a mensagem recebida para handle_message
        except Exception as e:
            print(f"Erro ao receber mensagem: {e}")
        finally:
            client_socket.close()

    while True:
        client_socket, addr = server_socket.accept()  # Aceita conexão do cliente
        print(f"Conexão recebida de {addr}")
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

    drift_event = DriftEvent()
    threading.Thread(target=manage_drift, args=(local_clock, drift_event)).start()
    threading.Thread(target=update_drift, args=(drift_event,)).start()
    
    # Inicia servidor para receber vetores.
    # Atualiza os vetores recebidos no vetor do relógio local caso seja novo máximo.
    # Se ele receber a conexão primeiro do que tentar efetuar a conexão, ou seja,
    # se receber o vetor primeiro do que tentar enviar, ele fica só recebendo vetor. 
    # O código todo fica focado nessa thread. 
    # E ele não consegue fazer o gerenciamento do drift e nem fazer o envio dos vetores.
    threading.Thread(target=start_server, args=(port, lambda msg: local_clock.update(msg))).start()
    
    # Gerenciamento do drift
    
    
    # Enviar vetores periodicamente e executar eleição de líder
    other_clocks = [('127.0.0.1', 12346), ('127.0.0.1', 12347)]  # Outros relógios

    # Envio dos vetores
    # O primeiro código a ser executado consegue funcionar. Ele gerencia e atualiza o drift e também envia seus vetores para outros processos.
    while True:
        time.sleep(1)
        vector_str = str(local_clock.get_time())
        for i in range(len(other_clocks)):
            print(f"Enviando para: {other_clocks[i][0]}, {other_clocks[i][1]}, {vector_str}")
            send_message(other_clocks[i][0], other_clocks[i][1], vector_str)
            time.sleep(1)
        
        # Eleição do líder e sincronização
        #other_clocks = [local_clock] + [VectorClock(num_processes, i) for i in range(1, num_processes)]
        #leader = elect_leader(other_clocks)
        #synchronize_clocks(leader, other_clocks)
        #print(f"leader: {leader.get_time()}")


