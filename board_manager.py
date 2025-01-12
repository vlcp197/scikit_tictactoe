def start_board() -> list[int]:
    """
    initializes an empty game board
    """
    board = [0] * 9
    return board


def check_winner(board: list[int]) -> int | None:
    """Check if there's a winner."""
    winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                            (0, 3, 6), (1, 4, 7), (2, 5, 8),
                            (0, 4, 8), (2, 4, 6)]
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != 0:
            return board[combo[0]]
    if 0 not in board:
        return 0  # Draw
    return None  # Game continues


def board_to_repr(board: list[int]) -> str:
    """
    Turns the numeric board list into a string,
    so it can be written to a database.
    """
    board_repr = ",".join(str(x) for x in board)
    parts = board_repr.split(',')
    board_repr = f"""{parts[0]} , {parts[1]} , {parts[2]} |
                     {parts[3]} , {parts[4]} , {parts[5]} |
                     {parts[6]} , {parts[7]} , {parts[8]}"""
    board_repr = board_repr\
        .replace("0", " ")\
        .replace("-1", "O")\
        .replace("1", "X")
    return board_repr
