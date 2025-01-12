import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score


def train_model(X_train: list[np.array],
                X_test: list[np.array],
                y_train: list[np.array],
                y_test: list[np.array]) -> DecisionTreeClassifier:
    """
    Trains the model with an decision tree classifier
    """
    # Train the Decision Tree model
    clf = DecisionTreeClassifier()
    clf.fit(X_train, y_train)

    # Evaluate the model
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.2f}")
    return clf


def board_to_features(board: list[str]) -> list[int]:
    """
    Gets a string list and turns it into a numeric list so the model can
    work better with it.
    """

    if isinstance(board[0], list):
        board = [cell for row in board for cell in row]
    return [1 if x == 'X' else -1 if x == 'O' else 0 for x in board]


def predict_best_move(board: list[int], model=None) -> np.array:
    """
    Where the magic happens.
    Returns a random value if it can predict something better
    """
    teste = board_to_features(board)
    empty_cells = [i for i in range(9) if teste[i] == 0]
    if model is not None:
        # Predict best move
        X_test = np.array([board])
        predictions = model.predict(X_test)
        move = predictions[0]
        if move in empty_cells:
            return move
    # Fallback to random move if model prediction is invalid
    return np.random.choice(empty_cells)
