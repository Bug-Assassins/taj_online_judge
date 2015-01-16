from include_module import *

# File Created By Ashish Kedia, ashish1294@gmail.com
# Created on 16th Jan, 2015
# Modified on 16th Jan, 2015

'''Experience is what you get when you didn't get what you wanted.
And experience is often the most valuable thing you have to offer.
- Randy Pausch, The Last Lecture'''

def problem_view(request, probid) :

	if 'userid' not in request.session :
        return HttpResponseRedirect("/err/1")
