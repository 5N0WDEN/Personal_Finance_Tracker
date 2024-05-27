from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
import configparser
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Content, Email, To, Content, TemplateId, Substitution
import os
import ssl 
ssl._create_default_https_context = ssl._create_default_https_context

class AppTokenGenerator(PasswordResetTokenGenerator):

    def _make_url_value(self, user, timestamp):
        return (text_type(user.is_active) + text_type(user.pk) + text_type(timestamp))
    
    def _check_url_value(self, user, timestamp):
        pass

#It's for the sendGrid
class EmailSender:
    def __init__(self) -> None:
        config = configparser.ConfigParser()
        config_file_path = os.path.join(os.path.dirname(__file__), 'config.ini')
        config.read(config_file_path)
        self.APIKEY = config.get('SETTINGS', 'APIKEY')
        self.from_email = config.get('SETTINGS', 'FROM') 
    
    def send_email(self, email, subject, content):
        if self.APIKEY and self.from_email and len(email) > 0:
            message = Mail(self.from_email, email, subject, content)
            try:
                sg = SendGridAPIClient(self.APIKEY)
                response = sg.send(message)
                print(f"Mail sent successfully!!! {response.status_code}")
            except Exception as e:
                print(e)

    def send_verification_mail(self, email, subject, activate_url, username):
        if self.APIKEY and self.from_email and len(email) > 0:
            content = Content(
                mime_type="text/html",
                content=f"<div class='container'>
                            <h2 align='Center'>Verify your account</h2>
                            <h3>Dear {username},</h3>
                            <h3>Please click the button below to verify your account or activate your account:</h3>
                            <button><a href={activate_url} class='btn'>Verify Your Account</a></button>
                            <h3>Thank you!</h3>
                            <h3>Sincerely,<br>Personal Finance Tracker</h3>
                        </div>"
            )
            message = Mail(self.from_email, email, subject, content)
            try:
                sg = SendGridAPIClient(self.APIKEY)
                response = sg.send(message)
                print(f"Mail sent successfully!!! {response.status_code}")
            except Exception as e:
                print(e)
        
    
'''if __name__ == '__main__':
    token_generator = AppTokenGenerator()'''