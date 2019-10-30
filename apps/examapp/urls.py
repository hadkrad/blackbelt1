from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^thoughts$', views.dashboard),
    url(r'^login$', views.login),
    url(r'^wishes/new$', views.new),
    url(r'^createwish$', views.createwish),
    url(r'^remove/(?P<wishid>\d+)$', views.removewish),
    url(r'^grant_wish/(?P<wishid>\d+)$', views.grant_wish),
    url(r'^wishes/edit/(?P<wishid>\d+)$', views.edit_wish),
    url(r'^completeedit$', views.completeedit),
    url(r'^logout$', views.logout),
    url(r'^wishes/stats$', views.stats),
    url(r'^like/(?P<thoughtid>\d+)$', views.like), 
    url(r'^unlike/(?P<thoughtid>\d+)$', views.unlike), 
    url(r'^newthought$', views.newthought),
    url(r'^thoughts/(?P<thoughtid>\d+)$', views.details),
    url(r'^delete/(?P<thoughtid>\d+)$', views.delete),

    
]