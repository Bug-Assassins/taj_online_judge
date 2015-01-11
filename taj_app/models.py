from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class user(models.Model) :
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    userid = models.CharField(max_length=15)
    email = models.CharField(max_length=200)
    usertype = models.IntegerField()
    image = models.FileField(upload_to='profile_pic/')