from django.contrib.auth.models import User
from django.db import IntegrityError
from include_module import *

# File Written By Ashish Kedia, ashish1294@gmail.com
# Created on - 8th January, 2015
# Last Major Modification - 12th January, 2015

'''The training is nothing. The will is everything. The will to act.
- Ras al Ghul, Batman Begins'''

def signup(request) :
    json_obj = {'error' : '', 'user_id' : '', 'name' : '', 'email' : ''}

    if 'userid' in request.session :
        return HttpResponseRedirect("/dashboard")

    if 'taj_signup_id' in request.POST:
        error = ''
        user_id = ''
        if request.POST['taj_signup_id'] :
            user_id = str(request.POST['taj_signup_id']).strip()
        if user_id == '':
            error = "Please Enter User ID"

        email = ''
        if request.POST['taj_signup_email'] :
            email = str(request.POST['taj_signup_email']).strip()
        if email == '' and error == '':
            error = 'Please Enter Email ID'

        name = ''
        if request.POST['taj_signup_name'] :
            name = str(request.POST['taj_signup_name']).strip()
        if name == '' and error == '':
            error = 'Please Enter Your Name'

        password = ''
        if request.POST['taj_signup_password'] :
            password = str(request.POST['taj_signup_password']).strip()
        if password == '' and error == '' :
            error = 'Please Enter Password'

        password_con = ''
        if request.POST['taj_signup_password_con'] :
            password_con = str(request.POST['taj_signup_password_con']).strip()
        if password_con == '' and error == '' :
            error = 'Please Enter Confirmation Password'

        if password != password_con and error == '':
            error = 'Password Mismatch'

        if error == '' :
            try :
                new_user = User.objects.create_user(user_id, email, password)
                u = user(name=name, user=new_user)
                u.save()
            except IntegrityError as e:
                error = 'A user with given details already exist !!'
            except Error as e:
                error = 'Cannot Create User at the moment !!'

        json_obj = {'error': error, 'user_id': user_id, 'email': email, 'name': name}

        if error == '' :
            return secure_render(request, 'index.html', {'error': 'User Successfully Registered'})

    return secure_render(request, 'signup.html', json_obj)