from include_module import *
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# File Written By Ashish Kedia, ashish1294@gmail.com
# Created on - 8th January, 2015
# Last Major Modification - 12th January, 2015

'''It's only after we've lost everything that we're free to do anything
- Tyler Durden, Fight Club'''

def login(request) :
    json_obj = {'error' : ''}
    if 'userid' in request.session :
        return HttpResponseRedirect("/dashboard")

    #Checking if User submitted Login Form
    if 'loginid' in request.POST :
        loginid = request.POST['loginid']
        password = request.POST['password']

        #Authenticating User
        u = authenticate(username = loginid, password = password)

        print u

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
                print "Account Active"
                #Checking User's Login Status to prevent concurrent login Sessions
                if user_data.is_login == True :
                    user_data.is_login = False
                    user_data.save()
                    json_obj['error'] = 'Another Login @ ' + str(user_data.last_login_ip)
                else :
                    print "Final Else"
                    #Updating Table with Login Records
                    user_data.is_login = True
                    user_data.last_login_ip = str(request.META['REMOTE_ADDR'])
                    user_data.last_login = datetime.datetime.now()
                    user_data.save()

                    #Deleting Existing sessions if any and creating new one
                    request.session['userid'] = u.username
                    request.session['type'] = user_data.usertype
                    request.session['name'] = user_data.name

                    return HttpResponseRedirect("/dashboard")
        else :
            json_obj['error'] = 'Invalid UserID or Password !!'
    return secure_render(request, 'index.html', json_obj)