from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
import configparser
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Content, Email, To, Content, TemplateId, Substitution
import os
import ssl 
ssl._create_default_https_context = ssl._create_default_https_context
import threading

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
                content = f"""<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width, initial-scale=1.0'><title>Verify Your Account</title><style>body{{font-family:Arial, sans-serif;margin:0;padding:0;background-color:#f4f4f4;}}.container{{max-width:600px;margin:20px auto;padding:20px;background-color:#ffffff;border-radius:8px;box-shadow:0 0 10px rgba(0, 0, 0, 0.1);}}h1{{text-align:center;color:#007bff;}}p{{margin-bottom:15px;}}.btn{{display:inline-block;padding:10px 20px;background-color:#3498db;color:#ffffff;text-decoration:none;border-radius:5px;}}.btn:hover{{background-color:#2980b9;}}</style></head><body><div class='container'><h1>Verify Your Account</h1><p>Dear {username},</p><p>Please click the button below to verify your account or activate your account:</p><h3><a href='{activate_url}' class='btn'>Verify Your Account</a></h3><p>Thank you!</p><p>Sincerely,<br>Personal Finance Tracker</p></div></body></html>"""
            )
            threading.Thread(target=self.send_email, args=(email, subject, content), daemon=False).start()
    
    def send_password_reset_mail(self, email, subject, reset_url, username):
        if self.APIKEY and self.from_email and len(email) > 0:
            content = Content(
                mime_type="text/html",
                content=f"<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width, initial-scale=1.0'><title>Reset Your Password</title><style>body{{font-family:Arial, sans-serif;margin:0;padding:0;background-color:#f4f4f4;}}.container{{max-width:600px;margin:20px auto;padding:20px;background-color:#ffffff;border-radius:8px;box-shadow:0 0 10px rgba(0, 0, 0, 0.1);}}h1{{text-align:center;color:#007bff;}}p{{margin-bottom:15px;}}.btn{{display:inline-block;padding:10px 20px;background-color:#e74c3c;color:#ffffff;text-decoration:none;border-radius:5px;}}.btn:hover{{background-color:#c0392b;}}</style></head><body><div class='container'><h1>Reset Your Password</h1><p>Dear {username},</p><p>We received a request to reset your password. Please click the button below to reset it:</p><h3><a href='{reset_url}' class='btn'>Reset Your Password</a></h3><p>If you did not request a password reset, please ignore this email or contact support.</p><p>Thank you!</p><p>Sincerely,<br>Personal Finance Tracker</p></div></body></html>"
            )
            threading.Thread(target=self.send_email, args=(email, subject, content), daemon=False).start()

        
    
'''if __name__ == '__main__':
    token_generator = AppTokenGenerator()'''