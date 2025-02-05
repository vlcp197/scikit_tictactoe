import sqlite3

from board_manager import board_to_repr


def get_db_connection() -> sqlite3.Connection:
    """
    Allow connection to the database
    """
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def create_players_table():
    """
    Build players table, if not created, when the app starts
    """
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
    """
        Register player when the api endpoint is called.
    """
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


def create_match_board():
    """
        Create the board for the match
    """
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


def create_match(player_id: str, game_id: str, board: list[int]):
    """
    Create match when the endpoint is called
    """
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


def update_player_win(player_id: str):
    """
    Called when someone wins a match
    """
    conn = get_db_connection()
    conn.execute(
        """
        UPDATE players
        SET games_won = games_won + 1
        WHERE player_id = ?
        """,
        (player_id,))
    conn.commit()
    conn.close()


def update_player_lose(player_id: str):
    """
    Called when someone loses a match
    """
    conn = get_db_connection()
    conn.execute(
        """
        UPDATE players
        SET games_lost = games_lost + 1
        WHERE player_id = ?
        """,
        (player_id,))
    conn.commit()
    conn.close()


def update_player_draw(player_id: str):
    """
    Called when the match draws
    """
    conn = get_db_connection()
    conn.execute(
        """
        UPDATE players
        SET games_drawn = games_drawn + 1
        WHERE player_id = ?
        """,
        (player_id,))
    conn.commit()
    conn.close()


def fetch_player_stats(player_id: str) -> list[str | int]:
    """
    Allows to see the player name, how many games it won, lose or have drawn.
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT name, games_won, games_lost, games_drawn
        FROM players
        WHERE player_id = (?)
        """,
        (player_id,))
    result = cursor.fetchone()
    return result[0:4]


def update_board(game_id: str, board: list[int]):
    """
    Update the board to the database after ever move
    """
    board = board_to_repr(board)
    conn = get_db_connection()
    conn.execute(
        """
        UPDATE match
        SET board_state = ?
        WHERE game_id = ?
        """,
        [board, game_id])
    conn.commit()
    conn.close()
