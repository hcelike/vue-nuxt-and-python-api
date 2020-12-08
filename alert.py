from models import *
from config import * 
import utils
from alert_event import AlertEvent
from position import Position


@utils.logged
class Alert(DynamicDocument):
    """Class represents a trading alert"""
    user = ReferenceField('User')
    condition = StringField()
    value = FloatField()
    field = StringField()
    expiration_date = DateTimeField()
    alert_types = ListField(StringField(), default=[])
    message = StringField()
    position = ReferenceField('Position')
    alert_event = ReferenceField('AlertEvent')
    is_open = BooleanField(default=True)
    has_sent_email = BooleanField(default=False)
    has_sent_sms = BooleanField(default=False)

    @staticmethod
    def create(user, condition, value, field, 
               expiration_date, alert_types, message, position):
        alert = Alert(
            user=user,
            condition=condition, 
            value=value, 
            field=field, 
            expiration_date=expiration_date, 
            alert_types=alert_types, 
            message=message, 
            position=position
        )
        alert.save()
        return alert

    def remove(self): 
        self.is_open = False
        self.save()

    def should_trigger(self):
        should_alert = False
        position_value = getattr(self.position, self.field)

        # don't want to trigger if value is not a number
        if (not isinstance(position_value, float) and 
                not isinstance(position_value, int)):
            return False

        if self.condition == GREATER_THAN:
            should_alert = position_value > self.value
        elif self.condition == GREATER_THAN_OR_EQUAL_TO:
            should_alert = position_value >= self.value
        elif self.condition == LESS_THAN:
            should_alert = position_value < self.value
        elif self.condition == LESS_THAN_OR_EQUAL_TO:
            should_alert = position_value <= self.value
        return should_alert

    def check(self):
        alert_event = None
        if self.is_open and self.should_trigger() and not self.alert_event:
            value = getattr(self.position, self.field)
            alert_event = AlertEvent.create(
                user=self.user, 
                alert=self, 
                value=value
            )
            self.alert_event = alert_event
            self.save()
            self.send()
            self.remove()
        self.check_position_still_open()
        return alert_event

    def check_position_still_open(self):
        if not self.position.is_open:
            self.remove()

    def send(self):
        if self.message: 
            message = self.message
        else:
            message = str(self)
        message_data = {
            'link': DASHBOARD_ENDPOINT, 
            'message': message,
        }
        if 'sms' in self.alert_types and not self.has_sent_sms:
            self.has_sent_sms = True
            self.save()
            self.user.send_message(
                message_template='alert', 
                message_data=message_data, 
                medium='sms',
                alert=self,
            )

        if 'email' in self.alert_types and not self.has_sent_email:
            self.has_sent_email = True
            self.save()
            self.user.send_message(
                message_template='alert', 
                message_data=message_data, 
                medium='email',
                alert=self,
            )

    def __str__(self):
        condition = ' '.join(self.condition.split('_'))
        return "{} has gone {} {}".format(
            str(self.position), condition, self.value) 
        
            
    
 
