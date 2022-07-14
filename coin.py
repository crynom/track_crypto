import requests

class Coin:
    
    def __init__(self, ticker):
        self.ticker = ticker.upper()
        self.price = self.get_price()
        self.asset = self.ticker[1:-4]

    def __repr__(self):
        return str(self.asset)

    def get_price(self):
        resp = requests.get(f'https://api.kraken.com/0/public/Ticker?pair={self.ticker}').json()
        return float(resp['result'][self.ticker]['c'][0])

if __name__ == '__main__':
    pass