import pandas as pd

from superstore.consts import DATA_DIR

def product_dim_cleanizer():
    df: pd.DataFrame = pd.read_csv(DATA_DIR / "product_dim.csv", delimiter="\t")
    df = pd.get_dummies(df, columns=["Sub-Category","Category"])
    return df

print(product_dim_cleanizer())