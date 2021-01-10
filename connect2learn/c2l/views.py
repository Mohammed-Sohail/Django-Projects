from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from .forms import RegForm
from .models import c2lUser
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.models import User

def home(request):
    return render(request,"index.html",{'title':'Home'})

def register(request):
    template = 'register.html'
    c2l=c2lUser()
    if request.method == 'POST':
            ins = RegForm(request.POST)
            if ins.is_valid():
                if User.objects.filter(username=ins.cleaned_data['username']).exists():
                    return render(request, template, {
                    'form': ins,
                    'error_message': 'Username already exists.'
                })
                else:
                # Create the user:
                    user = User.objects.create_user(
                    ins.cleaned_data['username'],
                    ins.cleaned_data['email'],
                    ins.cleaned_data['password1'],
                    )
                    uname=ins.cleaned_data['username']
                    c2l.username=ins.cleaned_data['username']
                    c2l.first_name=ins.cleaned_data['first_name']
                    c2l.last_name=ins.cleaned_data['last_name']
                    c2l.phone=ins.cleaned_data['phone']
                    c2l.address=ins.cleaned_data['address']
                    user.save()
                    c2l.save()
                    messages.success(request, f"Account Created for {uname}!")
                # redirect to accounts page:
                    return redirect('login')

    else:
        ins = RegForm()
    return render(request,'register.html',{'title':'Register','form':ins})


def log_in(request):
    template='login.html'
    if request.method == 'POST':
        # Process the request if posted data are available
        username = request.POST['username']
        password = request.POST['password']
        # Check username and password combination if correct
        user = authenticate(username=username, password=password)
        if user is not None:
            # Save session as cookie to login the user 
            login(request, user)
            return redirect('profile')
        else:
            # Incorrect credentials, let's throw an error to the screen.
            messages.warning(request, f"Invalid Username/Password")
            return render(request, template)
    else:
        # No post data availabe, let's just show the page to the user.
        return render(request, template)


def profile(request):
    return render(request,'profile.html')

def log_out(request):
    return render(request,'logout.html')

def about(request):
    return render(request,'about.html')