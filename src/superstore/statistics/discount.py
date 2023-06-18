import pathlib

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy as sp
from matplotlib.colors import LogNorm, LinearSegmentedColormap


from superstore.consts import DATA_DIR


def divide_data(data_dir: pathlib.Path = DATA_DIR) -> tuple[pd.DataFrame]:
    """
    merge fact table with product_dim table
    extract needed columns
    split data into 2 groups discounted and undiscounted
    """

    def discount_preprocessor(df: pd.DataFrame, discounted: bool) -> pd.DataFrame:
        result_df: pd.DataFrame = df.loc[df["Discounted"] == discounted].copy().groupby("Product Name").sum(numeric_only=True).reset_index()
        result_df["Product Code"] = result_df.index.values
        cols: list[str] = ["Product Code", "Product Name", "Sales", "Quantity", "Discount", "Profit"]
        return result_df.loc[:, cols]


    fact_df: pd.DataFrame = pd.read_csv(data_dir / "fact.csv", delimiter="\t")
    product_df: pd.DataFrame = pd.read_csv(data_dir / "product_dim.csv", delimiter="\t")
    merged_df: pd.DataFrame = pd.merge(fact_df, product_df, how="left", on="Product ID")
    merged_df["Discounted"] = merged_df["Discount"].mask(lambda x: x > 0, True).mask(lambda x: x == 0, False)
    d_df: pd.DataFrame = discount_preprocessor(merged_df, True)
    und_df: pd.DataFrame = discount_preprocessor(merged_df, False)
    return (d_df, und_df)
   

def ttest_data(d_df: pd.DataFrame, und_df: pd.DataFrame) -> pd.DataFrame:
    """
    do ttest between discounted and undiscounted products using three metircs
    sales, quantity, profit
    """
    metrics: list[str] = ["Sales", "Quantity", "Profit"]
    d_metrics_df = d_df.loc[:, metrics].copy()
    und_metrics_df = und_df.loc[:, metrics].copy()
    
    stats_values, p_values = sp.stats.ttest_ind(d_metrics_df, und_metrics_df)

    data: dict[str, list] = {"Stats": stats_values.tolist(), "P_value": p_values.tolist()}

    ttest_df: pd.DataFrame = pd.DataFrame(data, index=metrics)
    ttest_df.index.name = "Metric"

    return ttest_df


def plot_data(d_df: pd.DataFrame, und_df: pd.DataFrame) -> None:
    """
    d_df: discounted products dataframe
    und_df: undiscounted products dataframe
    create 3 2D histogram plots for each groups (discounted, undiscounted)
    x-axis: Product Code
    y-axis: [Sales, Quantity, Profit]
    """
    def get_values(df: pd.DataFrame, col: str) -> np.ndarray:
        return df[col].values

    fig, axes = plt.subplots(3, 2, figsize=(9, 16), tight_layout=True)
    colors: list[tuple] = [(0.85, 0.7, 1), (0.7, 0.3, 1)] # light purple to dark purple
    cmap = LinearSegmentedColormap.from_list("LbDb", colors)

    cols: dict[int, pd.DataFrame] = {0: d_df, 1: und_df}
    rows: dict[int, str] = {0: "Sales", 1: "Quantity", 2: "Profit"}
    for col in [0, 1]:
        for row in [0, 1, 2]:
            axes[row][col].hist2d(
                get_values(cols[col], "Product Code"),
                get_values(cols[col], rows[row]),
                bins=10,
                norm=LogNorm(),
                cmap=cmap
            )
            axes[row][col].set_xlabel("Product Code")
            axes[row][col].set_ylabel(rows[row])
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


def store_data(dataframes: list[pd.DataFrame], filenames: list[str], has_index: list[bool], data_dir: pathlib.Path = DATA_DIR,) -> None:
    """
    store divide_data and ttest_data into csv files which stored in
    data/statistics/
    """
    for df, fn, hi in zip(dataframes, filenames, has_index):
        df.to_csv(data_dir / f"statistics/{fn}.csv", index=hi)
