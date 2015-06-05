from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from include_module import secure_render
from django.http import HttpResponseRedirect
from taj_app.models import incident, user

# File Written By Ashish Kedia, ashish1294@gmail.com
# Created on - 8th January, 2015
# Last Major Modification - 12th January, 2015

'''The training is nothing. The will is everything. The will to act.
- Ras al Ghul, Batman Begins'''

# A utility function that ensures that all the fields are properly submitted via form
def check_request_signup(request) :
    if 'taj_signup_id' in request.POST and 'taj_signup_email' in request.POST and 'taj_signup_name' in request.POST \
    and 'taj_signup_password' in request.POST and 'taj_signup_password_con' in request.POST :
        return True
    else :
        signup_inci = incident(content = incident.SIGNUP_FORM, ip = request.META['REMOTE_ADDR'])
        signup_inci.save()
        return False

def signup(request) :
    json_obj = {'error' : '', 'user_id' : '', 'name' : '', 'email' : ''}

    if 'userid' in request.session :
        return HttpResponseRedirect("/dashboard")

    if 'taj_signup_but' in request.POST:
        form_stat = check_request_signup(request)
        error = ''
        user_id = ''

        if form_stat == True :
            user_id = str(request.POST['taj_signup_id']).strip()
            if user_id == '':
                error = "Please Enter User ID"

            email = str(request.POST['taj_signup_email']).strip()
            if email == '' and error == '':
                error = 'Please Enter Email ID'
            elif error == '' :
                try :
                    validate_email(email)
                except ValidationError:
                    error = 'Invalid Email Address Given'

            name = str(request.POST['taj_signup_name']).strip()
            if name == '' and error == '':
                error = 'Please Enter Your Name'

            password = str(request.POST['taj_signup_password']).strip()
            if password == '' and error == '' :
                error = 'Please Enter Password'

        
            password_con = str(request.POST['taj_signup_password_con']).strip()
            if password_con == '' and error == '' :
                error = 'Please Enter Confirmation Password'

            if password != password_con and error == '':
                error = 'Password Mismatch'

            if error == '' :
                try :
                    new_user = User.objects.create_user(username=user_id, password=password, email=email)
                    u = user(name=name, user=new_user, email=email, uname=user_id)
                    u.save()
                except IntegrityError:
                    error = 'A user with given details already exist !!'
                except Exception:
                    error = 'Cannot Create User at the moment !!'

            json_obj = {'error': error, 'user_id': user_id, 'email': email, 'name': name}

        else :
            error = incident.HACK_MSG
            json_obj['error'] = error

        if error == '' :
                return HttpResponseRedirect('/success/1')

    return secure_render(request, 'signup.html', json_obj)