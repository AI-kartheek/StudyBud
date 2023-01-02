# from email import message
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Message, Room, User, Topic
from .forms import RoomForm, MyUserForm, UpdateUser 

# Create your views here.

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = MyUserForm()
    if request.method == 'POST':
        form = MyUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An Error occured during registration.")
    context = {'form': form}
    return render(request, 'base/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)
            if user is not None:
                next = request.GET.get('next')
                login(request, user)
                if next:
                    return redirect(next)
                return redirect('home')
            else:
                messages.error(request, 'Wrong password.')
        except:
            messages.error(request, "User doesn't exists")
    return render(request, 'base/login.html')


def logoutPage(request):
    logout(request)
    return redirect('home')


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    room_count = rooms.count()
    topics = Topic.objects.all()
    topics_count = topics.count()
    topics = topics[:5]
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {'rooms': rooms, 'room_count': room_count, 'topics': topics, 'topics_count': topics_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    topics = Topic.objects.all()
    topics_count = topics.count()
    topics = topics[:5]
    room_messages = user.message_set.all()
    context = {'user': user, 'rooms': rooms, 'topics': topics, 'topics_count': topics_count, 'room_messages': room_messages}  
    return render(request, 'base/userProfile.html', context)


@login_required(login_url='login') 
def updateUser(request):
    user = request.user
    form = UpdateUser(instance=user)
    if request.method == 'POST':
        form = UpdateUser(request.POST, request.FILES, instance=user)
        if form.is_valid:
            form.save()
            return redirect('user-profile', pk=user.id)
    return render(request, 'base/updateUser.html', {'form': form})


def room(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)    
    room_messages = room.message_set.all()
    room_participants = room.participants.all()
    context = {'room': room, 'room_messages': room_messages, 'participants': room_participants}
    return render(request, 'base/room.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic_name = " ".join([word.capitalize() for word in topic_name.split()])
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        return redirect('home')
    context = {'header': 'create', 'form': form, 'topics': topics}
    return render(request, 'base/roomForm.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('You are not allowed Here!')
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic_name = " ".join([word.capitalize() for word in topic_name.split()])
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.topic = topic
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    context = {'header': 'update', 'room': room, 'form': form, 'topics': topics}
    return render(request, 'base/roomForm.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('You are not allowerd Here!')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': 'Room', 'obj_msg': room})

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('You are not allowerd Here!')
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': 'Message', 'obj_msg': message})

def activity(request):
    room_messages = Message.objects.all()
    context = {'room_messages': room_messages}
    return render(request, 'base/activity.html', context)

def topics(request):
    topics = Topic.objects.all()
    context = {'topics': topics, 'topics_count': topics.count()}
    return render(request, 'base/topics.html', context)