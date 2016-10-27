#!/usr/bin/env python3

import sys

from data.api import HDFReader, HDFWriter
import datetime as dt
import pandas as pd

reader = HDFReader()
writer = HDFWriter()
# data = pd.DataFrame(pd.np.random.rand(10,2), index=pd.DatetimeIndex(start=pd.datetime(2015,1,1), periods=10, freq='d'))
# writer.write(data, **{
#     'table_key': 'test',
#     'symbol': 'GOLD',
#     'provider':'oanda',
#     'data_type': 'forex', #data_tags
#     'candle_format': 'ohlcv',
#     'granularity':'m1',
#     'dt_first': dt.datetime(2016, 1, 1),
#     'dt_last': dt.datetime(2016, 4, 1)
#     })

for data in reader.read(symbol='GOLD',
            table_key='test',
            provider='oanda',
            data_type='forex',
            candle_format='ohlcv',
            granularity='m1',
            dt_first=dt.datetime(2016, 2, 1),
            dt_last=dt.datetime(2016, 4, 1)):
    print(data)

#provider...
