import socket
import threading
import time
from vector_clock import VectorClock
from drift import DriftEvent, manage_drift, update_drift 
import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

# Comunicação entre dispositivos - Recebe vetor
def start_server(port, handle_message):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)  # Coloca o socket em escuta

    def client_thread(client_socket):
        try:
            message = client_socket.recv(1024).decode()
            if message:
                handle_message(eval(message))  # Passa a mensagem recebida para handle_message
        except Exception as e:
            print(f"Erro ao receber mensagem: {e}")
            pass
        finally:
            client_socket.close()

    while True:
        client_socket, addr = server_socket.accept()  # Aceita conexão do cliente
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


@app.route('/leader', methods=['GET'])
def get_leader():
    vector = local_clock.get_time()
    leader_index, leader_value = elect_leader(vector)
    return jsonify({
        'leader_index': leader_index,
        'leader_value': leader_value
    })

"""@app.route('/drift', methods=['POST'])
def update_drift_route():
    data = request.json
    drift_value = data.get('drift_value')
    if drift_value is not None:
        drift_event.set_drift(drift_value)
        return jsonify({'message': 'Drift atualizado com sucesso', 'drift_value': drift_value})
    else:
        return jsonify({'error': 'drift_value é necessário'}), 400"""

# Eleição do líder
def elect_leader(vector):
    vector = list(vector)
    leader_index = 0
    leader_value = 0
    for i in range(len(vector)):
        if int(vector[i]) > leader_value:
            leader_value = vector[i]
            leader_index = i
    return leader_index, leader_value

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
    #all_clocks_addr = [('172.16.103.13', 12355), ('172.16.103.14', 12356), ('172.16.103.12', 12357)]
    all_clocks_addr =[('127.0.0.1', 12345), ('127.0.0.1', 12346), ('127.0.0.1', 12347)]
    app.run(host='0.0.0.0', port=5030 + process_id, debug=False, use_reloader=False)

    # Envio dos vetores
    # O primeiro código a ser executado consegue funcionar. Ele gerencia e atualiza o drift e também envia seus vetores para outros processos.
    while True:
        time.sleep(1)
        vector_str = str(local_clock.get_time())
        #print(vector_str)
        for i in range(len(all_clocks_addr)):
            if all_clocks_addr[i][1] != port:
                send_message(all_clocks_addr[i][0], all_clocks_addr[i][1], vector_str)
            
        # Eleição do líder e sincronização
        leader_index, leader_value = elect_leader(local_clock.get_time())
        print(datetime.datetime.now().strftime('%H:%M:%S'), "- Líder: ", leader_index, leader_value)
        


