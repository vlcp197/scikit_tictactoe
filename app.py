import numpy as np
from utils import load_dataset, update_dataset, position_to_index
import ticTacToeMl as ml
from preprocessing import preprocessing
from board_manager import board_to_repr, start_board, check_winner
import db_manager as dbm

from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

matchs = {}

dataset = load_dataset("dataset.data")
X_y = preprocessing(dataset)

model = ml.train_model(*X_y)

dbm.create_players_table()

outcome = None


@app.route('/api/register/', methods=['POST'])
def register_player():
    """Route to register new players"""
    data = request.get_json()
    if not data or 'nome' not in data:
        return jsonify({"erro": "campo 'nome' ausente"}), 400

    player_name = data['nome']
    player_id = str(uuid.uuid4())  # Generate an id for the player

    dbm.create_player(player_id, player_name)

    return jsonify({"player_id": player_id}), 201


@app.route('/api/board/', methods=['POST'])
def peek_board():
    """
    Route to retrieve the board state
    """
    data = request.get_json()
    game_id = data.get("game_id")
    _match = matchs.get(game_id)
    board = _match["board"]

    return jsonify({
        "tabuleiro": board_to_repr(board),
        "Jogo": game_id
    }), 200


@app.route('/api/start/', methods=['POST'])
def start_game():
    """
    Route to start a new match
    """
    data = request.get_json()
    player_id = data.get("player_id")
    game_id = str(uuid.uuid4())
    board = start_board()

    dbm.create_match_board()
    dbm.create_match(player_id, game_id, board_to_repr(board))

    matchs[game_id] = {
        "board": board,
        "current_player": player_id,
    }

    return jsonify({
        "game_id": game_id,
        "player_id": player_id,
        "tabuleiro": board_to_repr(board)
    }), 201


@app.route('/api/move/', methods=['POST'])
def make_move():
    """
    Route to make a move in the game
    """
    data = request.get_json()
    game_id = data.get("game_id")
    player_id = data.get("player_id")
    line = int(data.get("linha"))
    column = int(data.get("coluna"))

    if not all([game_id, player_id, line, column]):
        if not data:
            return jsonify({"erro": "campos ausentes"}), 400
        elif 'game_id' not in data:
            return jsonify({"erro": "campo 'game_id' ausente"}), 400
        elif 'player_id' not in data:
            return jsonify({"erro": "campo 'player_id' ausente"}), 400
        elif 'linha' not in data:
            return jsonify({"erro": "campo 'linha' ausente"}), 400
        elif 'coluna' not in data:
            return jsonify({"erro": "campo 'coluna' ausente"}), 400

    _match = matchs.get(game_id)
    if not _match:
        return jsonify({"erro": "Jogo não encontrado"}), 404

    if player_id != _match["current_player"]:
        return jsonify({"erro": "Não é o turno deste jogador"}), 403

    board = _match["board"]
    index = position_to_index(line, column)
    if board[index] != 0:
        return jsonify({"erro": "Posição já ocupada"}), 400

    board[index] = 1
    dbm.update_board(game_id, board)

    outcome = check_winner(board)
    if outcome:
        if outcome == 0:
            dbm.update_player_draw(player_id)
            update_dataset(board, "negative")
            return jsonify({
                "tabuleiro": board_to_repr(board),
                "resultado": "Empate"
            }), 200

        dbm.update_player_win(player_id)
        update_dataset(board, "negative")
        name, *_ = dbm.fetch_player_stats(player_id)

        return jsonify({
            "tabuleiro": board_to_repr(board),
            "resultado": f"Vitoria do jogador: {name}"
        }), 200

    # # AI makes its move
    board_state = np.array(board).reshape(1, -1)
    move = np.argmax(model.predict_proba(board_state)[0])
    while board[move] != 0:
        move = (move + 1) % 9
    board[move] = -1  # Model is O

    outcome_ai = check_winner(board)
    # Check if AI wins
    if check_winner(board):
        if outcome_ai == 0:
            dbm.update_player_draw(player_id)
            update_dataset(board, "negative")
            return jsonify({
                "tabuleiro": board,
                "resultado": "Empate"
            }), 200

        dbm.update_player_lose(player_id)
        update_dataset(board, "positive")
        return jsonify({
            "tabuleiro": board_to_repr(board),
            "resultado": "Vitoria da IA"
        }), 200

    return jsonify({
        "tabuleiro": board_to_repr(board),
        "mensagem": "Jogada válida"
    }), 200


@app.route('/api/player-stats/', methods=['POST'])
def player_stats():
    """
    Route to check the player statistics
    """
    data = request.get_json()
    player_id = data.get("player_id")
    name, wins, loses, draws = dbm.fetch_player_stats(player_id)
    return jsonify({
        "Nome": name,
        "Vitorias": wins,
        "Derrotas": loses,
        "Empates": draws,
    }), 200

@app.route('/api/ai-move/', methods=['POST'])
def ai_hint():
    raise NotImplementedError("Not Implemented")
#     data = request.get_json()
#     game_id = data.get("game_id")
#     _match = matchs.get(game_id)
#     board = _match["board"]

#     board_state = np.array(board).reshape(1, -1)
#     move = np.argmax(model.predict_proba(board_state)[0])
#     while board[move] != 0:
#         move = (move + 1) % 9
#     board[move] = -1  # Model is O
#     ...
#     return jsonify({
#         "Próxima jogada sugerida: ": None
#     }), 200


if __name__ == '__main__':

    app.run(debug=True)
