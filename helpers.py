import time

from config import *
from models import *
from user import User
from position import Position
import utils
from alert_event import AlertEvent
from alert import Alert


def clear_all_data():
    if input('Are you sure you want to delete everything? YES/no  ') == 'YES':
        for p in Position.objects():
            print('Deleting', p)
            for a in Alert.objects(position=p):
                print('Deleting', a)
                a.delete()
            for a in AlertEvent.objects(position=p):
                print('Deleting', a)
                a.delete()
            p.delete()


def create_user(role=None):
    u = User.create(
        first_name='Francis', 
        last_name='Larson', 
        email='fsnlarson@gmail.com',
        password='password',
        phone_number='9178262319',
        trading_account_token='test_token',
    )
    u.role = role
    u.save()
    return u
    

    
if __name__ == '__main__':
    u = User.objects(email='fsnlarson+admin@gmail.com').first()
    u.role = 'admin'
    u.save()
   
   

 
    
   
   
    
    
    
