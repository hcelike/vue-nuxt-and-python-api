import json

from flask import *
from flask_socketio import join_room, leave_room
from flask_socketio import SocketIO, emit
from flask_restx import marshal

from base_app import *
from config import *
from trading_service import TradingService
from position import Position
import utils
from alert import Alert
from alert_event import AlertEvent
from api import alert_schema, alert_event_schema, position_schema

# need to monkey patch eventlent 
# on the server to not block the app
# but not on local development server
if not TEST:
    import eventlet
    eventlet.monkey_patch()
    async_mode = 'eventlet'
else:
    async_mode = 'threading'
    

socketio = SocketIO(cors_allowed_origins="*", async_mode=async_mode)
logger = utils.logger()


@socketio.on('connect')
def connect(message=None):
    try:
        user = load_user_from_session(session)
    except Exception as e:
        user = None
    if user:
        
        logger.info("Client connected: sid {}".format(request.sid))
        user.websocket_session_id = request.sid
        user.save()
    emit('event', {'data': 'Connected'})
    logger.info("Client connected")


@socketio.on('disconnect')
def disconnect():
    try:
        user = load_user_from_session(session)
    except Exception as e:
        user = None
    if user:
        user.websocket_session_id = None
        user.save()
    logger.info("Client disconnected")


def parse_message(message):
    if isinstance(message, str):
        message = json.loads(message)
    logger.info(type(message))
    token = message.get('token')
    data = message.get('data')
    user = User.objects(trading_account_token=token).first()
    trading_account_username = user.trading_account_username if user else None
    return token, data, user 


@socketio.on('error')
def handle_error(message):
    """Receive error messages about the IB/TWS instance"""
    token, data, user = parse_message(message)
    if user:
        msg = {'ib_username': user.trading_account_username, 'message': data}
        emit(
            'brokerage_connection_event', 
            msg,
            room=user.websocket_session_id
        )
    

@socketio.on('position')
def handle_position(message):
    """Receive position data from the IB/Risk websocket connection,  
    store the new positions, check for alerts, and 
    send to the right user on the frontend""" 
    logger.info(message)
    token, data, user = parse_message(message)
    
    if user:
        alerts = Alert.objects(user=user)
        original_number_alerts = alerts.count() 
        positions = Position.create_positions(user, data) 
        position_data_formatted = marshal(list(positions), position_schema)
        
        #logger.info([user, 'EMIT to', user.websocket_session_id])
        emit(
            'frontend_position', 
            position_data_formatted, 
            room=user.websocket_session_id
        )

        for alert in alerts:
            alert_event = alert.check()
            if alert_event:  
                alerts = Alert.objects(user=user)
                alert_events = AlertEvent.objects(user=user)
                alert_data_formatted = marshal(list(alerts), alert_schema)
                alert_events_data_formatted = marshal(
                    list(alert_events), alert_event_schema)
                alert_event_data_formatted = marshal(
                    alert_event, alert_event_schema)
                emit(
                    'frontend_alerts', 
                    alert_data_formatted, 
                    room=user.websocket_session_id
                )
                emit(
                    'frontend_alert_events', 
                    alert_events_data_formatted, 
                    room=user.websocket_session_id
                )
                emit(
                    'frontend_alert_event', 
                    alert_event_data_formatted, 
                    room=user.websocket_session_id
                )

        alerts = Alert.objects(user=user)
        alert_data_formatted = marshal(list(alerts), alert_schema)
        if alerts.count() != original_number_alerts:
            emit(
                'frontend_alerts', 
                alert_data_formatted, 
                room=user.websocket_session_id
            )
             
    return {
        "status": "success", 
        "position": data, 
        "token": token,
    }


