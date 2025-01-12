# Flask-RESTful API & Machine Learning Tic Tac Toe

Este projeto implementa uma API em flask que permite jogar jogo da velha contra 
um modelo de machine learning.

O algoritmo utilizado para treinar o modelo é o de arvore de decisão. 

Exemplo de dataset utilizado:
```
b,b,b,o,b,o,x,x,x,positive
b,b,b,b,o,o,x,x,x,positive
x,x,o,x,x,o,o,b,o,negative
x,x,o,x,x,o,b,o,o,negative
...
```

Da esquerda para a direita, as posições de cada letra refletem uma posição no 
tabuleiro. A palavra "positive" refere-se ao formato do tabuleiro onde a IA 
ganha o jogo. A palavra "negative" refere-se ao formato do tabuleiro em que a IA
perde.

A posições de cada letra em uma linha, da esquerda para a direita, referem-se às
seguintes posições no tabuleiro:
"superior-esquerda", "superior-central", "superior-direita",
"central-esquerda", "central", "central-direita",
"inferior-esquerda","inferior-central", "inferior-direita"

Link do dataset utilizado: [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/101/tic+tac+toe+endgame)

Principais bibliotecas utilizadas:
1. Flask - Provisionar servidor para a API.
2. Numpy - Manipulação de arrays.
3. Pandas - Manipulação de dataframes e csv.
4. scikit-learn - Treinamento e implementação de IA.

Estrutura do projeto:
```
.
├── README.md
├── app.py
├── board_manager.py
├── db_manager.py
├── preprocessing.py
├── ticTacToeMl.py
├── utils.py
├── dockerfile
├── docker-compose.yml
├── dataset.data
└── requirements.txt
```

* app.py - Inicialização da aplicação.
* board_manager.py - Módulo  relacionado a manipulação do tabuleiro.
* db_manager.py - Módulo relacionado a manipulação do banco de dados.
* preprocessing.py - Módulo relacionado ao pré processamento dos dados usados para treinar o modelo.
* ticTacToeMl.py - Módulo do modelo de machine learning.
* utils.py - Funções relacionadas a tratamento do arquivo de dataset.
* dataset.data - Arquivo que contém a informação para treinar o modelo.

## Como Executar

1. Clone o repositório.
2. No terminal Windows, sem docker. É necessário ter o python instalado em uma versão acima do 12:
    ```
    python -m venv venv;
    ./venv/Scripts/activate;
    pip install requirements.txt;
    flask run

    ```

3. Caso deseje utilizar Docker. É necessário ter o docker e docker compose instalados:
    ```
    docker-compose build
    docker-compose up
    ```
    
## Como utilizar a API
### Endpoint para registrar jogador
POST http://127.0.0.1:5000/api/register/

REQUISIÇÃO
```json
{
	"nome": "Teste"
}
```
RESPOSTA
```json
{
    "player_id": "fe1320ed-5f80-4d82-a549-b2d998c91d9d"
}
```
### Endpoint para mostrar estado do tabuleiro
POST http://127.0.0.1:5000/api/board/

REQUISIÇÃO
```json
{
	"game_id": "fe1320ed-5f80-4d82-a549-b2d998c91d9d"
}
```
RESPOSTA
```json
{
    "tabuleiro": "  ,   ,   |   ,   ,   |   ,   ,  ",
    "Jogo": "fe1320ed-5f80-4d82-a549-b2d998c91d9d"
}
```
### Endpoint para começar um novo jogo
POST http://127.0.0.1:5000/api/start/

REQUISIÇÃO
```json
{
    "player_id": "fe1320ed-5f80-4d82-a549-b2d998c91d9d"
}
```

RESPOSTA
```json
{
    "game_id": "d96a3415-8776-423a-884e-157bd3406aa4",
    "player_id": "fe1320ed-5f80-4d82-a549-b2d998c91d9d",
    "tabuleiro": "  ,   ,   |   ,   ,   |   ,   ,  "

}
```
### Endpoint para fazer um movimento no jogo
POST http://127.0.0.1:5000/api/move/

Você precisa fazer uma requisição no endpoint para iniciar um novo jogo e copiar o game_id que é retornado pela api para usar como argumento nesta requisição


REQUISIÇÃO
```json
{
    "game_id": "d96a3415-8776-423a-884e-157bd3406aa4",
    "player_id": "fe1320ed-5f80-4d82-a549-b2d998c91d9d",
    "linha": "2",
    "coluna": "0"
}
```

RESPOSTA
```json
{
    "tabuleiro": "O , O ,   |   ,   ,   | X , X , X"
    "mensagem": "Jogada válida",
}
```

### Endpoint para retornar os status do jogador
POST http://127.0.0.1:5000/api/player-stats/

REQUISIÇÃO
```json
{
    "player_id": "fe1320ed-5f80-4d82-a549-b2d998c91d9d"
}
```
RESPOSTA
```json
{
        "Nome": "Teste",
        "Vitorias": 1,
        "Derrotas": 1,
        "Empates": 0,
}
```