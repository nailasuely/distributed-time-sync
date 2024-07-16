# Sincronização de Relógios em Ambientes Distribuídos

## Descrição do Projeto

O projeto implementa um sistema de sincronização de relógios em ambientes distribuídos utilizando relógios vetoriais. A solução é voltada para computadores conectados na mesma rede, permitindo que dispositivos se comuniquem entre si para ajustar seus relógios, que podem apresentar deriva (drift). O sistema se organiza em torno da ideia de que o dispositivo com o maior tempo se torna o líder e sincroniza os demais.

## Funcionalidades

- **Relógio Vetorial:** Implementa um mecanismo para manter a ordem de eventos em sistemas distribuídos.
- **Comunicação entre Processos:** Usa sockets para enviar e receber atualizações de relógio entre dispositivos.
- **Eleições de Líder:** O dispositivo com maior tempo se torna o novo líder, promovendo a sincronização dos relógios.
- **Drift Manual:** Permite a inserção manual de drift em cada dispositivo para simulações e testes.

## Estrutura do Código

O projeto é estruturado em três arquivos principais:

1. **`main.py`**: Contém a lógica principal do sistema, incluindo a comunicação entre processos e a eleição de líderes.
2. **`vector_clock.py`**: Define a classe `VectorClock`, que gerencia a lógica dos relógios vetoriais e suas operações.
3. **`drift.py`**: Implementa a lógica para o gerenciamento do drift, permitindo que o tempo de tick seja ajustado dinamicamente.

## Threads Necessárias

O sistema utiliza quatro threads para garantir a operação correta:

1. **Thread de Drift:** Insere um atraso na contagem do relógio.
2. **Thread de Envio:** Envia o vetor de tempo para outros dispositivos.
3. **Thread de Recepção:** Recebe vetores de tempo de outros dispositivos.
4. **Thread de Contagem:** Serve como o contador que atualiza o vetor local.

## Algoritmo Utilizado

O projeto utiliza o algoritmo de relógios vetoriais para resolver o problema de sincronização de tempo em sistemas distribuídos.

Como o Algoritmo Funciona:
Estrutura de Dados: Cada processo possui um vetor que mantém o estado de seus próprios eventos e os eventos de outros processos. O vetor tem um tamanho igual ao número total de processos, e cada posição do vetor representa o tempo de um processo específico.

Incremento Local: Sempre que um evento ocorre em um processo, ele incrementa seu próprio contador no vetor.

Comunicação: Ao enviar uma mensagem, um processo envia seu vetor de relógio. Quando recebe um vetor, ele atualiza seu próprio vetor tomando o valor máximo entre seu vetor atual e o vetor recebido.

Eleições de Líder: O algoritmo também permite a eleição de um líder com base no valor máximo do vetor. O processo que tiver o maior valor no vetor se torna o novo líder, e os outros processos ajustam seus relógios de acordo.

Resolução do Problema:
Consistência: Os relógios vetoriais garantem que todos os processos tenham uma visão consistente da ordem dos eventos, mesmo que ocorram em paralelo.
Detecção de Conflitos: O algoritmo permite detectar e resolver conflitos entre operações simultâneas, proporcionando uma lógica clara de causalidade.
Robustez em Ambientes Distribuídos: O uso de comunicação assíncrona entre processos permite que o sistema opere de forma robusta, mesmo na presença de falhas ou atrasos na rede.

Em resumo, o algoritmo de relógios vetoriais resolve o problema de sincronização em sistemas distribuídos ao fornecer uma maneira eficiente de rastrear e comunicar o tempo entre processos, garantindo a consistência e a ordem correta dos eventos.

## Execução

Para executar o projeto, siga os passos abaixo:

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/distributed-time-sync.git
   cd distributed-time-sync
