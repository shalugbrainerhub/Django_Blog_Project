from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.





class UserRegistration(models.Model):
    username=models.CharField(max_length=50, unique=True)
    email=models.EmailField()
    otp = models.PositiveIntegerField(blank=True, null=True)
    otp_timestamp = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.username




class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.title





class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content