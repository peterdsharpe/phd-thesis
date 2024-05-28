from common import *

cols = [
    "airspeed",
    "baro_alt",
    "voltage",
    "current",
]

import polars as pl

df = pl.DataFrame({
    c: simple_read(c)[1]
    for c in cols
})

print(df.describe())