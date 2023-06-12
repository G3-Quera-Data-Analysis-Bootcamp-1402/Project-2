import pandas as pd

from superstore.consts import CLEANIZED_DIR

from superstore.cleanizers.order_dim import order_dim_cleanizer
from superstore.cleanizers.geo_dim import geo_dim_cleanizer
from superstore.cleanizers.product_dim import product_dim_cleanizer
from superstore.cleanizers.customer_dim import customer_dim_cleanizer


def store_cleanized_data():
    order_dim_cleanizer().to_csv(CLEANIZED_DIR / "order_dim.csv", index=False)
    geo_dim_cleanizer().to_csv(CLEANIZED_DIR / "geo_dim.csv", index=False)
    product_dim_cleanizer().to_csv(CLEANIZED_DIR / "product_dim.csv", index=False)
    customer_dim_cleanizer().to_csv(CLEANIZED_DIR / "customer_dim.csv", index=False)