Teste Prático: Jogo da Velha com Flask, Identificação de Jogadores e Machine Learning

 

Objetivo do Teste

Desenvolver uma API em Flask que permita jogadores identificados por ID jogarem contra um modelo de Machine Learning em um jogo da velha, onde as decisões de jogada são baseadas em histórico de jogadas armazenadas em um dataset.

 

Instruções Gerais

1. Crie um repositório no GitHub para o seu projeto.

2. Estruture seu projeto de forma limpa, utilizando boas práticas de organização de código.

3. Inclua um arquivo README.md com instruções claras de como configurar e executar o projeto.

4. Use commits consistentes para documentar o desenvolvimento do projeto.

 

Parte 1: Configuração do Ambiente

 

1. Setup do Ambiente

- Crie um ambiente virtual para o projeto.

- Prepare um arquivo `requirements.txt` com todas as dependências necessárias, incluindo Flask, numpy, pandas e uma biblioteca de Machine Learning como scikit-learn.

Parte 2: Sistema de Identificação de Jogadores

 

1. Modelagem de Jogadores

- Implemente um sistema para registrar jogadores, onde cada jogador tem um ID único (`player_id`), nome e histórico de jogos (vencidas, perdidas, empatadas).

2. Rota para Registro de Jogadores

- Implemente uma rota `POST /api/register` para registrar novos jogadores com um nome. Retorne o `player_id` do jogador registrado.

 

Parte 3: Implementação da Lógica do Jogo

 

1. Representação do Tabuleiro

- Implemente uma representação do tabuleiro do jogo da velha com uma estrutura de dados apropriada (por exemplo, uma lista 3x3).

2. Regras do Jogo

- Crie funções para verificar condições de vitória, empate e jogadas válidas.

 

Parte 4: Desenvolvimento da API Flask

 

1. Iniciar Jogo

- Implemente uma rota `POST /api/start` que inicia um novo jogo com base no `player_id`. Retorne o estado inicial do tabuleiro e os IDs dos jogadores.

2. Realizar Jogada

- Implemente uma rota `POST /api/move` que aceita a jogada do jogador utilizando seu `player_id`. A entrada deve incluir a posição no tabuleiro. Retorne o estado atualizado do tabuleiro e o resultado se o jogo terminou.

 

Parte 5: Machine Learning e Histórico de Jogadas

 

1. Dataset de Histórico de Jogadas

- Utilize ou simule um dataset que insere várias situações de jogo com as jogadas subsequentes mais prováveis.

2. Treinamento do Modelo

- Treine um modelo de Machine Learning usando o dataset para prever a próxima melhor jogada, considerando o histórico de jogadas.

3. Integração com a API

- Implemente uma rota `GET /api/ai-move` onde, após a jogada do jogador, o modelo de Machine Learning sugere a próxima jogada com base no estado atual do tabuleiro e no histórico.

4. Atualização do Histórico

- Após cada jogo, atualize o histórico com os resultados para melhorias futuras no modelo.

 

Parte 6: Extras (Opcional)

1. Interface de Estatísticas

- Adicione uma rota `GET /api/player-stats/<player_id>` que retorna as estatísticas de jogo do jogador, incluindo o número de vitórias, derrotas e empates.

2. Feedback do Jogo

- Implemente um sistema de feedback que sugere ao jogador melhorias com base no resultado dos jogos.

 

Entrega

- Certifique-se de que o `README.md` contém todas as instruções necessárias para instalar dependências, configurar o ambiente e rodar o servidor Flask.

- Inclua exemplos detalhados de como interagir com a API, registrar jogadores, iniciar jogos e realizar jogadas.

- Detalhe os passos necessários para treinar o modelo e como a integração do conjunto de dados histórico melhora o desempenho da IA.

 