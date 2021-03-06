from django.conf.urls import patterns, include, url
from django.contrib import admin
from taj_app.views import *

# File Created by Ashish Kedia, ashish1294@gmail.com
# File Created on 7th Jan, 2015
# Last Modified on 14th Jan, 2015

'''There is no secret ingredient ! - Kung Fu Panda'''


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TAJ.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', login),
    url(r'^index/?$', login),
    url(r'^error/(\d{1})/?$', error),
    url(r'^success/(\d{1})/?$', success),
    url(r'^success/(?P<succ>\d{1})/?$', login),
    url(r'^err/(?P<err>\d{1})/?$', login),
    url(r'^signup/?$', signup),
    url(r'^dashboard/?$', dashboard),
    url(r'^logout/?$', logout),
    url(r'^users/edit/(.+)/?$', edit_user),
    url(r'^users/view/(.+)/?$', view_user),
    url(r'^users/search/err/(?P<err>\d{1})/?$', search_user),
    url(r'^users/search/?$', search_user),
    url(r'^problems/add/new?$', problem_add),
    url(r'^problems/?$', problem_list),
    url(r'^problems/view/(.+)/?$', problem_view),
)