from include_module import *

# File Written by Ashish Kedia, ashish1294@gmail.com
# Created on 14th Jan, 2015
# Last Modified on 14th Jan, 2015

'''Remember Red, hope is a good thing, maybe the best of things, and no
good thing ever dies. Fear can hold you prisoner, hope can set you free
- Andy Dufresne, The Shawshank Redemption'''

def dashboard(request) :

    if 'userid' not in request.session :
        return HttpResponseRedirect("/")

    json_obj = {'news' : []}

    if 'new' in request.POST :
        posted_news = news(posted_at=timezone.now(), content=request.POST['new'], author_id=request.session['id'])
        posted_news.save()

    if 'del' in request.POST :
        for n in request.POST['del'] :
            news.objects.get(id=n.id).delete()

    for n in news.objects.all() :
        json_obj['news'].append({'id' : n.id, 'posted_at' : n.posted_at, 'content' : n.content, 'author' : n.author.name})

    return secure_render(request, 'dashboard.html', json_obj)