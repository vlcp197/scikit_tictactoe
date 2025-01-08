# initializes an empty game board 
def start_board():    
    return [[" " for _ in range(3)] for _ in range(3)]

# the board parameter needs to be a 3X3 list
def verify_win(board):
    for i in range(3):
        # verify if the board have a horizontal line
        if board[i][0] == board[i][1] == board[i][2] != " ":
            return True
        
        # verify if the board have a vertical line
        if board[0][i] == board[1][i] == board[2][i] != " ":
            return True

    # verify if the board have a diagonal line    
    if board[0][0] == board[1][1] == board[2][2] != " ":
        return True
    
    if board[0][2] == board[1][1] == board[2][0] != " ":
        return True
    
    return False
    

def verify_draw(board):
    ...


