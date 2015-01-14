from include_module import *

# File Written by Ashish Kedia, ashish1294@gmail.com
# Created on 14th Jan, 2015
# Last Modified on 14th Jan, 2015

'''Remember Red, hope is a good thing, maybe the best of things, and no
good thing ever dies. Fear can hold you prisoner, hope can set you free
- Andy Dufresne, The Shawshank Redemption'''

def dashboard(request) :
	json_obj = {'news' : []}
	return secure_render(request, 'dashboard.html', json_obj)