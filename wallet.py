from coin import Coin
import matplotlib.pyplot as plt
import numpy as np

class Wallet:

    def __init__(self):
        self.coins = {}
        new_coin = input('\nAdd which coin to your portfolio? ').upper()
        while new_coin != '':
            self.add_asset(new_coin)
            new_coin = input('\nAdd a coin or press [Enter] to continue: ').upper()
        print('\n')
        self.value = self.get_value()
        self.ts = self.get_ts()
        

    def __repr__(self):
        consolidated_coins = [f'{i[1]} {i[0]}' for i in self.coins.values()]
        return f"\nWallet worth ${self.value:.2f} containing: " + ', '.join(consolidated_coins)
    

    def get_value(self):
        value = 0
        for coin in self.coins.values():
            value += coin[1] * coin[0].price
        return value


    def get_ts(self):
        values = list(self.coins.values())
        ts = [[t[0], 0] for t in values[0][0].ts]
        for coin in values:
            for i, j in enumerate(coin[0].ts):
                ts[i][1] += j[1] * coin[1]
        return ts
       
    
    def plot_ts(self):
        plt.plot([t[0] for t in self.ts], [p[1] for p in self.ts])
        plt.title("Time Series for Your Wallet")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.show()


    def plot_ts_asset(self, asset = None):
        assets = list(self.coins.keys())
        if asset is None:
            asset = input('Plot time series for which asset? ')
        asset = asset.upper()
        while asset not in assets:
            asset = input(f"That asset isn't in your wallet.\nPlease choose from {assets}: ").upper()
        plt.plot([t[0] for t in self.coins[asset][0].ts], [p[1] for p in self.coins[asset][0].ts])
        plt.title(f"Time Series for {asset}")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.show()

    
    def plot_dist(self):
        ts_price = [p[1] for p in self.ts]
        returns = [np.log(ts_price[i]/ts_price[i-1]) for i in range(1, len(ts_price))]
        plt.hist(returns, bins = 32)
        plt.title("Return Distribution for Your Wallet")
        plt.xlabel(f"Log Return with mean {np.mean(returns):.4%} and sd {np.std(returns):.4%}")
        plt.ylabel("Frequency")
        plt.show()


    def plot_dist_asset(self, asset = None):
        if asset is None:
            fig = plt.figure("Asset Return Distribution")
            length = len(list(self.coins.keys()))
            ncol = int(np.ceil(np.sqrt(length)))
            nrow = int(np.ceil(length / ncol))
            for i, coin in enumerate(list(self.coins.values())):
                ts_price = [p[1] for p in coin[0].ts]
                returns = [np.log(ts_price[i]/ts_price[i-1]) for i in range(1, len(ts_price))]
                ax = fig.add_subplot(nrow, ncol, i + 1)
                ax.hist(returns, bins = 32)
                ax.set_title(f'Distribution for {coin[0].asset}')
                ax.set_xlabel(f"Returns with mean {np.mean(returns):.4%} and sd {np.std(returns):.4%}")
                ax.set_ylabel("Frequency")
            fig.tight_layout()
        else:
            assets = list(self.coins.keys())
            asset = asset.upper()
            while asset not in assets:
                asset = input(f"That asset isn't in your wallet.\nPlease choose from {assets}: ").upper()
            ts_price = [p[1] for p in self.coins[asset][0].ts]
            returns = [np.log(ts_price[i]/ts_price[i-1]) for i in range(1, len(ts_price))]
            plt.hist(returns, bins = 32)
            plt.title(f'{asset} Return Distribution')
            plt.xlabel(f'Log Return with mean {np.mean(returns):.4%} and sd {np.std(returns):.4%}')
        plt.show()


    def add_asset(self, asset = None, amount = None):
        if asset is None:
            asset = input('Add which asset to your wallet? ').upper()
        if amount is None:
            amount = float(input(f'Add how many tokens of {asset}? '))
        assets = list(self.coins.keys())
        added = True
        asset = asset.upper()
        amount = float(amount)
        if asset in assets:
            self.coins[asset][1] += amount
        else:
            my_vars = vars()
            try:
                new_asset = 'X' + asset + 'ZUSD'
                my_vars[new_asset] = Coin(new_asset)
                self.coins[str(my_vars[new_asset])] = [my_vars[new_asset], amount]
            except KeyError:
                try:
                    new_asset = asset + 'USD'
                    my_vars[new_asset] = Coin(new_asset)
                    self.coins[str(my_vars[new_asset])] = [my_vars[new_asset], amount]
                except KeyError:
                    try:
                        new_asset = asset
                        my_vars[new_asset] = Coin(new_asset)
                        if my_vars[new_asset].asset not in assets:
                            self.coins[str(my_vars[new_asset])] = [my_vars[new_asset], amount]
                        else:
                            self.coins[my_vars[new_asset].asset][1] += amount
                    except KeyError:
                        print('Could not find an asset by that name... \n')
                        added = False
        if added:
            try:
                print(f'\nAdded {amount} of {my_vars[new_asset].asset} to your wallet.')
            except UnboundLocalError:
                print(f'\nAdded {amount} of {self.coins[asset][0].asset} to your wallet.')
            self.value = self.get_value()



    def remove_asset(self, asset = None, amount = None):
            pass


    def save(self, name):
        pass


    def load(self, name):
        pass


if __name__ == '__main__':
    my_wallet = Wallet()
    print(my_wallet)