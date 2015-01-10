from django.conf.urls import patterns, include, url
from django.contrib import admin
from taj_app.views import * 

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TAJ.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', login),
)
