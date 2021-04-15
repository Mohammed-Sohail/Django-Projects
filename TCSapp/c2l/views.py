from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from .forms import RegForm
from .models import c2lUser
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.models import User
import asyncio,json,datetime
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData


def home(request):
    return render(request,"index.html",{'title':'Home'})

def register(request):
    template = 'register.html'
    c2l=c2lUser()
    if request.method == 'POST':
            ins = RegForm(request.POST)
            # ins=request.POST
            if ins.is_valid():
                if User.objects.filter(username=ins.cleaned_data['username']).exists():
                    return render(request, template, {
                    'form': ins,
                    'error_message': 'Username already exists.'
                })
                # print("Success")
                else:
                # Create the user:
                    user = User.objects.create_user(
                    ins.cleaned_data['username'],
                    ins.cleaned_data['email'],
                    ins.cleaned_data['password1'],
                    )
                    uname=ins.cleaned_data['username']
                    print(uname)
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
        # ins=request.POST

    return render(request,'registers.html',{'title':'Register','form':ins})


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

def comment(request):
    template='comments.html'
    cmts={}
    cur=datetime.datetime.now()
    if request.method == 'POST':
        username = request.POST['username']
        mail = request.POST['mail']
        sub = request.POST['sub']
        body = request.POST['body']
        date = cur.strftime("%d-%m-%y")
        time = cur.strftime("%H:%M:%S")
        async def run():
            events = EventHubProducerClient.from_connection_string(conn_str="Endpoint=sb://traileventhub.servicebus.windows.net/;SharedAccessKeyName=all;SharedAccessKey=UGHwK6OuNPrKj5ehj745BotXr2rMAh/C/1ScynAP7AQ=", eventhub_name="rg2input")
            async with events:
                event_data_batch = await events.create_batch()
                cmts={
                        'username' : username,
                        'mail' : mail,
                        'comment_subject' : sub,
                        'comment':body,
                        'date_posted':date,
                        'time_posted':time
                    }
                s= json.dumps(cmts)
                event_data_batch.add(EventData(s))
                await events.send_batch(event_data_batch)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(run())
        return render(request, template)
    else:
        return render(request, template)

    

def profile(request):
    return render(request,'profile.html')

def log_out(request):
    return render(request,'logout.html')

def about(request):
    return render(request,'about.html')