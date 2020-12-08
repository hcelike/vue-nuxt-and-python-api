from flask import *
from flask import g
from flask_jwt_extended import create_access_token, get_current_user
from flask_restx import Api, Resource, fields, marshal, utils as futils

import utils
from models import *
from alert import Alert
from alert_event import AlertEvent
from position import Position
from config import *
from public_globals import PublicGlobals
from base_app import *
from user import User


api_blueprint = Blueprint(
    'api',
    __name__,
    subdomain=API_SUBDOMAIN,
    url_prefix='/v1',
)


api = Api(
    api_blueprint,
    version='1.0',
    title='{} API'.format(BRAND_NAME),
    description='',
    ui=False,
    doc=DOCS_URL,
    add_specs=SHOW_DOCS,
    authorizations={'basicAuth': {'type': 'basic'}},
    security=['basicAuth'],
)


position_schema  = api.model('Position', {
    'id': fields.String(readOnly=True),
    'account_id': fields.String,
    'trading_account_username': fields.String,
    'position_id': fields.String,
    'daily_pnl': fields.Float,
    'unrealized_pnl': fields.Float,
    'symbol': fields.String,
    'security_type': fields.String,
    'expiration_date': fields.DateTime,
    'multiplier': fields.Float,
    'strike': fields.Float,
    'right': fields.String,
    'delta': fields.Float,
    'gamma': fields.Float,
    'value': fields.Float,
    'vega': fields.Float,
    'theta': fields.Float,
    'underlying_price': fields.Float,
    'updated_date': fields.DateTime,
    'entry_price': fields.Float,
    'open_price': fields.Float,
    'price': fields.Float,
    'position': fields.Float,
})


alert_schema = api.model('Alert', {
    'id': fields.String(readOnly=True),
    'condition': fields.String,
    'value': fields.Float,
    'field': fields.String,
    'expiration_date': fields.DateTime,
    'alert_types': fields.List(fields.String),
    'message': fields.String,
    'position': fields.Nested(position_schema,  skip_none=True),
    'is_open': fields.Boolean,
    'has_sent_email': fields.Boolean,
    'has_sent_sms': fields.Boolean, 
})


alert_event_schema = api.model('AlertEvent', {
    'id': fields.String(readOnly=True),
    'created_date': fields.DateTime, 
    'value': fields.Float,
    'position': fields.Nested(position_schema,  skip_none=True),
    'alert': fields.Nested(alert_schema, skip_none=True)
})


user_schema = api.model('User', {
    'id': fields.String(readOnly=True),
    'first_name': fields.String,
    'role': fields.String,
    'last_name': fields.String,
    'phone_number': fields.String,
    'requires_two_factor': fields.Boolean,
    'enable_sound_alerts': fields.Boolean,
    'enable_voice_alerts': fields.Boolean,
    'email': fields.String,
    'confirmed_emails': fields.List(fields.String),
})


brokerage_connection_schema = api.model('BrokerageConnection', {
    'ib_username': fields.String,
    'status': fields.String,
})


alerts_ns = api.namespace(
    path='/alerts', name='Alerts', description='Alerts')
alert_events_ns = api.namespace(
    path='/alert_events', name='Alert Events', description='Alert Events')
positions_ns = api.namespace(
    path='/positions', name='Positions', description='Positions')
auth_ns = api.namespace(
    path='/auth', name='Auth', description='Auth')
user_ns = api.namespace(
    path='/user', name='User', description='User')
public_globals_ns = api.namespace(
    path='/public_globals', name='Public Globals')
webhooks_ns = api.namespace(
    path='/webhooks', name='Webhooks')
brokerage_connection_ns = api.namespace(
    path='/brokerage_connection', name='Brokerage Connection')
admin_ns = api.namespace(
    path='/admin', name='Admin', description='Admin')


@public_globals_ns.route('/')
class PublicGlobalsResource(Resource):

    def get(self):
        """Retrieve useful global variables"""
        public_globals = PublicGlobals().data()
        return utils.dumps_response(public_globals)


@webhooks_ns.route('/trading_service')
class WebhooksTradingServiceResource(Resource):

    def post(self):
        """Create a trading service webhook request"""
        utils.logger().info(request.json)
        return utils.dumps_response({'status': 'ok'})


@auth_ns.route('/')
class AuthResource(Resource):

    def post(self):
        '''Create an access token with an email and password'''
        email = request.json.get('email')
        password = request.json.get('password')
        user = User.objects(email=email).first()
        if user and user.is_correct_password(password):
            access_token = create_access_token(identity=str(user.id))
            user.claim_account()
            session['user_id'] = str(user.id)
            resp = {'access_token': access_token}
            if (user.requires_two_factor and not 
                    session.get('two_factor_verified') == str(user.id)):
                user.request_two_factor_token()
                resp['requires_two_factor'] = True
            return resp
        abort(401)

    def put(self):
        '''Update a password with a token'''
        token = request.json.get('token')
        user = User.get_user_from_reset_token(token)
        if user:
            # we want to assume they've confirmed the email here
            if user.email not in user.confirmed_emails:
                user.confirmed_emails.append(user.email)
                user.save()
            password = request.json.get('password')
            password_confirm = request.json.get('password_confirm')
            if password == password_confirm:
                user.set_password(password)
                user.password_changed()
                return {'email': user.email}
            return {'message': 'Passwords do not match'}, 400
        return {'message': 'This link has expired'}, 400

    def delete(self):
        '''Logout a user'''
        session['user_id'] = None
        session['two_factor_verified'] = None
        return {'message': 'logged out'}, 200


@auth_ns.route('/two_factor', doc=False)
class Auth2faResouce(Resource):

    def post(self):
        '''Request a 2fa code'''
        g.user.request_two_factor_token()
        return {'status': 'success'}


@auth_ns.route('/two_factor/validate', doc=False)
class AuthVerifyResouce(Resource):

    def post(self):
        '''Validate a 2fa code'''
        code = request.json.get('code')
        if g.user.validate_two_factor_token(code):
            session['two_factor_verified'] = str(g.user.id)
            return {'status': 'success'}
        abort(401)


@auth_ns.route('/change')
class AuthPasswordChangeResouce(Resource):

    @user_auth_required
    def put(self):
        '''Update a password with current password'''
        current_password = request.json.get('current_password')
        if g.user.is_correct_password(current_password):
            password = request.json.get('password')
            password_confirm = request.json.get('password_confirm')
            if password == password_confirm:
                g.user.set_password(password)
                g.user.password_changed()
                return {'message': 'Changed'}
            return {'message': 'Passwords do not match'}, 400
        return {'message': 'Password is incorrect'}, 400


@auth_ns.route('/reset')
class AuthResetResouce(Resource):

    def post(self):
        '''Create a password reset request'''
        email = request.json.get('email')
        user = User.objects(email=email).first()
        if user:
            user.send_password_reset()
        return {'status': 'success'}


@auth_ns.route('/confirm/email', doc=False)
class AuthConfirmEmail(Resource):

    def post(self):
        '''Confirm email with a token'''
        token = request.json.get('token')
        user = User.get_user_from_reset_token(token)
        if user:
            user.confirmed_emails.append(g.user.email)
            user.save()
            return {'message': 'Confirmed'}
        return {'message': 'This link has expired'}, 400

    @user_auth_required
    def put(self):
        '''Resend Confirm email with a token'''
        new_email = request.json.get('email')
        if new_email and new_email != g.user.email:
            if g.user.is_email_available(new_email):
                g.user.email = new_email
                g.user.save()
            else:
                abort(400, 'Email not available.')
        g.user.send_confirm_email()
        return {'message': 'Resent'}


@user_ns.route('/')
class UserResource(Resource):

    @api.marshal_with(user_schema)
    @user_auth_required
    def get(self):
        '''Retrieve the current user'''
        return g.user

    @api.marshal_with(user_schema)
    @user_auth_required
    def put(self):
        '''Update the current user'''
        data = request.json
        fields = data.keys()
        user = g.user

        first_name = request.json.get('first_name')
        if first_name:
            g.user.first_name = first_name

        last_name = request.json.get('last_name')
        if last_name:
            g.user.last_name = last_name

        phone_number = request.json.get('phone_number')
        if phone_number:
            g.user.set_phone_number(phone_number)

        email = request.json.get('email')
        if email and email != g.user.email:
            usable, error = User.is_email_usable(email, g.user)
            if usable:
                g.user.set_email(email)
                g.user.send_confirm_email()
            else:
                abort(400, error)

        enable_voice_alerts = request.json.get('enable_voice_alerts')
        if enable_voice_alerts == True:
            g.user.enable_voice_alerts = True
        elif enable_voice_alerts == False:
            g.user.enable_voice_alerts = False

        enable_sound_alerts = request.json.get('enable_sound_alerts')
        if enable_sound_alerts == True:
            g.user.enable_sound_alerts = True
        elif enable_sound_alerts == False:
            g.user.enable_sound_alerts = False

        requires_two_factor = request.json.get('requires_two_factor', False) 
        if requires_two_factor == True or requires_two_factor == False:
            g.user.requires_two_factor = requires_two_factor
            g.user.save()
            session['two_factor_verified'] = str(g.user.id)

        g.user.save()
        return g.user

    @api.marshal_with(user_schema, code=201)
    def post(self):
        '''Create a user'''
        phone_number = request.json.get('phone_number')
        email = request.json.get('email')
        password = request.json.get('password')
        if not phone_number or len(phone_number) < 10:
            abort(400, 'Phone Number must be 10 numbers')
        if len(password) < 6:
            abort(400, 'Password should be at least 6 characters')
        user = User.objects(email=email).first()
        if user:
            abort(400, 'User already exists.')

        usable, error = User.is_email_usable(email)
        if not usable:
            abort(400, error)

        user = User.create(
            phone_number=phone_number,
            email=email,
            password=password
        )
        user.send_confirm_email()
        return user, 201


@brokerage_connection_ns.route('/')
class BrokerageConnectionResource(Resource):

    @api.marshal_with(brokerage_connection_schema)
    @user_auth_required
    def get(self):
        '''Retrieve brokerage connection'''
        status = g.user.check_trading_data()
        data = {'status': status, 
            'ib_username': g.user.trading_account_username}
        return data

    @api.marshal_with(brokerage_connection_schema)
    @user_auth_required
    def post(self):
        '''Create a brokerage connection'''
        username = request.json.get('username') 
        password = request.json.get('password')
        trading_mode = request.json.get('trading_mode')
        if g.user.trading_account_token:
            g.user.stop_trading_data()
        status = g.user.start_trading_data(
            username, password, trading_mode)
        data = {'status': status,
            'ib_username': g.user.trading_account_username}
        return data

    @api.marshal_with(brokerage_connection_schema)
    @user_auth_required
    def delete(self):
        '''Delete a brokerage connection'''
        status = g.user.stop_trading_data()
        data = {'status': status,
            'ib_username': g.user.trading_account_username}
        return data

@alert_events_ns.route('/')
class AlertEventsResource(Resource):

    @api.marshal_list_with(alert_event_schema,  envelope=LIST_ENVELOPE)
    @user_auth_required
    def get(self):
        '''Retrieve all alerts events'''
        alert_events = AlertEvent.objects(user=g.user)
        return list(alert_events)


@positions_ns.route('/')
class PositionsResource(Resource):

    @api.marshal_list_with(position_schema,  envelope=LIST_ENVELOPE)
    @user_auth_required
    def get(self):
        '''Retrieve all positions'''
        positions = Position.objects(user=g.user, is_open=True)
        return list(positions)


@alerts_ns.route('/')
class AlertsResource(Resource):

    @api.marshal_list_with(alert_schema,  envelope=LIST_ENVELOPE)
    @user_auth_required
    def get(self):
        '''Retrieve all alerts'''
        alerts = Alert.objects(user=g.user)
        return list(alerts)

    @api.marshal_with(alert_schema)
    @user_auth_required
    def post(self):
        '''Create an alert'''
        position_id = request.json.get('position').get('id')
        position = Position.objects(id=position_id).first()
        alert = Alert.create(
            user=g.user,
            condition=request.json.get('condition'), 
            value=float(request.json.get('value')), 
            field=request.json.get('field'), 
            expiration_date=request.json.get('expiration_date'), 
            alert_types=request.json.get('alert_types'), 
            message=request.json.get('message'), 
            position=position,
        )
        return alert


@alerts_ns.route('/<string:id>')
class AlertResource(Resource):

    @api.marshal_with(alert_schema)
    @user_auth_required
    def get(self, id):
        '''Retrieve an alert'''
        alert = Alert.objects(user=g.user, id=id).first()
        return alert

    @user_auth_required
    def delete(self, id):
        '''Delete an alert'''
        alert = Alert.objects(user=g.user, id=id).first()
        alert.remove()
        return {'message': 'Deleted'}

    @user_auth_required
    @api.marshal_with(alert_schema)
    def put(self, id):
        '''Update an alert'''
        alert = Alert.objects(user=g.user, id=id).first()
        position_id = request.json.get('position').get('id')
        position = Position.objects(id=position_id).first()
        alert.condition = request.json.get('condition')
        alert.value = float(request.json.get('value'))
        alert.field = request.json.get('field')
        alert.expiration_date = request.json.get('expiration_date')
        alert.alert_types = request.json.get('alert_types')
        alert.message = request.json.get('message')
        alert.position = position
        alert.save()
        return alert


@admin_ns.route('/users', doc=False)
class AdminUserResource(Resource):

    @user_auth_required
    @special_role_required('admin')
    @api.marshal_list_with(user_schema,  envelope=LIST_ENVELOPE)
    def get(self):
        """List all users"""
        return list(User.objects().order_by('-id'))

    @user_auth_required
    @special_role_required('admin')
    def post(self):
        """Create an auth token for a user"""
        id = request.json.get('id') 
        user = User.objects(id=id).first()
        if user:
            access_token = create_access_token(identity=str(user.id))
            session['user_id'] = str(user.id)
            session['two_factor_verified'] = str(user.id)
            response = {'access_token': access_token}
            return response
        abort(404)


