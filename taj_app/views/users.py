from include_module import *

# File Created by Ashish Kedia, ashish1294@gmail.com
# Created on 15th Jan, 2015
# Modified on 16th Jan, 2015

'''Tired of lying in the sunshine, Staying home to watch the rain
You are young and life is long, And there is time to kill today
And then one day you find, 10 years have got behind you
No one told you when to run, You missed the starting gun
- Time, Pink Floyd'''

def view_user(request, uname) :

    if 'userid' not in request.session :
        return HttpResponseRedirect("/err/1")

    uname = str(uname)

    user_list = user.objects.filter(uname = uname)

    if user_list.count() == 0 :
        return HttpResponseRedirect("/users/search/err/1")

    user_data = user_list[0]

    json_obj = {'uid' : uname, 'name' : user_data.name , 'email' : user_data.email }
    json_obj['problem_solved'] = []
    json_obj['solved'] = 0
    json_obj['submitted'] = 0
    json_obj['wrong_ans'] = 0
    json_obj['error'] = 0
    
    sub_list = submission.objects.filter(submitted_by_id = request.session['id'])

    for sub in sub_list :
        json_obj['submitted'] = json_obj['submitted'] + 1
        if sub.result == submission.CORRECT :
            json_obj['problem_solved'].append(sub.problem_id)
            json_obj['solved'] = json_obj['solved'] + 1
        elif sub.result == submission.WRONG_ANS :
            json_obj['wrong_ans'] = json_obj['wrong_ans'] + 1
        elif sub.result == submission.TIME_LIMIT_EXCEEDED or sub.result == COMPILE_ERROR:
            json_obj['error'] = json_obj['error'] + 1
        elif sub.result == submission.FATAL_EXCEPTION or sub.result == submission.RUN_TIME_ERROR :
            json_obj['error'] = json_obj['error'] + 1

    return render(request, 'user.html', json_obj)

# A utility function that verifies the Search Form Fields
def check_search(request) :
    if 'user_id' in request.POST :
        return True
    else :
        search_inci = incident(content = incident.INCOMPLETE_SEARCH_FORM, ip = request.META['REMOTE_ADDR'], against_id = request.session['id'])
        search_inci.save()
        return False

def search_user(request, err = 0) :

    if 'userid' not in request.session :
        return HttpResponseRedirect("/err/1")

    json_obj = {'error' : ''}

    try :
        err = int(err)

        if err == 1 :
            json_obj['error'] = "No Such User was found !!"
        elif err == 2 :
            json_obj['error'] = "You are not authorized for the action !!"
        elif err == 3 :
            json_obj['error'] = incident.HACK_MSG
        elif 'taj_search_submit' in request.POST :
            if check_search(request):
                uid = str(request.POST['user_id']).strip()
                if uid == '' :
                    json_obj['error'] = 'Please Enter A Used Name !!'
                else :
                    return HttpResponseRedirect('/users/view/' + str(request.POST['user_id']))
            else :
                json_obj['error'] = incident.HACK_MSG                
    except Exception as e :
        json_obj['error'] = 'Invalid Parameters were Passed !!'
    
    return secure_render(request, 'user_search.html', json_obj)

def check_edit(request) :

    if 'taj_user_name' in request.POST and 'taj_user_password' in request.POST and \
    'taj_user_password_con' in request.POST :
        if request.session['type'] == user.ADMIN :
            try :
                acc_type = int(request.POST['account_type'])
                if acc_type == user.STUDENT or acc_type == user.TEACHER :
                    return True
                else :
                    return False
            except Exception as e :
                return False
        elif 'account_type' in request.POST :
            return False
        else :
            return True
    else :
        return False

def edit_user(request, uname) :

    if 'userid' not in request.session :
        return HttpResponseRedirect("/err/1")

    json_obj = {}

    try :
        uname = str(uname)
        print "Uname ", uname
        user_data = user.objects.get(uname = uname)

        if request.session['type'] == user.ADMIN or request.session['userid'] == uname :
            print "Auth Granted"
            if 'taj_eu_submit' in request.POST :
                print "Form Submitted"
                if check_edit(request) :
                    print "Form Checked"
                    try :
                        u_n = str(request.POST['taj_user_name']).strip()
                        u_p = str(request.POST['taj_user_password']).strip()
                        u_c = str(request.POST['taj_user_password_con']).strip()
                        print "Data Extracted"

                        if u_n == '' :
                            json_obj['error'] = "Please Enter Name"
                        elif u_p == '' :
                            json_obj['error'] = "Please Enter Password"
                        elif u_c == '' :
                            json_obj['error'] = "Please Enter Confirm Password"
                        elif u_p != u_c :
                            json_obj['error'] = "Password Mismatch"
                        else :
                            print "Final Else Reached"
                            user_data.name = u_n
                            if request.session['type'] == user.ADMIN :
                                user_data.usertype = int(request.POST['account_type'])
                            u = user_data.user
                            u.set_password(request.POST)
                            u.save()
                            user_data.save()

                            return HttpResponseRedirect('/users/view/' + str(user_data.uname))
                            
                    except (SyntaxError, NameError) as se :
                        json_obj['error'] = "Invalid Data Submitted !!"
                    except Exception as e :
                        json_obj['error'] = 'Could Not Process Your Request !!'
                else :
                    inci = incident(content = incident.USER_EDIT_FORM, ip = request.META['REMOTE_ADDR'], against_id = request.session['id'])
                    inci.save()
                    return HttpResponseRedirect("/users/search/err/3")
            
            json_obj['name'] = user_data.name
            json_obj['uid'] = user_data.uname
            json_obj['account_type'] = user_data.usertype

        else :
            return HttpResponseRedirect("/users/search/err/2")

    except Exception as e :
        return HttpResponseRedirect("/users/search/err/1")

    return secure_render(request, 'user_edit.html', json_obj)