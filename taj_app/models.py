from django.db import models
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session

# Created by Ashish Kedia, ashish1294@gmail.com
# Created on 13th Jan, 2015
# Last Modefied on 13th Jan, 2015

# @Ashish - Make Sure to Add Triggers to Data Base to increment problem solved !!
# @Ashish - Fix the Unique Email Thing. May be Separate

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

    name = models.CharField(max_length = 200)
    uname = models.CharField(max_length = 50, unique = True)
    email = models.EmailField(max_length = 254, unique = True)
    user = models.OneToOneField(User)
    usertype = models.IntegerField(default = STUDENT, choices = ACCOUNT_TYPE_CHOICES)
    image = models.FileField(upload_to = 'profile_pic/')
    account_status = models.IntegerField(default = ACTIVE, choices = ACCOUNT_STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add = True, auto_now = False)
    is_login = models.BooleanField(default = False)
    last_login = models.DateTimeField(auto_now_add = False, auto_now = False, blank = True, null = True)
    last_login_ip = models.CharField(max_length = 20, blank = True, default = '0.0.0.0')
    last_session = models.ForeignKey(Session, null = True)

    def __str__(self) :
        return "Name = %s Type= %s" % (self.name, self.usertype)
    
class news(models.Model) :
    posted_at = models.DateTimeField(auto_now_add = True, auto_now = False)
    content = models.CharField(max_length = 500)
    author = models.ForeignKey(user)

class problem(models.Model) :
    id = models.CharField(max_length = 15, primary_key = True)
    name = models.CharField(max_length = 200, unique = True)
    statement = models.TextField()
    comment = models.TextField()
    author = models.ForeignKey(user)
    added_at = models.DateTimeField(auto_now_add = True, auto_now = False)
    c_time_limit = models.DecimalField(default = 1.0, max_digits = 5, decimal_places = 3)
    java_time_limit = models.DecimalField(default = 2.0, max_digits = 5, decimal_places = 3)

    def __str__(self) :
        return "Id = %s, Name = %s" % (self.id, self.name)

class submission(models.Model) :
    C_LANG = 0
    CPP_LANG = 1
    JAVA_LANG = 2
    LANGUAGE_CHOICES = (
        (C_LANG, 'C'),
        (CPP_LANG, 'C++'),
        (JAVA_LANG, 'Java'),
    )

    NOT_EVALUATED = 0
    CORRECT = 1
    WRONG_ANS = 2
    TIME_LIMIT_EXCEEDED = 3
    COMPILE_ERROR = 4
    RUN_TIME_ERROR = 5
    FATAL_EXCEPTION = 6

    RESULT_CHOICES = (
        (NOT_EVALUATED, 'Yet to be Judged'),
        (CORRECT, 'Accepted'),
        (WRONG_ANS, 'Wrong Ans'),
        (COMPILE_ERROR, 'Compile Error'),
        (RUN_TIME_ERROR, 'Run Time Error'),
        (FATAL_EXCEPTION, 'Fatal Error'),
    )

    submitted_at = models.DateTimeField(auto_now_add = True, auto_now = False)
    submitted_by = models.ForeignKey(user)
    problem = models.ForeignKey(problem)
    language = models.IntegerField(choices = LANGUAGE_CHOICES)
    result = models.IntegerField(choices = RESULT_CHOICES, default = NOT_EVALUATED)

    def __str__(self) :
        return "%s by %s res = %d" % (self.problem_id, self.submitted_by.name, self.result)

class incident(models.Model) :
    DASHBOARD_FORM = 'Hacking News Post Form'
    INCOMPLETE_SIGNUP_FORM = 'Sending Bad Request on SignUp'

    reported_at = models.DateTimeField(auto_now_add = True, auto_now = False)
    against = models.ForeignKey(user, null = True)
    content = models.TextField()
    ip = models.CharField(max_length = 20, null = True)

class bug(models.Model) :
    reported_by = models.ForeignKey(user)
    reported_at = models.DateTimeField(auto_now_add = True, auto_now = False)
    content = models.TextField()