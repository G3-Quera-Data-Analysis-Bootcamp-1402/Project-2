import pandas as pd

from superstore.consts import DATA_DIR


def order_dim_cleanizer():
    df: pd.DataFrame = pd.read_csv(DATA_DIR / "order_dim.csv", delimiter="\t")
    priorities: dict[str, int] = {
        "Low": 1,
        "Medium": 2,
        "High": 3,
        "Critical": 4
    }
    for priority_name, priority_val in priorities.items():
        df["Order Priority"] = df["Order Priority"].mask(df["Order Priority"] == priority_name, priority_val)
    df = pd.get_dummies(df, columns=["Ship Mode"])    
    return df