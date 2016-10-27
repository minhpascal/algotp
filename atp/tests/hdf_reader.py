#!/usr/bin/env python3

import sys

from atp.data import HDFReader
import datetime as dt

reader = HDFReader()

for d in reader.read(symbol='GOLD',
            provider='oanda',
            data_type='forex',
            candle_format='ohlcv',
            granularity='m1',
            dt_first=dt.datetime(1, 1, 2016),
            dt_last=dt.datetime(1, 1, 2016)):
    print('data: ', d)
