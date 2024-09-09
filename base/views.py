from django.shortcuts import render
from django.shortcuts import get_object_or_404,redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout

from .models import *
from .forms import *

def index(request):
    context ={'Status':'working'}
    return render(request, "index.html", context)

def homepage(request):
    users = User.objects.filter(participant = True)
    events = Event.objects.all()
    context = {'users':users , 'events':events}
    return render(request, "homepage.html" , context)  


@login_required(login_url='login')    
def profile(request, pk):
    user = get_object_or_404(User , pk=pk)
    context = {'user': user}
    return render(request, "profile.html", context)

@login_required(login_url='login')    
def account(request):
    user = request.user
    
    # participated_in = Event.objects.filter(participants = user.id)
    # + many = True
    #   added related name to Event model and modified template {% for event in user.events.all %} =)

    context = {'user': user}
    return render(request, "account.html", context)


def eventpage(request, pk):
    event =  get_object_or_404(Event , pk=pk)
    # we want to know if the user is registered or not
    registered = False
    try : 
        myevents = Event.objects.filter(participants = request.user.id)
        if event in myevents:
            registered = True
        submitted = Submission.objects.filter(event = event , participant = request.user).exists()
        sub = Submission.objects.get(event = event , participant = request.user)
        # registered= request.user.events.filter(id=event.id).exists() #better check if anon user breaks
    except :
        sub = ""
        submitted =False
    context = {'event':event , 'registered':registered ,'submitted': submitted,"sub":sub}
    return render(request, "event.html",context)

@login_required(login_url='login')    
def registration_confirmation(request, pk):
    event =  get_object_or_404(Event , pk=pk)
    context = {'event':event}
    if request.method == 'POST':
        event.participants.add(request.user)
        return redirect('event_page', pk = event.pk)
    return render(request, "event_confirmation.html", context)

@login_required(login_url='login')    
def project_submission(request,pk):
    event = get_object_or_404(Event, pk=pk)
    form = SubmissionForm()
    
    if request.method == 'POST':
        form = SubmissionForm(request.POST) #initial={'event':event, 'participant':request.user} dosnt get sent to server =(
        if form.is_valid():
            submission = form.save(commit=False)
            submission.participant=request.user #fill the user details implicitly
            submission.event=event
            form.save()
            return redirect('account')
    context = {'event': event, 'form': form}
    return render(request, "submit_form.html", context)    

@login_required(login_url='login')    
def updated_submission(request,pk):
    try : 
        Sub = get_object_or_404(Submission,pk=pk)
        event = Sub.event
        if Sub.participant == request.user :
            form=SubmissionForm(instance=Sub)
            if request.method == 'POST':
                form = SubmissionForm(request.POST, instance=Sub)
                if form.is_valid():
                    form.save()
                    return redirect('account')

            
            context = {'event': Sub.event, 'form': form}            
            return render(request,"submit_form.html", context)  
        else: 
            context = {"message" : "You dont have permission"}       
            return render(request,"error.html ",context)
    except  : 
        context = {"message" : "Does not exist"}       
        return render(request,"error.html ",context)   



       




def login_page(request):
    page = 'login'
    if request.method == 'POST':
        user = authenticate(
            email=request.POST['email'],
        password=request.POST['password']
        )
        if user is not None :
            login(request, user)
            return redirect('homepage')

    context = {'page':page}
    return render(request,"authenticate.html",context)

def logout_f(request):
    logout(request)
    return redirect('login')


def register_page(request):
    form = CustomUserCreationForum
    if request.method == 'POST':
        form = CustomUserCreationForum(request.POST)
        if form.is_valid():
                form.save()
                return redirect('login')
    page = 'register'
    context = {'page':page, 'form': form}
    return render(request,"authenticate.html",context)    