import datetime

from models import *
from config import * 
import utils


@utils.logged
class AlertEvent(DynamicDocument):
    """Class represents an alert event"""
    user = ReferenceField('User')
    alert = ReferenceField('Alert')
    position = ReferenceField('Position')
    created_date = DateTimeField(default=datetime.datetime.utcnow)
    value = FloatField()
    
    @staticmethod
    def create(user, alert, value):
        alert_event = AlertEvent(
            user=user,
            alert=alert,
            position=alert.position,
            value=value,
        )
        alert_event.save()
        return alert_event

