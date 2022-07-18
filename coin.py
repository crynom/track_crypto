import requests
from datetime import datetime as dt
class Coin:
    
    def __init__(self, ticker):
        self.ticker = ticker.upper()
        self.price = self.get_price()
        self.asset = self.ticker[1:-4] if self.ticker[-4:] == 'ZUSD' else self.ticker[:-3]
        self.ts = self.get_ts()

    def __repr__(self):
        return str(self.asset)

    def get_price(self):
        resp = requests.get(f'https://api.kraken.com/0/public/Ticker?pair={self.ticker}').json()
        return float(resp['result'][self.ticker]['c'][0])

    def get_ts(self):
        resp = requests.get(f'https://api.kraken.com/0/public/OHLC?pair={self.ticker}&interval=1440').json()
        ts = [(dt.fromtimestamp(int(t[0])), float(t[4])) for t in resp['result'][self.ticker]]
        return ts

if __name__ == '__main__':
    pass
    