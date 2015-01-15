from include_module import *

def view_user(request, uname) :

    if 'userid' not in request.session :
        return HttpResponseRedirect("/")

    user_data = user.objects.get(uname = uname)

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