import random
import datetime
import json
import time
from collections import defaultdict, Counter

import utils


class ExamplePortfolio(object):

    def __init__(self, token):
        self.token = token
        self.number_stocks = random.randint(5, 7) 
        self.account_ids = ['DU{}'.format(random.random()), 'REAL{}'.format(random.random())]
        self.symbols = [
            'MSFT',
            'AMZN',
            'AAPL', 
            'TSLA',
            'FB',
            'GOOGL', 
            'ZM',
            'WMT', 
            'MRNA', 
            'BABA',
        ]
        self.positions = []
        self.construct_portfolio()
        
    def construct_portfolio(self):
        stocks = random.sample(self.symbols, self.number_stocks)
        for account_id in self.account_ids:
            for symbol in stocks:
                underlying_price = float(random.randint(20, 2000))
                quantity = random.randint(10, 50)
                position = {
                    'security_type': 'STK', 
                    'account_id': account_id,
                    'symbol': symbol,
                    'id': random.randint(10000000, 1000000000), 
                    'price': underlying_price, 
                    'underlying_price': underlying_price,
                    'open_price': underlying_price,
                    'value': underlying_price * quantity,
                    'daily_pnl': random.randint(-1000, 10000),
                    'unrealized_pnl': random.randint(1000, 10000),
                    'entry_price': underlying_price,
                    'position': quantity,
                }
                self.positions.append(position)
                self.number_legs = random.randint(1, 3)
                for leg in range(self.number_legs):
                    price = underlying_price/100.0 
                    quantity = random.randint(2, 20)
                    position = {
                        'security_type': 'OPT', 
                        'symbol': symbol,
                        'price': price, 
                        'id': random.randint(10000000, 1000000000), 
                        'position': quantity,
                        'right': random.choice(['P', 'C']),
                        'underlying_price': underlying_price,
                        'daily_pnl': random.randint(-1000, 10000),
                        'unrealized_pnl': random.randint(1000, 10000),
                        'value': price * quantity * 100,
                        'open_price': price,
                        'multiplier': 100,
                        'entry_price': price,
                        'account_id': account_id,
                        'expiration_date': datetime.datetime.utcnow().strftime('%Y%m%d'),
                        'strike': random.randint(int(underlying_price * .9), int(underlying_price * 1.1)), 
                        'delta': round(random.random(), 2),
                        'gamma': round(random.random(), 2),
                        'vega': round(random.random(), 2),
                        'theta': round(random.random(), 2),
                    }
                    self.positions.append(position)

                counter = Counter()
                for position in self.positions: 
                    d = {
                        'vega': position.get('vega', 0),
                        'gamma': position.get('gamma', 0),
                        'theta': position.get('theta', 0),
                        'delta': position.get('delta', 0),
                        'daily_pnl': position.get('daily_pnl', 0),
                        'value': position.get('value', 0),
                        'unrealized_pnl': position.get('unrealized_pnl', 0),
                    } 
                    counter.update(d)
                agg_position = dict(counter)
                agg_position['symbol'] = symbol
                agg_position['security_type'] = 'AGG'
                agg_position['account_id'] = account_id
                agg_position['position'] = None
                agg_position['price'] = None
                agg_position['id'] = random.randint(10000000, 1000000000) 
                agg_position['entry_price'] = None
                agg_position['open_price'] = None
                self.positions.append(agg_position)

    def increase(self):
        underlying = {}
        for position in self.positions:
            for field in ['price', 'delta', 'gamma', 'vega', 'theta', 'daily_pnl', 'value']:
                if position.get(field) and position['security_type'] == 'OPT':
                    position[field] *= random.uniform(.9, 1.1)
                    position[field] = round(position[field], 2)
            underlying_price = position.get('underlying_price')
            symbol = position.get('symbol')
            if position['security_type'] != 'AGG':
                if not underlying.get(symbol):
                    underlying[symbol] = underlying_price * random.uniform(1 - .0001, 1 + .0001)
                position['underlying_price'] = round(underlying[symbol], 2)
                if position['security_type'] == 'STK':
                    position['price'] = position['underlying_price']
                multiplier = position.get('multiplier', 1)
            print(utils.dumps(position))

    def data(self):
        data = {
            'token': self.token,
            'data': {},
        }
        position_data = {} 
        for position in self.positions:
            account_id = position['account_id']
            if data['data'].get(account_id) is None:
                data['data'][account_id] = defaultdict(list)  
            data['data'][account_id][position['symbol']].append(position)  
        return data

if __name__ == '__main__':
    e = ExamplePortfolio('mecat')
    print(json.dumps(e.data()['data'], indent=2))
    for x in range(100):
        time.sleep(.2)
        e.increase() 
        print(json.dumps(e.data()['data'], indent=2))
    
