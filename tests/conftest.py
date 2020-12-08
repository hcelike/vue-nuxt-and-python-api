"""Create fixtures to use across all tests"""
import random

import pytest

import utils
from user import User
from config import *


@pytest.fixture(scope='module')
def user():
    user = User.create(
        first_name='Francis', 
        last_name='Larson', 
        email='fsnlarson+testing{}@gmail.com'.format(random.randint(1000, 10000)),
        password='password',
        phone_number='9178262319',
        trading_account_username='{}'.format(random.randint(10001,100000)),
    )
    user.trading_account_token = '{}'.format(random.randint(10001,100000))
    user.save() 
    return user




