import json
from functools import wraps
import datetime
import traceback
import random

import requests
from flask import *
from flask import g
from flask_cors import CORS
import flask_socketio
from flask_jwt_extended import (
    JWTManager, 
    verify_fresh_jwt_in_request,
    jwt_required, 
    get_jwt_identity,
    verify_jwt_in_request_optional,
    jwt_optional, 
    create_access_token,
    decode_token,
    get_current_user,
)
import mongoengine
import database

from models import *
import utils
from utils import dumps_response
from config import *
from public_globals import PublicGlobals
from user import User


app = Flask(__name__, subdomain_matching=True)

# disable to flask doesn't 404 or redirect on no trailing slash
app.url_map.strict_slashes = False 

app.config['SECRET_KEY'] = FLASK_SECRET_KEY
app.config['DEBUG'] = TEST

# removes X-mask dummy defaults in restplus
app.config['RESTPLUS_MASK_SWAGGER'] = False

app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 60 * 1000 * 10
# it's risky to have the JWT token in the query_string
# but we only do it for the pdf viewer which can't use headers
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'query_string']

# required for subdomains
app.config['SERVER_NAME'] = BASE_DOMAIN

# We use session cookies as XSS protection in addition to JWT in header 
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = None

CORS(app, supports_credentials=True)
jwt = JWTManager(app)


@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    """Return the user based on the correct jwt"""
    if identity:
        user = User.objects(id=identity).first()
        return user 


@app.before_request        
def get_platform_user():
    """this allows us to have the correct type of user methods
    available here in the main controller"""
    g.user = None
    try:
        user = None    
        verify_jwt_in_request_optional()
        user = get_current_user()
        if not user:
            raise Exception('JWT missing from request')

        # this requires all authenticated requests
        # come from the browser and not from nuxt server
        if str(user.id) != session.get('user_id'):
            raise Exception('XSS Protection session missing')

        g.user = user
    except Exception as e:
        if request.method != 'OPTIONS':
            current_app.logger.error('ERROR on Before Request: {} {} {}'.format(
                request.method, request.path, e))


@app.context_processor
def inject_public_globals():
    """This allows jinja templates to access public variables"""
    return dict(public_globals=PublicGlobals().__dict__)


def special_role_required(role_name):
    def inner_function(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            user = g.user
            if not user or not user.has_role(role_name):
                abort(401)
            return f(*args, **kwargs)
        return decorated
    return inner_function


def load_user_from_token(token):
    user = None
    try:
        id = decode_token(token)
        if id:
            user = User.objects(id=id).first()
    except Exception as e:
        print(e)
    return user


def load_user_from_session(session):
    user = None
    try:
        id = session.get('user_id')
        if id:
            user = User.objects(id=id).first()
    except Exception as e:
        print(e)
    return user
    

def user_auth_required_socketio(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = load_user_from_session(session)
        if not user:
            current_app.logger.error(
                'ERROR socketio auth: {} {}'.format(
                request.method, request.path))
            flask_socketio.disconnect()
        else:
            return f(*args, **kwargs)
    return decorated


def user_auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = g.user
        if not user:
            abort(401)
        if (user.requires_two_factor and 
                session.get('two_factor_verified') != str(user.id)
            ):
            current_app.logger.error('Failed two factor session')
            abort(403, "Two factor required") 
        return f(*args, **kwargs)
    return decorated


@app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(500)
def error(e):
    errors = {
        400: 'Missing a required parameter.',
        401: 'Credentials are invalid.',
        403: 'Forbidden',
        404: 'Page Not Found',
        500: 'Something has gone wrong, please contact ' + SUPPORT_EMAIL,
    }
    error = traceback.format_exc()
    try:
        code = e.code
        current_app.logger.error(error)
    except Exception as e:
        current_app.logger.error(e)
        code = 500
    if code == 500:
        utils.send_email(
            subject="Internal Server Error",
            message=error,
            from_email=SUPPORT_EMAIL,
            to_email=SUPPORT_EMAIL,
        )
    error_message = errors.get(code, 'Unknown Error')
    if code == 404:
        if 'www' in request.url:
            url = request.url.lstrip('http://www.')
            url = 'http://' + url
            return redirect(url)
    return dumps_response(dict(message=error_message)), code

