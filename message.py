from models import *
from config import *

from public_globals import PublicGlobals


@utils.logged
class Message(DynamicDocument):

    date = DateTimeField(default=datetime.datetime.now)
    message = StringField()
    message_template = StringField()
    message_data = DictField(default={})
    subject = StringField()
    sender_data = DictField()
    medium = StringField()
    user = ReferenceField('User')
    alert = ReferenceField('Alert')
    attachments = ListField(FileField())
    recipients = ListField(StringField())

    def __init__(self, *args, **kwargs):
        """Construct the message and the subject if necessary"""
        DynamicDocument.__init__(self, *args, **kwargs)
        self.subject = self.get_subject() 
        self.message = self.get_message()

    def get_subject(self):
        """Get the subject of the message.

        Note: if no subject is given in the message_data,
        then the subject defaults to a pretty-printed verison
        of the message_template.
        """ 
        default_subject = ' '.join(self.message_template.split('_')).title()
        return self.message_data.get('subject', default_subject)

    def get_message(self):
        """Render a message using a jinja template.

        Note: The templates are in /templates/messages 
        and you can easily add another one. 
        """
        data = {}
        data['message_data'] = self.message_data
        data['sender_data'] = self.sender_data
        data['public_globals'] = PublicGlobals().__dict__
        template = 'messages/{}.html'.format(self.message_template)
        with Flask(__name__).app_context():
            rendered = render_template(template, **data)
        if self.medium == 'sms':
            # if the medium is an sms, we dont want all the style,
            # script, and other html tags,
            # only the text bits. 
            soup = BeautifulSoup(rendered)
            for s in soup(['script', 'style']):
                s.decompose()
            rendered = ' '.join(soup.stripped_strings)
        return rendered

    def send(self):
        """Send the message via the chosen medium"""
        if self.medium == 'email':
            utils.send_email(
                subject=self.subject,
                message=self.message,
                from_email=SUPPORT_EMAIL,
                to_email=self.recipients,
            )
        elif self.medium == 'sms':
            utils.send_sms(
                number=self.recipients,
                message=self.message,
            )
        else:
            raise Exception('Message medium not supported')
        self.save()
    

