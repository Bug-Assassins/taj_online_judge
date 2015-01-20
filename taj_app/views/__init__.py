from include_module import *
from login import *
from signup import *
from dashboard import *
from users import *
from problem import *

# File Written By Ashish Kedia, ashish1294@gmail.com
# Created on - 8th January, 2015
# Last Major Modification - 12th January, 2015

'''Don't let someone tell you you can't do something. Not even me. You got a
dream, you gotta protect it. When people can't do something themselves, they
are gonna tell you that you can't do it. You want something go get it. - Will
Smith, The Pursuit of Happyness'''

def error(request, error = 0) :

	if 'userid' not in request.session :
		return HttpResponseRedirect("/err/1")

	json_obj = {}

	try :
		error = int(error)

		if error == 1:
			json_obj['error'] = "You Do Not have Authorization for the action requested !!"
		elif error == 2 :
			json_obj['error'] = 'The Problem was Successfully Added !!'
		elif error == 3 :
			json_obj['error'] = 'Some Unknown Error while processing your request !!'
		else :
			raise Exception("check")
	except Exception as e :
		print "Unknown Error ~ From __init__.py "
		json_obj['error'] = "Some Unknown Error"

	return secure_render(request, 'error.html', json_obj)

def success(request, succ = 0) :

	if 'userid' not in request.session :
		return HttpResponseRedirect("/err/1")

	json_obj = {}

	try :
		succ = int(succ)

		if succ == 1:
			json_obj['success'] = "Your Problem was Successfully Added !!"
		else :
			raise Exception("check")
	except :
		print "Unknown Error ~ From __init__.py "
		json_obj['sucess'] = "Operation Successful !!"

	return secure_render(request, 'success.html', json_obj)