from django.shortcuts import render
from django.core.context_processors import csrf
from taj_app.models import *
from django.http import HttpResponseRedirect, HttpResponse
import datetime

# File Written By Ashish Kedia, ashish1294@gmail.com
# Created on - 8th January, 2015
# Last Major Modification - 12th January, 2015

'''You might never fail on the scale I did, but some failure in life is inevitable. It is
impossible to live without failing at something, unless you live so cautiously that you
might as well not have lived at all - in which case, you fail by default. - J. K. Rowling'''

def secure_render(request, page, c) :
    c.update(csrf(request))
    return render (request, page, c)