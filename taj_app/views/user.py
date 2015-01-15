def view_profile(request, uname) :

	if 'userid' not in request.session :
		return HttpResponseRedirect("/")

	u = User.objects.get(username = uname)
	user_data = user.objects.get(user = u)

	json_obj = {'uid' : uname, 'name' : user_data.name , 'email' : u.email }
	json_obj['problem_solved'] : []
	json_obj['solved'] : user_data.solved
	json_obj['submitted'] : user_data.submitted
	json_obj['wrong_ans'] : user_data.wrong_ans
	json_obj['error'] : user_data.error
	
	
