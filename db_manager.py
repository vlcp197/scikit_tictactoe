import sqlite3

# Allow connection to the database
def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Build players table when the app starts. 
def create_players_table():
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

def create_player(player_id: str, player_name: str):
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

def create_match_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS match (
            game_id	TEXT NOT NULL UNIQUE PRIMARY KEY,
            player	TEXT,
            board_state	TEXT
        )
    ''')
    conn.commit()
    conn.close()


def create_match(player_id, game_id, board):
    
    board = ' | '.join(','.join(inner_list) for inner_list in board)

    conn = get_db_connection()
    conn.execute(
        '''
        INSERT INTO match (game_id, player, board_state) 
        VALUES (?, ?, ?)
        ''', 
        (game_id, player_id, board)
        )
    conn.commit()
    conn.close()

def update_player_win(player_id):
    conn = get_db_connection()
    conn.execute(
        """
        UPDATE players
        SET games_won = 1 
        WHERE player_id = ?
        """, 
        (player_id,))
    conn.commit()
    conn.close()

def update_player_lose(player_id):
    conn = get_db_connection()
    conn.execute(
        "UPDATE players SET games_lost = games_lost + 1 WHERE player_id = ?", 
        (player_id,)
        )
    conn.commit()
    conn.close()

def update_player_draw(player_id):
    conn = get_db_connection()
    conn.execute(
            "UPDATE players SET games_drawn = games_drawn + 1 WHERE player_id = ?", (player_id,))
    conn.commit()
    conn.close()

def fetch_player_stats(player_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""SELECT name, games_won, games_lost, games_drawn FROM players WHERE player_id = (?)""", (player_id,))
    result = cursor.fetchone()
    return result[0:4] 



