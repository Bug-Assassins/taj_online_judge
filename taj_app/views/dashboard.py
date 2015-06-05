from include_module import secure_render
from django.http import HttpResponseRedirect
from taj_app.models import incident, user, news
from django.utils import timezone

# File Written by Ashish Kedia, ashish1294@gmail.com
# Created on 14th Jan, 2015
# Last Modified on 14th Jan, 2015

'''Remember Red, hope is a good thing, maybe the best of things, and no
good thing ever dies. Fear can hold you prisoner, hope can set you free
- Andy Dufresne, The Shawshank Redemption'''

def check_incident(request) :
    if request.session['type'] == user.STUDENT :
        dash_inci = incident(against_id = request.session['id'], content = incident.DASHBOARD_FORM, ip = request.META['REMOTE_ADDR'])
        dash_inci.save()
        return False
    else :
        return True

def dashboard(request) :

    if 'userid' not in request.session :
        return HttpResponseRedirect("/err/1")

    json_obj = {'news' : []}

    if 'new' in request.POST and check_incident(request):
        posted_news = news(posted_at = timezone.now(), content = request.POST['new'], author_id = request.session['id'])
        posted_news.save()

    if 'del' in request.POST and check_incident(request):
        for n in request.POST['del'] :
            news.objects.get(id=n.id).delete()

    for n in news.objects.all() :
        json_obj['news'].append({'id' : n.id, 'posted_at' : n.posted_at, 'content' : n.content, 'author' : n.author.name})

    return secure_render(request, 'dashboard.html', json_obj)