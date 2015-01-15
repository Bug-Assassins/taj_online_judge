from include_module import *
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# File Written By Ashish Kedia, ashish1294@gmail.com
# Created on - 8th January, 2015
# Last Major Modification - 12th January, 2015

'''It's only after we've lost everything that we're free to do anything
- Tyler Durden, Fight Club'''

def login(request, succ = 0, err = 0) :

    if 'userid' in request.session :
        return HttpResponseRedirect("/dashboard")

    json_obj = {'error' : ''}

    try :
        succ = int(succ)
        err = int(err)
        if succ == 1 :
            json_obj['error'] = 'User Successfully Registered'
        elif succ == 2:
            json_obj['error'] = 'Successfully Logged Out !!'
        elif err == 1 :
            json_obj['error'] = 'Please Login to Continue !!'
    except Error as e :
        print "Some Error Has been Caught !! ~ login.py"

    #Checking if User submitted Login Form
    if 'loginid' in request.POST and 'password' in request.POST:
        loginid = request.POST['loginid'].strip()
        password = request.POST['password']

        #Authenticating User
        u = authenticate(username = loginid, password = password)

        if u is not None :

            #Checking User's Account State
            user_data = user.objects.get(user=u)
            if user_data.account_status == user.PERMANENTLY_DISABLED :
                json_obj['error'] = 'Your Account has been Permanently Disabled !!'
            elif user_data.account_status == user.TEMPORARILY_DISABLED :
                json_obj['error'] = 'Your Account has been Temporarily Disabled !!'
            elif user_data.account_status == user.INACTIVE :
                json_obj['error'] = 'Your Account is Inactive !!'
            elif user_data.account_status == user.ACTIVE :
                #Checking User's Login Status to prevent concurrent login Sessions
                if user_data.is_login == True :
                    temp_sess = user_data.last_session
                    user_data.last_session = None
                    temp_sess.delete()
                    user_data.is_login = False
                    user_data.save()
                    json_obj['error'] = 'Already Logged @ ' + str(user_data.last_login_ip) + ". All Sessions Destroyed !!"
                else :

                    #Creating a New Session
                    request.session['userid'] = u.username
                    request.session['type'] = user_data.usertype
                    request.session['name'] = user_data.name
                    request.session['id'] = user_data.pk
                    print "Just Checking -", request.session['userid'], " ", Session.objects.all().count()
                    print "key ", request.session.session_key

                    #Updating Table with Login Records
                    user_data.is_login = True
                    user_data.last_login_ip = str(request.META['REMOTE_ADDR'])
                    user_data.last_login = timezone.now()
                    user_data.last_session = Session.objects.get(pk=request.session.session_key)
                    user_data.save()

                    return HttpResponseRedirect("/dashboard")
        else :
            json_obj['error'] = 'Invalid UserID or Password !!'

    return secure_render(request, 'index.html', json_obj)

def logout(request) :

    if 'userid' not in request.session :
        return HttpResponseRedirect("/err/1")

    json_obj = {'error' : ''}
    user_data = user.objects.get(id=request.session['id'])
    user_data.is_login = False
    user_data.last_session = None
    user_data.save()
    Session.objects.get(pk=request.session.session_key).delete()
    return HttpResponseRedirect("/success/2")