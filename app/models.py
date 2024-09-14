from django.db import models
from datetime import datetime
from django.utils import timezone

class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField(max_length=200)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='/static/myapp/profile.png')
    bio = models.TextField(max_length=50, null=True, blank=True, default="this user don't created a bio ")

    def __str__(self):
        return self.name

class Messages(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    reciver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    msg = models.TextField()
    sended = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=False)

class Inv(models.Model):
    id = models.AutoField(primary_key=True)
    reciver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_invitations')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations')
    date = models.DateTimeField(default=timezone.now)

class Friends(models.Model):
    id = models.AutoField(primary_key=True)
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_of')

class Posts(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=100)
    pict = models.ImageField(upload_to='post_pictures/', null=True)
    date = models.DateTimeField(default=timezone.now)