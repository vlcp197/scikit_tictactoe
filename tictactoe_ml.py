from sklearn.tree import DecisionTreeClassifier

class TicTacToeMl(DecisionTreeClassifier):

    def machine_plays(board:list[str], player_moves: list[int]):
        ...