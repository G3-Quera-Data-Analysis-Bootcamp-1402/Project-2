import pathlib

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm


from superstore.consts import DATA_DIR


def divide_data(data_dir: pathlib.Path = DATA_DIR) -> None:
    fact_df: pd.DataFrame = pd.read_csv(data_dir / "fact.csv", delimiter="\t")
    fact_df["Discounted"] = (
        fact_df["Discount"]
        .mask(fact_df["Discount"] > 0, True)
        .mask(fact_df["Discount"] == 0, False)
    )
    product_df: pd.DataFrame = pd.read_csv(data_dir / "product_dim.csv", delimiter="\t")
    df: pd.DataFrame = pd.merge(fact_df, product_df, how="left", on="Product ID").loc[
        :, ["Product Name", "Sales", "Quantity", "Discount", "Profit", "Discounted"]
    ]
    discounted_df: pd.DataFrame = df.loc[df["Discounted"] == True]
    undiscounted_df: pd.DataFrame = df.loc[df["Discounted"] == False]
    discounted_product_df: pd.DataFrame = (
        discounted_df.groupby("Product Name").sum(numeric_only=True).reset_index()
    )
    undiscounted_product_df = pd.DataFrame = (
        undiscounted_df.groupby("Product Name").sum(numeric_only=True).reset_index()
    )
    discounted_product_df["Product Code"] = discounted_product_df.index.tolist()
    undiscounted_product_df["Product Code"] = undiscounted_product_df.index.tolist()
    return discounted_product_df, undiscounted_product_df


def plot_data(data_dir: pathlib.Path = DATA_DIR) -> None:
    d_df, und_df = divide_data(data_dir)

    def get_values(df: pd.DataFrame, col: str) -> np.ndarray:
        return df[col].values

    fig, axes = plt.subplots(3, 2, figsize=(9, 16), tight_layout=True)
    cols: dict[int, pd.DataFrame] = {0: d_df, 1: und_df}
    rows: dict[int, str] = {0: "Sales", 1: "Quantity", 2: "Profit"}
    for col in [0, 1]:
        for row in [0, 1, 2]:
            axes[row][col].hist2d(
                get_values(cols[col], "Product Code"),
                get_values(cols[col], rows[row]),
                bins=10,
                norm=LogNorm(),
            )
            axes[row][col].set_xlabel("Product Code")
            axes[row][col].set_ylabel("Sales")
    # set titles
    axes[0][0].set_title("Discounted")
    axes[0][1].set_title("Undiscounted")
    # set limits
    axes[0][0].set_ylim(0, 65000)
    axes[0][1].set_ylim(0, 65000)
    axes[1][0].set_ylim(0, 500)
    axes[1][1].set_ylim(0, 500)
    axes[2][0].set_ylim(-10000, 20000)
    axes[2][1].set_ylim(-10000, 20000)
    # show plots
    plt.show()