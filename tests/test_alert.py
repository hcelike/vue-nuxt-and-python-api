import pytest

from config import * 
from position import Position 
from alert import Alert
from example_portfolio import ExamplePortfolio


def test_alert_closed_from_position_close(user):
    example_portfolio = ExamplePortfolio(user.trading_account_username)
    position_data = example_portfolio.data().get('data')
    Position.create_positions(user, position_data) 
    open_positions = Position.objects(user=user, is_open=True)
    position = open_positions[0]
    alert = Alert.create(
        user, 
        condition='greater than', 
        value=100, 
        field='price', 
        expiration_date=None, 
        alert_types=['sms'], 
        message=None, 
        position=position
    )
    assert Alert.objects(user=user, is_open=True).count() == 1
    position.remove()
    alert.check_position_still_open()
    assert Alert.objects(user=user, is_open=True).count() == 0


def test_alert_should_trigger(user):
    data = {
        'symbol': 'FB', 
        'security_type': 'OPT',
        'delta': .5,
        'gamma': -.3,
        'vega': .4,
        'theta': 6,
        'underlying_price': 300,
        'price': 300, 
        'value': 30002, 
        'daily_pnl': 1000,
        'unrealized_pnl': 4000,
        'underlying_pct_change': .65,
        'unrealized_pct_change': .1,
        'pnl_pct_change': .09,
    }

    for field in FIELDS:
        value = data[field]

        position = Position.create(user, **data)
        alert = Alert.create(
            user, 
            condition=LESS_THAN,
            value=value, field=field,
            expiration_date=None, 
            alert_types=['sms'], 
            message=None, 
            position=position
        )
        assert alert.should_trigger() == False
        setattr(position, field, value - .1) 
        position.save()
        assert alert.should_trigger() == True

        position = Position.create(user, **data)
        alert = Alert.create(
            user, 
            condition=LESS_THAN_OR_EQUAL_TO,
            value=value, field=field,
            expiration_date=None, 
            alert_types=['sms'], 
            message=None, 
            position=position
        )
        assert alert.should_trigger() == True
        setattr(position, field, value - .1) 
        position.save()
        assert alert.should_trigger() == True

        position = Position.create(user, **data)
        alert = Alert.create(
            user, 
            condition=GREATER_THAN,
            value=value, field=field,
            expiration_date=None, 
            alert_types=['sms'], 
            message=None, 
            position=position
        )
        assert alert.should_trigger() == False
        setattr(position, field, value + .1) 
        position.save()
        assert alert.should_trigger() == True

        position = Position.create(user, **data)
        alert = Alert.create(
            user, 
            condition=GREATER_THAN_OR_EQUAL_TO,
            value=value, field=field,
            expiration_date=None, 
            alert_types=['sms'], 
            message=None, 
            position=position
        )
        assert alert.should_trigger() == True
        setattr(position, field, value + .1) 
        position.save()
        assert alert.should_trigger() == True
      


         
        

    

    
    
    
    
     
    
    

 

       


    



