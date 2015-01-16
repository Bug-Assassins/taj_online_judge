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
    
    sub_list = submission.objects.filter(submitted_by_id=request.session['id'])

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
            json_obj['error'] = "Cannot Process Your Query !!"
        elif 'taj_search_submit' in request.POST :
            if check_search(request):
                print "Here - " + '/users/view/' + str(request.POST['user_id'])
                return HttpResponseRedirect('/users/view/' + str(request.POST['user_id']))
            else :
                json_obj['error'] = incident.HACK_MSG                
    except Error as e :
        json_obj['error'] = 'Invalid Parameters were Passed !!'
    
    return secure_render(request, 'user_search.html', json_obj)


def edit_user(request, uname) :

    if 'userid' not in request.session :
        return HttpResponseRedirect("/err/1")

    try :
        uname = str(uname)

        if request.session['type'] == user.ADMIN or request.session['userid'] == uname :
            if ''
        else :
            return HttpResponseRedirect("/users/search/err/2")
    except Error as e :
        print "Some Exception Was Caught !! ~ Edit User"
        return HttpResponseRedirect("/users/search/err/3")

    return secure_render(request, 'user_edit.html', {'error' : ''})