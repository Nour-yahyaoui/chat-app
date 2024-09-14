# views.py
from django.shortcuts import render, redirect
from .models import User, Inv, Friends, Messages, Posts
from django.db.models import Q


def logout(request):
    if 'auth' in request.session:
        if 'registered' in request.session:
            del request.session['registered']
        if 'logedin' in request.session:
            del request.session['logedin']
        del request.session['auth']
        del request.session['name']
        del request.session['email']
    return redirect('login')

def login(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(name=name).exists():
            user = User.objects.get(name=name)
            if user.password == password:
                request.session['name'] = name
                request.session['email'] = email
                request.session['auth'] = True
                request.session['logedin'] = True
                request.session.set_expiry(2592000) 
                if 'registered' in request.session:
                    del request.session['registered']
                current_user = User.objects.get(name=request.session['name'])
                friends = Friends.objects.filter(user=current_user).values_list('friend', flat=True)
                users = User.objects.exclude(name=current_user.name).exclude(id__in=friends)
                return redirect('home')
            else:
                return render(request, 'login.html', {'error': 'Incorrect password'})
        else:
            return render(request, 'login.html', {'error': 'User does not exist'})
    return render(request, 'login.html')

def profile(request, profile_name):
    if request.method == 'POST':
        if request.session['name'] ==  profile_name:
            name = request.POST.get('name')
            bio = request.POST.get('bio')
            email = request.POST.get('email')
            password = request.POST.get('pass')
            
            user = User.objects.get(name=profile_name)
            
            user.name = name
            user.password = password
            user.bio = bio
            user.email = email
            request.session['email'] = email
            request.session['auth'] = True
            request.session.set_expiry(2592000) 
            user.save()
        else:
            return redirect('home')
        
    profile = User.objects.get(name=profile_name)
    return render(request, 'profile.html', {'profile': profile})

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(name=name).exists():
            return render(request, 'register.html', {'error': 'User already exists'})
        user = User(name=name, email=email, password=password)
        user.save()
        request.session['name'] = name
        request.session['email'] = email
        request.session['auth'] = True
        request.session['registered'] = True
        request.session.set_expiry(2592000) 
        if 'logedin' in request.session:
            del request.session['logedin']
        current_user = User.objects.get(name=request.session['name'])
        friends = Friends.objects.filter(user=current_user).values_list('friend', flat=True)
        users = User.objects.exclude(name=current_user.name).exclude(id__in=friends)
        return redirect('home')
    return render(request, 'register.html') 

def home(request):
    current_user = User.objects.get(name=request.session['name'])
    friends = Friends.objects.filter(Q(user=current_user) | Q(friend=current_user)).values_list('friend', flat=True)
    users = User.objects.exclude(name=current_user.name).exclude(id__in=friends)
    posts = Posts.objects.all().order_by('-date')
    return render(request, 'home.html', {'users': users, 'posts':posts})

def addpost(request):
    if request.method == 'POST':
        author = User.objects.get(name=request.session['name'])
        text = request.POST.get('text')
        post = Posts(author=author, text=text)
        post.save()
        
    return redirect('home')
    
def search_view(request):
    if request.method == 'POST':
        q = request.POST.get('q')
        searchs = User.objects.filter(name__icontains=q) | User.objects.filter(email__icontains=q)
        current_user = User.objects.get(name=request.session['name'])
        friends = Friends.objects.filter(Q(user=current_user) | Q(friend=current_user)).values_list('friend', flat=True)
        searchs = searchs.exclude(id__in=friends).exclude(name=current_user.name)
        return render(request, 'home.html', {'userrs': searchs})
    return redirect('home')

def invitations(request):
    if 'auth' in request.session:
        if request.method == 'GET':
            current_user = User.objects.get(name=request.session['name'])
            invitations = Inv.objects.filter(reciver=current_user)
            return render(request, 'invitations.html', {'invitations': invitations, 'username': current_user.name})
    return redirect('home')

def delete(request, inv):
    if request.method == 'GET':
        try:
            invitation = Inv.objects.get(pk=inv)
            invitation.delete()
        except Inv.DoesNotExist:
            # Handle the case where the invitation doesn't exist
            pass
        
        reciv = User.objects.get(name=request.session['name'])
    invitations = Inv.objects.filter(reciver=reciv.id)
    return render(request, 'invitations.html', {'invitations': invitations})

def accept(request, inv):
    if request.method == 'GET':
        try:
            invitation = Inv.objects.get(pk=inv)
            if not Friends.objects.filter(Q(user=invitation.sender, friend=invitation.reciver) | Q(user=invitation.reciver, friend=invitation.sender)).exists():
                friend1 = Friends(user=invitation.sender, friend=invitation.reciver)
                friend1.save()
                friend2 = Friends(user=invitation.reciver, friend=invitation.sender)
                friend2.save()
            invitation.delete()
        except Inv.DoesNotExist:
            # Handle the case where the invitation doesn't exist
            pass
    return redirect('home')

def add(request, friendid):
    if 'auth' in request.session:
        if request.method == 'GET':
            current_user = User.objects.get(name=request.session['name'])
            friend_user = User.objects.get(id=friendid)
            if not Inv.objects.filter(sender=current_user, reciver=friend_user).exists() and not Inv.objects.filter(sender=friend_user, reciver=current_user).exists() and not Friends.objects.filter(friend=current_user, user=friend_user).exists() and not Friends.objects.filter(friend=friend_user, user=current_user).exists():
                inv = Inv(sender=current_user, reciver=friend_user)
                inv.save()
            else:
                # Handle the case where the invitation already exists
                pass
    return redirect('home')

def friends(request):
    if 'auth' in request.session:

        current_user = User.objects.get(name=request.session['name'])
        current_user = current_user.id
        friends = Friends.objects.filter(Q(user=current_user) | Q(friend=current_user))
        friends_list = []
        for friend in friends:
            if friend.user == current_user:
                friends_list.append(friend.friend)
            else:
                friends_list.append(friend.user)
        return render(request, 'friends.html', {'friends': friends_list})
    return redirect('login')

def message(request, friend_id):
    current_user = User.objects.get(name=request.session['name'])
    friend = User.objects.get(pk=friend_id)
    messages = Messages.objects.filter((Q(sender=current_user, reciver=friend) | Q(sender=friend, reciver=current_user))).order_by('sended')
    if request.method == 'POST':
        msg = request.POST.get('message')
        if msg:
            message = Messages(sender=current_user, reciver=friend, msg=msg)
            message.save()
    return render(request, 'message.html', {'friend': friend, 'messages': messages, 'current_user': current_user})