import datetime

import bcrypt
from mongoengine import (
    DynamicDocument, 
    EmbeddedDocument,
    ListField,
    GenericReferenceField,
    ReferenceField,
    LazyReferenceField,
    FileField,
    FloatField,
    DictField,
    StringField,
    DateTimeField,
    BooleanField,
    EmbeddedDocumentField,
    IntField,
)
from itsdangerous import URLSafeTimedSerializer
import boto
from boto.s3.key import Key
from boto.s3.connection import S3Connection
from authy.api import AuthyApiClient
from authy import AuthyFormatException

import utils
import database
from config import *
from trading_service import TradingService
from models import *
from validate_email import validate_email
from position import Position
from alert import Alert
from message import Message


authy_api = AuthyApiClient(AUTHY_API_KEY)


@utils.logged
class User(DynamicDocument):
    email = StringField(max_length=255, api_public=True)
    password = StringField(max_length=255)
    first_name = StringField( api_public=True)
    last_name = StringField( api_public=True)
    phone_number = StringField(max_length=255, api_public=True)
    role = StringField(default='owner', api_public=True)
    date_account_claimed = DateTimeField(api_public=True)
    date_last_invite_sent = DateTimeField(api_public=True)
    accepted_tos_date = DateTimeField()
    accepted_tos_ip = StringField()
    websocket_session_id = StringField()
    trading_account_username = StringField()
    trading_account_token = StringField()
    confirmed_emails = ListField(StringField(), default=[], api_public=True)
    authy_id = StringField() 
    enable_sound_alerts = BooleanField(default=False)
    enable_voice_alerts = BooleanField(default=False)

    def check_alerts(self):
        alerts = Alert.objects(user=self, is_open=True)
        for alert in alerts:
            alert.check()

    def check_trading_data(self):
        t = TradingService(token=self.trading_account_token)
        status = t.check()
        return status

    def clear_trading_account(self):
        self.trading_account_token = None
        self.trading_account_username = None
        self.save()

    def clear_positions(self):
        for position in Position.objects(is_open=True, user=self):
            position.remove()

    def stop_trading_data(self, token=None):
        token = token or self.trading_account_token
        t = TradingService(token=token)
        status = t.stop()
        self.clear_trading_account()
        self.clear_positions()
        return status

    def start_trading_data(self, username, password, trading_mode):
        self.stop_trading_data()
        websocket_endpoint = WEBSOCKET_ENDPOINT
        webhook_url = API_ENDPOINT + '/webhooks/trading_service'
        t = TradingService(
          username, password, trading_mode, 
          websocket_endpoint=websocket_endpoint, 
          startup_done_webhook=webhook_url,
        )
        token, status = t.start()
        self.logger.info('STARTING')
        self.logger.info(token)
        self.logger.info(status)
        self.trading_account_token = token
        self.trading_account_username = username
        self.save()
        return status

    def send_confirm_email(self):
        link = self.confirm_email_link()
        subject = "Please confirm your email"
        message_data = {
            'link': link, 
            'subject': subject,
        }
        self.send_message('confirm_email', 
            message_data=message_data)

    def has_role(self, role_name):
        return role_name == self.role

    @staticmethod 
    def hash_password(plaintext):
        plaintext = plaintext.encode('utf-8')
        hashed = bcrypt.hashpw(plaintext, bcrypt.gensalt()).decode('utf-8')
        return hashed

    @staticmethod
    def is_email_available(email, user):
        if user:
            existing_user = User.objects(email=email, id__ne=user.id).first() 
        else:
            existing_user = User.objects(email=email).first() 
        if not existing_user:
            return True
        return False

    @staticmethod
    def is_email_valid(email):
        return validate_email(email)

    @staticmethod
    def is_email_usable(email, user=None):
        email = email.lower().strip()
        if not User.is_email_available(email, user):
            return False, 'Email is in use'
        if not User.is_email_valid(email):
            return False, 'Email is invalid'
        return True, None

    def is_correct_password(self, plaintext):
        plaintext = plaintext.encode('utf-8')
        hashed_password = self.password.encode('utf-8')
        return bcrypt.checkpw(plaintext, hashed_password) 

    def set_password(self, password):
        self.password = User.hash_password(password)
        self.save()

    def set_email(self, email):
        email = email.lower().strip()
        self.email = email
        self.save()

    def set_phone_number(self, phone_number):
        self.phone_number = phone_number
        self.save()
        self.create_authy()

    def password_changed(self):
        """tell user their password has changed"""
        message_data = {'subject': 'Your password has changed'}
        self.send_message(message_template='password_changed', message_data=message_data)

    def password_reset_link(self, invite=False):
        """generate password reset link"""
        token = self.generate_token()
        link = self.dashboard_url() + CHANGE_PASSWORD_ROUTE + '?token=' + token
        if invite:
            link += '&invite=true'
        return link

    def confirm_email_link(self):
        """generate confirm email link and return"""
        token = self.generate_token()
        link = self.dashboard_url() + '/confirm_email?token=' + token 
        return link

    def send_invite(self, medium='email', message_template='invite_team', **data):
        """send invite link and send to user"""
        link = self.password_reset_link(invite=True)
        subject = "You've been invited to {}".format(BRAND_NAME)
        message_data = {
            'link': link, 
            'subject': subject,
        }
        message_data.update(data)
        self.send_message(message_template=message_template, 
            message_data=message_data, medium=medium)
        self.date_last_invite_sent = datetime.datetime.now()
        self.save()

    def claim_account(self): 
        if not self.date_account_claimed:
            self.date_account_claimed = datetime.datetime.now()
            self.save()

    def dashboard_url(self):
        """get the dashboard url if this user"""
        url = DASHBOARD_ENDPOINT
        return url

    def send_password_reset(self):
        """generate password token and send to user"""
        link = self.password_reset_link()
        message_data = {'link': link, 'subject': 'Reset Your Password'}
        self.send_message(message_template='reset_your_password', 
            message_data=message_data)

    def generate_token(self):
        """generate token used for password resets"""
        ts = URLSafeTimedSerializer(FLASK_SECRET_KEY)
        token = ts.dumps(self.email, salt=PASSWORD_RECOVER_KEY)
        return token

    @staticmethod
    def get_user_from_reset_token(token):
        """Returns user if token is right and token not expired"""
        ts = URLSafeTimedSerializer(FLASK_SECRET_KEY)
        email = ts.loads(token, salt=PASSWORD_RECOVER_KEY, max_age=86400)
        if email:
            user = User.objects(email=email).first()
            return user

    def full_name(self):
        return "{} {}".format(self.first_name.encode('utf-8').decode('utf-8'), 
            self.last_name.encode('utf-8').decode('utf-8'))

    def request_two_factor_token(self):
        if not self.authy_id:
            raise Exception('No Authy id for this user')
        sms = authy_api.users.request_sms(self.authy_id, {'force': True})

    def validate_two_factor_token(self, token):
        try:
            verification = authy_api.tokens.verify(
                self.authy_id,
                token
            )
            if not verification.ok():
                self.logger.error('Invalid Token')
                return False
        except AuthyFormatException as e:
            self.logger.error(str(e))
            return False
        return True

    def create_authy(self):
        authy_user = authy_api.users.create(
             self.email,
             self.phone_number,
             1,
        )
        self.authy_id = str(authy_user.id)
        self.save()

    @staticmethod 
    def create(email, password, **kwargs):
        first_name = kwargs.get('first_name', '').strip()
        last_name = kwargs.get('last_name', '').strip()
        middle_name = kwargs.get('middle_name', '').strip()
        trading_account_username = kwargs.get('trading_account_username')
        requires_two_factor = kwargs.get('requires_two_factor', False)
        email = email.lower().strip()
        dob = kwargs.get('dob')
        phone_number = kwargs.get('phone_number')
        dob = Dob(**dob) if dob else dob 
        password = User.hash_password(password)
        user = User.objects(email=email).first()
        if not user:
            user = User(
                email=email, 
                password=password, 
                first_name=first_name, 
                middle_name=middle_name, 
                last_name=last_name, 
                dob=dob,
                phone_number=phone_number,
                trading_account_username=trading_account_username,
                requires_two_factor=requires_two_factor,
            )
            user.save()
            if user.requires_two_factor:
                user.create_authy()
            return user
        else:
            raise Exception('User exists already')

    def send_message(
            self, 
            message_template, 
            message_data={},
            medium='email',  
            attachments=None, 
            alert=None,
        ):
        sender_data = {
            'first_name': self.first_name, 
            'last_name': self.last_name
        }
        if medium == 'sms':
            recipients = [self.phone_number]
        else:
            recipients = [self.email]
        m = Message(
            message_template=message_template,
            user=self,
            sender_data=sender_data, 
            message_data=message_data,
            recipients=recipients,
            medium=medium, 
            attachments=attachments,
            alert=alert,
        )
        m.send()
    




