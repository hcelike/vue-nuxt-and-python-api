from copy import deepcopy
import datetime

from utils import is_number
from models import *
from config import * 
import utils

logger = utils.logger()

@utils.logged
class Position(DynamicDocument):
    """Class represents a trading position"""
    created_date = DateTimeField(default=datetime.datetime.utcnow)
    updated_date = DateTimeField(default=datetime.datetime.utcnow)
    user = ReferenceField('User')
    trading_account_username = StringField()
    account_id = StringField()
    position_id = StringField(unique=False)
    symbol = StringField()
    daily_pnl = FloatField()
    unrealized_pnl = FloatField()
    security_type = StringField()
    expiration_date = DateTimeField()
    multiplier = FloatField()
    strike = FloatField()
    right = StringField()
    delta = FloatField()
    gamma = FloatField()
    vega = FloatField()
    value = FloatField()
    theta = FloatField()
    underlying_price = FloatField()
    entry_price = FloatField()
    open_price = FloatField()
    underlying_pct_change = FloatField()
    unrealized_pct_change = FloatField()
    pnl_pct_change = FloatField()
    price = FloatField()
    position = FloatField()
    is_open = BooleanField(default=True)

    @staticmethod
    def create(user, **kwargs):
        position = Position(
            user=user, 
            trading_account_username=user.trading_account_username,
        )
        try:
            position.save()
        except Exception as e:
            position.logger.error('Error on saving doc')
            position.logger.error(e)
            position.logger.error(utils.dumps(kwargs))
        position.edit(**kwargs)
        return position

    def __str__(self):
        base = '{}-{}-{} '.format(self.trading_account_username, 
            self.account_id, self.security_type)
        pretty = '{} {}'.format(self.symbol, self.security_type) 
        if self.security_type == 'OPT':
           pretty = '{} {} {} {}'.format(
               self.symbol, self.security_type, self.strike, self.right) 
        if self.price:
            price = utils.currency(self.price)
        else:
            price = ' No price data'
        quantity = ' ({} qty)'.format(self.position)
        formatted = base + pretty + ': ' + price + quantity
        return formatted

    def edit(self, **kwargs):
        
        account_id = kwargs.get('account_id')
        position_id = kwargs.get('position_id')
        symbol = kwargs.get('symbol')
        daily_pnl = kwargs.get('daily_pnl')
        unrealized_pnl = kwargs.get('unrealized_pnl')
        security_type = kwargs.get('security_type')
        expiration_date = kwargs.get('expiration_date')
        multiplier = kwargs.get('mutliplier')
        strike = kwargs.get('strike')
        right = kwargs.get('right')
        delta = kwargs.get('delta')
        gamma = kwargs.get('gamma')
        vega = kwargs.get('vega')
        value = kwargs.get('value')
        theta = kwargs.get('theta')
        underlying_price = kwargs.get('underlying_price')
        price = kwargs.get('price')
        position = kwargs.get('position')
        underlying_pct_change = kwargs.get('underlying_pct_change')
        unrealized_pct_change = kwargs.get('unrealized_pct_change')
        pnl_pct_change = kwargs.get('pnl_pct_change')

        self.symbol = symbol
        self.security_type = security_type
        self.multiplier = multiplier
        self.right = right
        self.strike = strike
        self.account_id = account_id
        self.position_id = position_id
        self.expiration_date = expiration_date

        # for data that changes we only want
        # to update the fields if in fact there is data
        # and sometimes the pricing server 
 
        if is_number(daily_pnl):
            self.daily_pnl = float(daily_pnl)

        if is_number(unrealized_pnl):
            self.unrealized_pnl = float(unrealized_pnl)

        if is_number(delta):
            self.delta = float(delta)

        if is_number(value):
            self.value = float(value)

        if is_number(gamma):
            self.gamma = float(gamma)

        if is_number(vega):
            self.vega = float(vega)

        if is_number(theta):
            self.theta = float(theta)

        if is_number(underlying_price):
            self.underlying_price = float(underlying_price)

        if is_number(price):
            self.price = float(price)

        if is_number(position):
            self.position = float(position)

        if is_number(underlying_pct_change):
            self.underlying_pct_change = float(underlying_pct_change)

        if is_number(unrealized_pct_change):
            self.unrealized_pct_change = float(unrealized_pct_change) 

        if is_number(pnl_pct_change):
            self.pnl_pct_change = float(pnl_pct_change) 

        self.updated_date = datetime.datetime.utcnow()
        try:
            self.save()
        except Exception as e:
            self.logger.error('Error on saving doc')
            self.logger.error(e)
            self.logger.error(utils.dumps(kwargs))

    def remove(self): 
        self.is_open = False
        self.save()

    def reopen(self): 
        self.is_open = True
        self.save()

    @staticmethod
    def create_position_id(symbol, account_id, position_data):
        security_type = position_data['security_type']
        id = position_data['id']
        if security_type == 'AGG':
            position_id = '{}-{}-{}'.format(account_id, symbol, security_type) 
        else:
            position_id = '{}-{}-{}'.format(account_id, str(id), security_type) 
        return position_id

    @staticmethod
    def parse_incoming(symbol, account_id, position_data):
        id =  position_data['id']
        position_data['symbol'] = symbol
        position_data['account_id'] = account_id
        position_data['position_id'] = Position.create_position_id(
            symbol, account_id, position_data)
        del position_data['id']
        try:
            position_data['multiplier'] = float(position_data['multiplier'])
        except Exception as e:
            position_data['multiplier'] = None
        try:
            position_data['expiration_date'] = datetime.datetime.strptime(
                position_data['expiration_date'], '%Y%m%d')
        except Exception as e:
            position_data['expiration_date'] = None
        return position_data
     
    @staticmethod
    def create_positions(user, data):
        position_ids = []
        data = deepcopy(data) 
        for account_id in data.keys():
            symbol_data = data[account_id]
            for symbol in symbol_data.keys():
                symbol_positions = symbol_data[symbol]
                for position_data in symbol_positions:
                    position_data = Position.parse_incoming(
                        symbol, account_id, position_data) 
                    position_id = position_data['position_id']
                    if position_data['security_type'] in ['STK', 'OPT', 'AGG']:
                        position_ids.append(position_id)
                        position = Position.objects(
                            user=user, 
                            position_id=position_id).first()
                        if not position:            
                            position = Position.create(      
                                user,
                                **position_data,             
                            )                                
                        else:                                
                            position.edit(**position_data)
                            position.reopen()
                        
        positions = Position.objects(user=user, is_open=True)
        for position in positions:
            if position.position_id not in position_ids:
                logger.error(['removing', str(position)])
                position.remove()
        positions = Position.objects(user=user, is_open=True)
        return positions 




                    
