import pandas as pd

columns = ['top-left', 'top-middle', 'top-right',
           'middle-left', 'middle-middle', 'middle-right',
           'bottom-left', 'bottom-middle', 'bottom-right',
           'outcome']


def load_dataset(path: str) -> pd.DataFrame:
    data = pd.read_csv(path, names=columns)
    if data.empty:
        # Initialize with empty dataset:
        # 9 features (board) + 1 target (best move)
        data = pd.DataFrame(columns=columns)
    return data


def update_dataset(board: list[int], outcome: str, file_path="dataset.data"):
    """Update the dataset with the new game outcome."""
    new_data = pd.DataFrame([board + [outcome]], columns=columns)
    new_data = new_data.replace(0, "b").replace(-1, "o").replace(1, "x")
    new_data.to_csv(file_path, mode='a', header=False, index=False)
    print("Game data saved.")


def position_to_index(row: int, col: int) -> int:
    """Translate (row, col) position into a number from 0 to 8."""
    return 3 * row + col
