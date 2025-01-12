import random
import numpy as np

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder


label_encoder = LabelEncoder()



def train_model(X_train, X_test, y_train, y_test):
    # Train the Decision Tree model
    clf = DecisionTreeClassifier()
    clf.fit(X_train, y_train)

    # Evaluate the model
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.2f}")
    return clf


def board_to_features(board):
    if isinstance(board[0], list):  
        board = [cell for row in board for cell in row]  
    return [1 if x == 'X' else -1 if x == 'O' else 0 for x in board]

def predict_best_move(board, model=None):

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

