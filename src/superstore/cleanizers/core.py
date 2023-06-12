import pandas as pd

from superstore.consts import CLEANIZED_DIR

from superstore.cleanizers.order_dim import order_dim_cleanizer
from superstore.cleanizers.geo_dim import geo_dim_cleanizer


def store_cleanized_data():
    order_dim_cleanizer().to_csv(CLEANIZED_DIR / "order_dim.csv", index=False)
    geo_dim_cleanizer().to_csv(CLEANIZED_DIR / "geo_dim.csv", index=False)