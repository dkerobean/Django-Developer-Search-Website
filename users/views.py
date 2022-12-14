from django.shortcuts import render, redirect
from .models import Profile, Skill, Message
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.models import User
from django.contrib import messages
#from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, ProfileEditForm, ProfileEditForm, AddSkill, SendMessage
from django.contrib.auth.decorators import login_required
from .utils import searchProfiles
from django.db.models import Q



def profiles(request):

    search_query, profiles = searchProfiles(request)

    context = {
        'profiles': profiles,
        'search_query':search_query
    }

    return render(request, 'users/profiles.html', context)


@login_required(login_url='login')
def userProfile(request, pk):
    user = Profile.objects.get(id=pk)
    skill_desc = user.skill_set.exclude(description__exact="")
    skill_nodesc = user.skill_set.filter(description__exact="")
    context = {
        'user':user,
        'skill_desc':skill_desc,
        'skill_nodesc':skill_nodesc
    }
    return render(request, 'users/user_profile.html',context)


def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username= username)
        except:
            messages.error(request, 'Username does not exist')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET  else 'account')
        else:
            messages.error(request, 'Username Or Password Is Incorrect')

    context = {
        'page':page
    }

    return render(request,'users/login_register.html',context);


def logoutUser(request):
    logout(request)
    messages.info(request, 'Logout Success')
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'Registered Successfull')

            login(request, user)
            return redirect('edit-account')


    context = {
        'page':page,
        'form':form
    }

    return render(request, 'users/login_register.html',context)


@login_required(login_url='login')
def usersAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    context = {
    'profile': profile,
    'skills': skills,
    'projects': projects,
    }
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileEditForm(instance=profile)

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated Successfully')
            return redirect('account')

    context = {
        'form':form
    }

    return render(request, 'users/profile_form.html',context)


@login_required(login_url='login')
def addSkill(request):
    profile = request.user.profile
    form = AddSkill()

    if request.method == 'POST':
        form = AddSkill(request.POST)
        skill = form.save(commit=False)
        skill.owner = profile
        skill.save()
        messages.success(request, 'Skill Added Successfully')
        return redirect('account')

    context = {
        'form':form
    }
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = AddSkill(instance=skill)

    if request.method == 'POST':
        form = AddSkill(request.POST, instance = skill)
        form.save()
        messages.success(request,'Skill Updated!')
        return redirect('account')

    context = {
        'form':form
    }
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request,'Skill Deleted!')
        return redirect('account')

    context = {
        'object':skill
    }

    return render(request, 'delete_file.html', context )


@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()

    context = {
        'messageRequests':messageRequests,
        'unreadMessages':unreadCount
    }
    return render(request, 'users/inbox.html', context)


@login_required(login_url='login')
def viewMessage(request, pk):
    profile = request.user.profile
    userMessages = profile.messages.get(id=pk)

    if userMessages.is_read == False:
        userMessages.is_read = True
        userMessages.save()

    context = {
    'message':message
    }
    return render(request, 'users/message.html',context)


def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = SendMessage()

    try:
         sender = request.user.profile
    except:
         sender = None

    if request.method == 'POST':
        form = SendMessage(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = message.email

            message.save()

            messages.success(request, 'Mesage sent!')
            return redirect('user-profile', pk=recipient.id)

    context = {
        'recipient': recipient,
        'form':form,
        'recipient':recipient
    }

    return render(request, 'users/message_form.html', context)
