import sqlite3

# Allow connection to the database
def get_db_connection() -> sqlite3.Row:
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