import pytest

from config import FIELDS
from position import Position 
from example_portfolio import ExamplePortfolio


def test_positions_match_incoming_account_portfolio_data(user):
    for x in range(5):
        example_portfolio = ExamplePortfolio(user.trading_account_token)
        position_data = example_portfolio.data().get('data')
        Position.create_positions(user, position_data) 
        open_positions = Position.objects(user=user, is_open=True)
        assert len(example_portfolio.positions) == open_positions.count() 

        for incoming_position in example_portfolio.positions:
            symbol = incoming_position['symbol']
            account_id = incoming_position['account_id']
            position_id = Position.create_position_id(symbol, account_id, incoming_position)
            open_position = Position.objects.get(
                position_id=position_id, is_open=True)
           
            for field in FIELDS:
                incoming_position_value = incoming_position.get(field)
                open_position_value = getattr(open_position, field)
                assert open_position_value == incoming_position_value

        example_portfolio.positions.pop()
        example_portfolio.positions.pop()
        position_data = example_portfolio.data().get('data')
        Position.create_positions(user, position_data) 
        assert len(example_portfolio.positions) == open_positions.count() 

 

       


    



