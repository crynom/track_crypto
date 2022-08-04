from coin import Coin
import matplotlib.pyplot as plt
import numpy as np
from os import path

class Wallet:

    def __init__(self, load = False, interval = 1440):
        self.coins = {}
        self.interval = interval
        if not load:
            new_coin = input('\nAdd which coin to your portfolio? ').upper()
            while new_coin != '':
                self.add_asset(new_coin)
                new_coin = input('\nAdd a coin or press [Enter] to continue: ').upper()
            print('\n')
        

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
        plt.xticks(rotation = 45)
        plt.ylabel("Price")
        plt.show()


    def plot_ts_asset(self, asset = None):
        assets = list(self.coins.keys())
        if asset is None:
            asset = input('Plot time series for which asset? ')
        asset = asset.upper()
        if asset == 'ALL':
            fig = plt.figure("Asset Time Series")
            length = len(assets)
            ncol = int(np.ceil(np.sqrt(length)))
            nrow = int(np.ceil(length / ncol))
            for i, coin in enumerate(list(self.coins.values())):
                ax = fig.add_subplot(nrow, ncol, i + 1)
                ax.plot([t[0] for t in coin[0].ts], [p[1] for p in coin[0].ts])
                ax.set_title(f'Distribution for {coin[0].asset}')
                ax.set_xlabel(f"Date")
                ax.set_ylabel("Price")
                ax.tick_params(axis='x', labelrotation = 45)
            fig.tight_layout()
        else:
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
        assets = list(self.coins.keys())
        if asset is None:
            asset = input('Plot distribution for which asset? ')
        asset = asset.upper()
        if asset == 'ALL':
            fig = plt.figure("Asset Return Distribution")
            length = len(list(self.coins.keys()))
            ncol = int(np.ceil(np.sqrt(length)))
            nrow = int(np.ceil(length / ncol))
            for i, coin in enumerate(list(self.coins.values())):
                ts_price = [p[1] for p in coin[0].ts]
                returns = [np.log(ts_price[n]/ts_price[n-1]) for n in range(1, len(ts_price))]
                ax = fig.add_subplot(nrow, ncol, i + 1)
                ax.hist(returns, bins = 32)
                ax.set_title(f'Distribution for {coin[0].asset}')
                ax.set_xlabel(f"Returns with mean {np.mean(returns):.4%} and sd {np.std(returns):.4%}")
                ax.set_ylabel("Frequency")
            fig.tight_layout()
        else:
            while asset not in assets:
                asset = input(f"That asset isn't in your wallet.\nPlease choose from {assets}: ").upper()
            ts_price = [p[1] for p in self.coins[asset][0].ts]
            returns = [np.log(ts_price[i]/ts_price[i-1]) for i in range(1, len(ts_price))]
            plt.hist(returns, bins = 32)
            plt.title(f'{asset} Return Distribution')
            plt.xlabel(f'Log Return with mean {np.mean(returns):.4%} and sd {np.std(returns):.4%}')
            plt.ylabel('Frequency')
        plt.show()


    def valid_number(self, amount):
        try:
            amount = float(amount)
            if amount <= 0:
                return False
            return True
        except ValueError:
            return False
        


    def add_asset(self, asset = None, amount = ''):
        if asset is None:
            asset = input('Add which asset to your wallet? ').upper()
        if amount == '':
            while not self.valid_number(amount):
                amount = input(f'Add how many tokens of {asset}? ')
            amount = float(amount)
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
                my_vars[new_asset] = Coin(new_asset, interval= self.interval)
                self.coins[str(my_vars[new_asset])] = [my_vars[new_asset], amount]
            except KeyError:
                try:
                    new_asset = asset + 'USD'
                    my_vars[new_asset] = Coin(new_asset, interval= self.interval)
                    self.coins[str(my_vars[new_asset])] = [my_vars[new_asset], amount]
                except KeyError:
                    try:
                        new_asset = asset
                        my_vars[new_asset] = Coin(new_asset, interval= self.interval)
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
            self.ts = self.get_ts()



    def remove_asset(self, asset = None, amount = ''):
            if asset is None:
                asset = input("\nRemove which asset? ")
            asset = asset.upper()
            while asset not in list(self.coins.keys()):
                asset = input("\nThat asset is not in your wallet. Remove which asset? ").upper()
            if amount == '':
                while not self.valid_number(amount):
                    amount = input(f"\nRemove how many tokens of {asset}? ")
                amount = float(amount)
            if amount >= self.coins[asset][1]:
                del self.coins[asset]
                print(f"\nDeleted {asset} from your wallet... ")
            else:
                self.coins[asset][1] -= amount
                print(f"\nRemoved {amount} of {asset}... ")
            self.value = self.get_value
            self.ts = self.get_ts()


    def save(self, name):
        path_to = path.realpath(path.join(path.dirname(__file__), 'saves', f'{name}.csv'))
        values = list(self.coins.values())
        with open(path_to, 'w') as file:
            for i, coin in enumerate(values):
                if i < len(values):
                    file.write(f'{coin[0]}${coin[1]},')
                else:
                    file.write(f'{coin[0]}${coin[1]}')
        print(f'Saved {name} to saves...\n')


    def load(self, name):
        path_from = path.realpath(path.join(path.dirname(__file__), 'saves', f'{name}.csv'))
        with open(path_from, 'r') as file:
            loaded = file.read()
            for coins in loaded.split(','):
                coin = coins.split('$')
                self.add_asset(coin[0], coin[1])
        print(f'Loaded {name} from saves...\n')


    def cov_matrix(self):
        returns = []
        for coin in list(self.coins.values()):
            prices = [p[1] for p in coin[0].ts]
            log_ret = [np.log(prices[i]/prices[i-1]) for i in range(1, len(prices))]
            returns.append(log_ret)
        covmtx = np.cov(returns)
        assets = list(self.coins.keys())
        print(f'\n        {"         ".join(assets)}')
        for i, j in zip(assets, covmtx):
            print(i, j)
        self.covmtx = covmtx

    
    def corr_matrix(self):
        returns = []
        for coin in list(self.coins.values()):
            prices = [p[1] for p in coin[0].ts]
            log_ret = [np.log(prices[i]/prices[i-1]) for i in range(1, len(prices))]
            returns.append(log_ret)
        corrmtx = np.corrcoef(returns)
        assets = list(self.coins.keys())
        print(f'\n        {"         ".join(assets)}')
        for i, j in zip(assets, corrmtx):
            print(i, j)
        self.corrmtx = corrmtx


    def plot_relative_price(self):
        assets = list(self.coins.keys())
        asset = input('\nPlot which asset? ').upper()
        while asset not in assets:
            asset = input('\nThat asset is not in your wallet. Plot which asset? ').upper()
        against = input('\nPlot against which asset? ').upper()
        while against not in assets:
            against = input('\nThat asset is not in your wallet. Plot against which asset? ').upper()
        fig = plt.figure('Relative Price Plot', figsize=(12,8))
        ax1 = fig.add_subplot(1,3,1)
        ax1.plot([t[0] for t in self.coins[asset][0].ts], [p[1] for p in self.coins[asset][0].ts], color = 'red')
        ax1.set_title(f'Time Series for {asset}')
        ax1.set_xlabel('Date')
        ax1.tick_params(axis='x', labelrotation = 45)
        ax1.set_ylabel('Price')
        ax2 = fig.add_subplot(1,3,2)
        ax2.plot([t[0] for t in self.coins[asset][0].ts], [p[1]/a[1] for p, a in zip(self.coins[asset][0].ts, self.coins[against][0].ts)])
        ax2.set_title(f'Time Series for {asset}/{against}')
        ax2.set_xlabel('Date')
        ax2.tick_params(axis='x', labelrotation = 45)
        ax2.set_ylabel('Price')
        ax3 = fig.add_subplot(1,3,3)
        ax3.plot([t[0] for t in self.coins[against][0].ts], [p[1] for p in self.coins[against][0].ts], color = 'green')
        ax3.set_title(f'Time Series for {against}')
        ax3.set_xlabel('Date')
        ax3.tick_params(axis='x', labelrotation = 45)
        ax3.set_ylabel('Price')
        fig.tight_layout()
        plt.show()


    def pos_neg_dist(self):
        pass


if __name__ == '__main__':
    my_wallet = Wallet()
    my_wallet.load('test')
    my_wallet.add_asset(asset='xrp', amount=10)
    # print(my_wallet)
    my_wallet.cov_matrix()
    my_wallet.remove_asset(asset='xrp', amount=10)
    my_wallet.corr_matrix()
    # my_wallet.plot_relative_price()
    # my_wallet.plot_dist()
    # my_wallet.plot_dist_asset()
    # my_wallet.plot_ts()
    # my_wallet.plot_ts_asset()
    