import random
import time

import socketio

from config import *
import utils

from example_portfolio import ExamplePortfolio
from user import User

if TEST:
    user = User.objects(email='fsnlarson@gmail.com').first()
    token = user.trading_account_token
else:
    token = 'test_token' 
    

portfolio1 = ExamplePortfolio(token=token)
sio = socketio.Client()
sio.connect(WEBSOCKET_ENDPOINT)


@sio.event
def connect():
    print("I'm connected!")



while True:
    time.sleep(2)
    sio.emit('position', portfolio1.data())
    portfolio1.increase()
