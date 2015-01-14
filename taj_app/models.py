from django.db import models
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session

# Created by Ashish Kedia, ashish1294@gmail.com
# Created on 13th Jan, 2015
# Last Modefied on 13th Jan, 2015

'''You are not haunted by the war, you miss it!
- Sherlock Holmes, Season 1'''
class user(models.Model) :
    STUDENT = 0
    TEACHER = 1
    ADMIN = 2
    ACCOUNT_TYPE_CHOICES = (
        (STUDENT, 'Student'),
        (TEACHER, 'Teacher'),
        (ADMIN, 'Admin'),
    )

    ACTIVE = 1
    INACTIVE = 2
    TEMPORARILY_DISABLED = 3
    PERMANENTLY_DISABLED = 4
    ACCOUNT_STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
        (TEMPORARILY_DISABLED, 'Temporarily Disabled'),
        (PERMANENTLY_DISABLED, 'Permanently Disabled'),
    )

    name = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    usertype = models.IntegerField(default=STUDENT, choices=ACCOUNT_TYPE_CHOICES)
    image = models.FileField(upload_to='profile_pic/')
    account_status = models.IntegerField(default=ACTIVE, choices=ACCOUNT_STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True,auto_now=False)
    is_login = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)
    last_login_ip = models.CharField(max_length=20, blank=True, default='0.0.0.0')
    last_session = models.ForeignKey(Session, null=True)