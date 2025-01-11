import random
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import os

DATASET_PATH = 'tic_tac_toe_dataset.csv'


label_encoder = LabelEncoder()

def load_dataset():

    if os.path.exists(DATASET_PATH):
        df = pd.read_csv(DATASET_PATH)
    else:
        columns = [f'pos_{i}' for i in range(9)] + ['label']
        df = pd.DataFrame(columns=columns)
        df.to_csv(DATASET_PATH, index=False)
        return df
    

    df['label'] = label_encoder.fit_transform(df['label'])
    return df

def train_model(df):

    if df.empty:
        return None
    X = df.drop('label', axis=1)
    y = df['label']
    

    class_weights = {
        label_encoder.transform(['Win'])[0]: 2,
        label_encoder.transform(['Draw'])[0]: 1,
        label_encoder.transform(['Lose'])[0]: 0
    }
    model = RandomForestClassifier(class_weight=class_weights)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)
    model.fit(X_train, y_train)
    accuracy = accuracy_score(y_test, model.predict(X_test))
    print(f'Model trained with accuracy: {accuracy:.2f}')
    return model

def board_to_features(board):
    if isinstance(board[0], list):  
        board = [cell for row in board for cell in row]  
    return [1 if x == 'X' else -1 if x == 'O' else 0 for x in board]

def predict_best_move(board, model=None):
 
    available_moves = [i for i, x in enumerate(board) if x == ' ']
    if not available_moves or model is None:
        return random.choice(available_moves) if available_moves else None
    best_move = None
    max_prob = -1
    win_index = label_encoder.transform(['Win'])[0]  
    
    for move in available_moves:
        temp_board = board[:]
        temp_board[move] = 'O'
        features = np.array(board_to_features(temp_board)).reshape(1, -1)
        prob = model.predict_proba(features)[0][win_index]
        if prob > max_prob:
            max_prob = prob
            best_move = move
    return best_move

def update_dataset(board, result):
    features = board_to_features(board)
    df = pd.read_csv(DATASET_PATH)
    new_data = pd.DataFrame([features + [result]], columns=df.columns)
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(DATASET_PATH, index=False)
    global model
    df['label'] = label_encoder.fit_transform(df['label'])
    model = train_model(df)
