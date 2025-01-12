import pandas as pd

def load_dataset(path):
    columns = ['top-left', 'top-middle', 'top-right', 'middle-left', 'middle-middle', 'middle-right', 'bottom-left', 'bottom-middle', 'bottom-right', 'outcome']
    data = pd.read_csv(path, header=None, names=columns)
    if data.empty:
        # Initialize with empty dataset: 9 features (board) + 1 target (best move)
        data = pd.DataFrame(columns=columns)
    return data

def update_dataset(board, outcome, file_path="tic_tac_toe_updated.csv"):
    """Update the dataset with the new game outcome."""
    columns = ['top-left', 'top-middle', 'top-right', 'middle-left', 'middle-middle', 'middle-right', 'bottom-left', 'bottom-middle', 'bottom-right', 'outcome']
    new_data = pd.DataFrame([board + [outcome]], columns=columns)
    new_data.to_csv(file_path, mode='a', header=False, index=False)
    print("Game data saved.")
