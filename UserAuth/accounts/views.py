from accounts.models import Profile
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.
def home (request):
    return render (request , 'home.html')

def login_attempt(request):
    return render (request, 'login.html')

def register_attempt (request):
    if request.method == 'POST' :
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            if User.objects.filter(username = username).first():
              messages.success(request,'Username is taken.')
              return redirect('/register')
        
            if User.objects.filter(email = email).first():
              messages.success(request, 'Email is taken')
              return redirect('/register')
        
            user_obj = User(username = username, email=email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())

            profile_obj = Profile.objects.create(user = user_obj , auth_token = auth_token)
            profile_obj.save()
            send_mail_after_registration(email , auth_token)
            return redirect('/token')
            

        except Exception as e:
            print(e)

        

    return render(request , 'register.html')

def token_send (request):
    return render(request , 'token_send.html')

def success (request):
    return render(request , 'success.html')

def verify(request , auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
        if profile_obj:
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'You account is been verified')
            return redirect('/login')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)


def error_page(request):
    return render(request, 'error.html')   


def send_mail_after_registration(email,token):
    subject = "Your account needs to be verified"
    message = f'Hi paste your link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list)