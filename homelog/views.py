from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib import auth



# Create your views here.
def home(request):
    return render(request,'home.html')




def login(request):
    if request.method == 'POST':
        user=auth.authenticate(username=request.POST['username'],password=request.POST['password'])
        if  user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            return render(request,'login.html',{'error':'Invalid User or Password'})
    else:
        return render(request,'login.html')


def conf_login(request, uidb64, token):
    if request.method == 'POST':
        user=auth.authenticate(username=request.POST['username'],password=request.POST['password'])
        if  user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            return render(request,'login.html',{'error':'Invalid User or Password'})
    else:
        return render(request,'login.html')

"""def signup(request):
   if request.method == 'POST':
        #user has info and wants homelog
        if request.POST['password'] == request.POST['confirm_password']:
            try:
                user=User.objects.get(username=request.POST['username'])
                return render(request,'signup.html',{'error':'User already exists !'})

            except User.DoesNotExist:
                user=User.objects.create_user(request.POST['username'],password=request.POST['password'])
                auth.login(request,user)
                return redirect('home')
        else:
            return render(request,'signup.html',{'error':'Password confirmation failed!'})
    else:
        #user wants to enter info
        return render(request,'signup.html')
"""
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('activate_email.html', {
                     'user': user,
                     'domain': current_site.domain,
                     'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                     'token': account_activation_token.make_token(user),
             })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request,'email_conf.html')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request)
        # return redirect('home')
        return render(request,'email_success.html')
    else:
        return HttpResponse('Activation link is invalid!')



def logout(request):
    if request.method=='POST':
        auth.logout(request)
        return redirect('home')
    return render(request,'logout.html')
