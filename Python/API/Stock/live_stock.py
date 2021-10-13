import os
import sys
import time
import yfinance
import pandas as pd
import numpy as np


while True:
    data = yfinance.download(tickers='FTNT', period='5m', interval='1m', progress=False)

    latest_point = data['Close'][-1:]

    print(latest_point)

    time.sleep(1)