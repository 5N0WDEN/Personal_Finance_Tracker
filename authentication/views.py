from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email 
from django.contrib import messages
from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .utils import AppTokenGenerator, EmailSender
import time
from django.contrib import auth

class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error':'Email is invalid'}, status = 400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error':'sorry email is used choose another one'}, status = 409)
        return JsonResponse({'email_valid': True})

class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error':'username should only contains alphanumeric characters'}, status = 400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'sorry username is used choose another one'}, status = 409)
        return JsonResponse({'username_valid': True})

class RegisterationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
    
    def post(self, request):
        #GET USER DATE
        #VALIDATE
        #create a user account

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues' : request.POST,
        }
    
        if not User.objects.filter(username=username).exists() or not User.objects.filter(email=email).exists():
            if len(password) < 6:
                messages.error(request, "Password too short")
                return render(request, 'authentication/register.html', context)
            
            user = User.objects.create_user(username=username, email=email)
            user.set_password(password)
            user.is_active = False
            user.save()

            # path_to_view
            # -->getting domain we are on
            # -->relative url to verification
            # -->encode uid
            # -->token
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain
            timestamp = int(time.time())
            token_generator = AppTokenGenerator()
            link = reverse('activate', kwargs = {'uidb64' : uidb64, 'token': token_generator._make_url_value(user, timestamp)})
            
            #activate_url = f"http://{domain}{link}"
            activate_url = f"http://192.168.0.213:8000/{link}"
            #print(activate_url)
            email_body = f"Hi, {user.username}. Please use this link to verify your account\n {activate_url}"
            email_subject = "Activate your account"
            # add email using sendGrid or may sendGrid is not working at night
            emailsender = EmailSender() 
            #emailsender.send_verification_mail(email, email_subject, activate_url, user.username)
            #return redirect(activate_url)
            messages.success(request, "Account successfully created")
            messages.info(request, "You'll get verification link shortly")
            #return render(request, 'authentication/register.html')
            return redirect(activate_url)
        messages.error(request, "Username or Email is already registered")
        return render(request, 'authentication/register.html')
        '''messages.success(request, "Success whatapp success")
        messages.warning(request, "Success whatapp warning")
        messages.info(request, "Success whatapp info")
        messages.error(request, "Success whatapp error")
        return render(request, 'authentication/register.html')'''

class VerificationView(View):
    def get(self, request, uidb64, token):

        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)
                
            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()
            messages.success(request, "Account activated successfully")
            return redirect('login')

        except Exception as ex:
            pass
        messages.error(request, "There's some issue")
        return redirect('login')
    

class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        if username and password:
            user = auth.authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, f"Welcome, {user.username} you are now logged in")
                    return redirect('expenses')
                messages.error(request, "Account is not active, please check your email")
                return render(request, 'authentication/login.html')
            messages.error(request, "Invalid credintials, try again")
            return render(request, 'authentication/login.html')
        messages.error(request, "Please fill all fields")
        return render(request, 'authentication/login.html')

class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('login')




