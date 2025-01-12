from flask import Flask, request, jsonify
import uuid

from board_manager import start_board,verify_draw,verify_win
from db_manager import create_players_table, create_player, create_match_table, create_match, update_player_win,update_player_lose, update_player_draw, fetch_player_stats, update_board
import tictactoe_ml as ml

app = Flask(__name__)
matchs = {}

create_players_table()

dataset = ml.load_dataset()
model = ml.train_model(dataset)

# Route to register new players
@app.route('/api/register/', methods=['POST'])
def register_player():
    data = request.get_json()
    if not data or 'nome' not in data:
        return jsonify({"error": "campo 'nome' ausente"}), 400
    
    player_name = data['nome']
    player_id = str(uuid.uuid4())  # Generate an id for the player
    
    create_player(player_id, player_name)
    
    return jsonify({"player_id": player_id}), 201

@app.route('/api/board/', methods=['GET'])
def peek_board():
    return start_board()

@app.route('/api/start/', methods=['POST'])
def start_game():
    data = request.get_json()
    player_id = data.get("player_id")
    game_id = str(uuid.uuid4())
    board = start_board()
    
    create_match_table()
    create_match(player_id, game_id, board)

    matchs[game_id] = {
        "board": board,
        "current_player": player_id,
    }

    return jsonify({
        "game_id": game_id,
        "player_id": player_id,
        "tabuleiro": board
    }), 201

@app.route('/api/move/', methods=['POST'])
def make_move():
    data = request.get_json()
    game_id = data.get("game_id")
    player_id = data.get("player_id")
    line = int(data.get("linha"))
    column = int(data.get("coluna"))

    if not all([game_id, player_id, line, column]):
        if not data:
            return jsonify({"error": "campos ausentes"}), 400
        elif 'game_id' not in data:
            return jsonify({"error": "campo 'game_id' ausente"}), 400
        elif 'player_id' not in data:
            return jsonify({"error": "campo 'player_id' ausente"}), 400
        elif 'linha' not in data:
            return jsonify({"error": "campo 'linha' ausente"}), 400
        elif 'coluna' not in data:
            return jsonify({"error": "campo 'coluna' ausente"}), 400
    
    _match = matchs.get(game_id)
    if not _match:
        return jsonify({"error": "Jogo não encontrado"}), 404
    
    if player_id != _match["current_player"]:
        return jsonify({"error": "Não é o turno deste jogador"}), 403
    
    board = _match["board"]
    if board[line][column] != " ":
        return jsonify({"error": "Posição já ocupada"}), 400

    board[line][column] = "X"
    update_board(game_id, board)

    if verify_win(board):

        update_player_win(player_id)
        ml.update_dataset(board, result="Lose")
        return jsonify({
            "tabuleiro": board,
            "resultado": f"Vitoria do jogador {player_id}"
        }), 200
    
    if verify_draw(board):
        update_player_draw(player_id)

        return jsonify({
            "tabuleiro": board,
            "resultado": "Empate"
        }), 200
    
    # AI makes its move
    flat_board = [cell for row in board for cell in row]
    ai_move_index = ml.predict_best_move(flat_board, model)
    if ai_move_index is None:
        return jsonify({"error": "Erro ao calcular a jogada da IA"}), 500

    ai_line, ai_column = divmod(ai_move_index, 3)
    board[ai_line][ai_column] = "O"
    update_board(game_id, board)

    # Check if AI wins
    if verify_win(board):
        update_player_lose(player_id)
        ml.update_dataset(board, result="Win")
        return jsonify({
            "tabuleiro": board,
            "resultado": "Vitoria da IA"
        }), 200

    if verify_draw(board):
        update_player_draw(player_id)
        ml.update_dataset(board, result="Draw")
        return jsonify({
            "tabuleiro": board,
            "resultado": "Empate"
        }), 200

    return jsonify({
        "tabuleiro": board,
        "mensagem": "Jogada válida"
    }), 200

@app.route('/api/player-stats/', methods=['POST'])
def player_stats():
    data = request.get_json()
    player_id = data.get("player_id")
    name,wins,loses,draws = fetch_player_stats(player_id)
    return jsonify({
        "Nome": name,
        "Vitorias": wins,
        "Derrotas": loses,
        "Empates": draws,
    }), 200


if __name__ == '__main__':
    app.run(debug=True)
