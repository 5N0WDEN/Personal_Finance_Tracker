from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
import configparser
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Content, Email, To, Content, TemplateId, Substitution
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
        config.read('config.ini')
        #self.APIKEY = config.get('SETTINGS', 'APIKEY', fallback=None)
        #self.APIKEY = "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" #old key 
        self.APIKEY = "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"
        #self.from_email = config.get('SETTINGS', 'FROM', fallback=None)
        self.from_email = "personalfinancetracker007@gmail.com"
    
    def send_email(self, email, subject, content):
        if self.APIKEY and self.from_email and len(email) > 0:
            content = Content(
                mime_type="text/html",
                content=f"<div class='container'><h2 align='Center'>Verify your account</h2><p>Please click the button below to verify your account or activate your account:</p><a href={verification_link} class='btn'>Verify Your Account</a><p>Thank you!</p><p>Sincerely,<br>Personal Finance Tracker</p></div>"
            )
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
                content=f"<div class='container'><h2 align='Center'>Verify your account</h2><h3>Dear {username},</h3><p>Please click the button below to verify your account or activate your account:</p><button><a href='{activate_url}'>Verify Your Account</a></button><p>Thank you!</p><p>Sincerely,<br>Personal Finance Tracker</p></div>"
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