from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect, HttpResponse
from .models import Profile
# Create your views here.
def login_page(request):
    if request.method == 'post':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username=email)
        if user_obj.exists(): 
                messages.warning(request, 'Email already exist')
                return HttpResponseRedirect(request.path_info)

        if not user_obj[0].profile.is_email_verified:
            messages.warning(request, 'your account is not verified')
            return HttpResponseRedirect(request.path_info)


        user_obj = authenticate(username= email, password= password)
        if user_obj:
            login(request, user_obj)
            return redirect('/')

        messages.warning(request, 'Invalid Password')
        return HttpResponseRedirect(request.path_info)

    return render(request, 'accounts/login.html')

def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username=email)

        if user_obj.exists(): 
            messages.warning(request, 'eMAIL IS ALREADY EXIST')
            return HttpResponseRedirect(request.path_info)

        user_obj = User.objects.create(first_name=first_name, last_name=last_name, email=email, username = email)
        user_obj.set_password(password)
        user_obj.save()

        messages.warning(request, 'An email has been send to your mail')
        return HttpResponseRedirect(request.path_info)

    return render(request, 'accounts/register.html')

def activate_email(request, email_token):
    try:
        user = Profile.objects.get(email_token=email_token)
        user.is_email_verified = True
        user.save()
        return redirect('/')
    except Exception as e:
        return HttpResponse('Invalid Email Token')

