import yfinance

data = yfinance.download(tickers='FTNT', period='1m', interval='1m')

print(data)