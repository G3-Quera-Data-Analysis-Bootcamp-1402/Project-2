import pandas as pd

from superstore.consts import DATA_DIR


def geo_dim_cleanizer():
    df: pd.DataFrame = pd.read_csv(DATA_DIR / "geo_dim.csv", delimiter="\t")
    df = pd.get_dummies(df, columns=["Country"], prefix="Country")
    return df
