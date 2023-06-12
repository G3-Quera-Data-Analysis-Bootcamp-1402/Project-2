import pandas as pd

from superstore.consts import DATA_DIR


def customer_dim_cleanizer():
    df: pd.DataFrame = pd.read_csv(DATA_DIR / "customer_dim.csv", delimiter="\t")
    df = pd.get_dummies(df, columns=["Segment"])
    return df