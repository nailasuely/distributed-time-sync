<h1 align="center">
  <br>
    <img width="400px" src="https://github.com/user-attachments/assets/c2a138c0-3b5e-476c-a7d2-9dea32af8eab">
  <br>
  Sincronização de Relógios em Ambientes Distribuídos
  <br>
</h1>

<h4 align="center">Projeto da disciplina TEC 502 - Concorrência e Conectividade </h4>

<p align="center">
<div align="center">

> Este relatório aborda a implementação de um sistema de sincronização de relógios em ambientes distribuídos utilizando relógios vetoriais. A solução é voltada para computadores conectados na mesma rede, permitindo que dispositivos se comuniquem entre si para ajustar seus relógios, que podem apresentar deriva (drift). O algoritmo utilizado foi o Relógio Vetorial, que permite o compartilhamento de um vetor com a quantidade de índices relacionado com a quantidade de dispositivos no sistema. Este projeto foi desenvolvido como parte dos estudos da disciplina de Concorrência e Conectividade na Universidade Estadual de Feira de Santana (UEFS).</p>

## Download do repositório

```
gh repo clone nailasuely/distributed-time-sync
```

</div>


<details open="open">
<summary>Sumário</summary>

- [Introdução](#Introdução)
- [Tecnologias e Ferramentas Utilizadas](#Tecnologias-e-Ferramentas-Utilizadas)
- [Funcionalidades](#Funcionalidades)
- [Threads Necessárias](#Threads-necessárias)
- [Discussão sobre os requisitos](#Discussão-sobre-os-requisitos)
  - [Interface para gerênciamento](#Interface-para-gerênciamento-do-tempo-dos-relógios)
  - [Protocolo de comunicação](#Protocolo-de-comunicação)
  - [Sincronizaçao dos relógios](#Estratégia-para-sincronizaçao-dos-relógios)
  - [Eleição do relógio referência](#Estratégia-para-eleição-do-relógio-referência)
  - [Tratamento da confiabilidade](#Tratamento-da-confiabilidade)
  - [Tratamento da monotonicidade](#Tratamento-da-monotonicidade)
- [Como utilizar](#Como-utilizar)
- [Equipe](#equipe)
- [Tutor](#tutor)
- [Referências](#referências)
  
</details>


![-----------------------------------------------------](https://github.com/nailasuely/breakout-problem3/blob/main/assets/img/prancheta.png)


<div align="center">
   
</div>

# Introdução 

<p align="justify">Este relatório aborda a implementação de um sistema de sincronização de relógios em ambientes distribuídos utilizando relógios vetoriais. A solução é voltada para computadores conectados na mesma rede, permitindo que dispositivos se comuniquem entre si para ajustar seus relógios, que podem apresentar deriva (drift). O algoritmo utilizado foi o Relógio Vetorial, que permite o compartilhamento de um vetor com a quantidade de índices relacionado com a quantidade de dispositivos no sistema. Este projeto foi desenvolvido como parte dos estudos da disciplina de Concorrência e Conectividade na Universidade Estadual de Feira de Santana (UEFS).</p>

## Tecnologias e Ferramentas Utilizadas
- **Python:** Linguagem de programação. 
- **Flask:**  Framework web em Python usado para realizar a implementação a API RESTful.
- **Socket:** Módulo em Python utilizado para a comunicação de rede.
- **Threading:** Módulo em Python utilizado para implementar threads e permitir operações concorrentes.
- **JSON:** Formato de dados utilizado para troca de mensagens.
- **CORS** (Cross-Origin Resource Sharing): Extensão Flask  que é utilizada para permitir solicitações de diferentes origens para API.
- **Docker:** Ferramenta para empacotar e distribuir aplicativos em contêineres.
  
## Funcionalidades

- **Relógio Vetorial:** Implementa um mecanismo para manter a ordem de eventos em sistemas distribuídos.
- **Comunicação entre Processos:** Usa sockets para enviar e receber atualizações de relógio entre dispositivos.
- **Eleições de Líder:** O dispositivo com maior tempo se torna o novo líder, promovendo a sincronização dos relógios.
- **Drift Manual:** Permite a inserção manual de drift em cada dispositivo para simulações e testes.

## Estrutura do Código

O projeto é estruturado em três arquivos principais:

1. [**`main.py`**](#main): Contém a lógica principal do sistema, incluindo a comunicação entre processos e a eleição de líderes.
2. **`vector_clock.py`**: Define a classe `VectorClock`, que gerencia a lógica dos relógios vetoriais e suas operações.
3. **`drift.py`**: Implementa a lógica para o gerenciamento do drift, permitindo que o tempo de tick seja ajustado dinamicamente.

## Threads Necessárias

O sistema utiliza quatro threads para garantir a operação correta:

1. **Thread de Drift:** Insere um atraso na contagem do relógio.
2. **Thread de Envio:** Envia o vetor de tempo para outros dispositivos.
3. **Thread de Recepção:** Recebe vetores de tempo de outros dispositivos.
4. **Thread de Contagem:** Serve como o contador que atualiza o vetor local.


## Discussão sobre os requisitos

### Interface para gerênciamento do tempo dos relógios

### Protocolo de comunicação

### Estratégia para sincronizaçao dos relógios

### Estratégia para eleição do relógio referência

### Tratamento da confiabilidade

### Tratamento da monotonicidade

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

## Como utilizar

Para executar o relógio usando o docker, siga os passos abaixo:

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/distributed-time-sync.git
   cd distributed-time-sync
    ```

2. Execute o Dockerfile:
   ```bash
   cd clock
   docker build -t time-sync .
   docker run --network='host' -it --name container-time-sync time-sync
    ```
   
Para executar o interface:

1. Execute o Dockerfile:
   ```bash
   cd distributed-time-sync 
   docker-compose up --build
   ```
   - Antes, não esqueça de definir o IP em `components`.


![-----------------------------------------------------](https://github.com/nailasuely/breakout-problem3/blob/main/assets/img/prancheta.png)

## Equipe

- Naila Suele
- Douglas de Jesus

## Tutores

- Elinaldo Santos de Gois Junior

![-----------------------------------------------------](https://github.com/nailasuely/breakout-problem3/blob/main/assets/img/prancheta.png)

## Referências 
> - [1] Python Software Foundation. "threading — Thread-based parallelism." Python 3.12.3 documentation. https://docs.python.org/3/library/threading.html. Acessado em 2024.
> - [2] Python Software Foundation. "socket — Low-level networking interface." Python 3.12.3 documentation. https://docs.python.org/3/library/socket.html. Acessado em 2024.
> - [3] Pallets Projects. "Flask Documentation (3.0.x)." Flask. https://flask.palletsprojects.com/en/3.0.x/api/. Acessado em 2024.
> - [6] Fabricio Veronez. "Docker do zero ao compose: Parte 01." Transmitido ao vivo em 24 de março de 2022.Youtube, https://www.youtube.com/watch?v=GkMJJkWRgBQ&t=2s. Acessado em 2024 
