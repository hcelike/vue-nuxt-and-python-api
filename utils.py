"""Utilities"""
from collections import Counter
import math
import email
import re
import time
from datetime import timedelta
import random
from decimal import Decimal
import string
import bson
import datetime
import uuid
import json
import base64
from io import BytesIO    
import os
import datetime

from flask import *
from faker import Faker
import logging 
import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from sendgrid.helpers.mail import *
from twilio.rest import Client as TwilioClient 


from config import *
import config


def fake_email():
    fake = Faker()
    name = ''.join(fake.name().split()).lower() + str(random_token())
    email = name + '@mailinator.com' 
    return email


def fake_name():
    fake = Faker()
    return fake.name()


def currency(num):
    if num is not None:
        return '${:,.2f}'.format(num)


def percent(num):
    if num is not None:
        return '{:.2f}%'.format(num*100)


def dumps_response(data, **kwargs):
    """return flask response with json-dumped data"""
    return Response(dumps(data),  mimetype='application/json')


def random_token():
    return uuid.uuid1() 


def logger(name=__name__):
    logger = logging.getLogger(name)
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(getattr(logging, config.LOG_LEVEL))
    logger.propagate = False
    return logger


def logged(class_):
    class_.logger = logger(class_.__name__)
    return class_


date_handler = lambda obj: (
    obj.isoformat()
    if isinstance(obj, datetime.datetime)
    or isinstance(obj, datetime.date)
    else None
)


class MongoJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bson.ObjectId):
            return str(obj)
        if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)


def dumps(obj, indent=4):
    return json.dumps(obj, indent=indent, cls=MongoJsonEncoder)

def send_sms(number, message): 
    # Your Account Sid and Auth Token from twilio.com/user/account
    number = re.sub("[^0-9]", "", str(number))
    client = TwilioClient(TWILIO_SID, TWILIO_TOKEN)
    message = client.messages.create(
        number,
        body=message,
        from_=TWILIO_NUMBER,
    )
    print(message)
    return message


def is_number(s):
    try:
        s = float(s)
        if not math.isnan(s): 
            return True
    except Exception as e:
        return False


def send_email(subject, message, from_email, to_email):

    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=message)
    try:
        sg = SendGridAPIClient(SENDGRID_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
   

def to_snake_case(str):
    res = [str[0].lower()] 
    for c in str[1:]: 
        if c in ('ABCDEFGHIJKLMNOPQRSTUVWXYZ'): 
            res.append('_') 
            res.append(c.lower()) 
        else: 
            res.append(c) 
    return ''.join(res) 


def kill_port_process(port):
    os.system('sudo kill -9 `sudo lsof -t -i:{}`'.format(port))
    print('Process on port {} killed'.format(port))
     

