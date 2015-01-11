from django.shortcuts import render

# Create your views here.
''' You might never fail on the scale I did, but some failure in life is inevitable. It is
impossible to live without failing at something, unless you live so cautiously that you
might as well not have lived at all - in which case, you fail by default. - J. K. Rowling '''

def login(request) :
	return render (request, 'index.html', {})

def signup(request) :
	return render (request, 'signup.html', {})