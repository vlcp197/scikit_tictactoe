from numpy import array
from sklearn.model_selection import train_test_split
import pandas as pd


def preprocessing(data: pd.DataFrame) -> list[array]:
    """
    Prepare the dataset for train the model
    """
    # Encode categorical data (x = 1, o = -1, b = 0)
    mapping = {'x': 1, 'o': -1, 'b': 0}
    for col in data.columns[:-1]:
        data[col] = data[col].map(mapping)

    data['outcome'] = data['outcome'].map({'positive': -1, 'negative': 0})
    # Split data into features and labels
    X = data[list(data.columns[:-1])]
    y = data['outcome']

    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42)

    return X_train, X_test, y_train, y_test
