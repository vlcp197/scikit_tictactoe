from flask import Flask, request, jsonify
import sqlite3
import uuid

app = Flask(__name__)
matchs = {}

# Allow connection to the database
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Build players table when the app starts. 
def create_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS players (
            player_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            games_won INTEGER DEFAULT 0,
            games_lost INTEGER DEFAULT 0,
            games_drawn INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

create_table()


# Route to register new players
@app.route('/api/register', methods=['POST'])
def register_player():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "name is required"}), 400
    
    player_name = data['name']
    player_id = str(uuid.uuid4())  # Generate an id for the player
    
    conn = get_db_connection()
    conn.execute(
        '''
        INSERT INTO players (player_id, name) 
        VALUES (?, ?)
        ''', 
        (player_id, player_name)
        )
    conn.commit()
    conn.close()
    
    return jsonify({"player_id": player_id}), 201

if __name__ == '__main__':
    app.run(debug=True)
