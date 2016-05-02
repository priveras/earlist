from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'blog'
urlpatterns = [
	# url(r'^$entry/', views.PostListView.as_view(), name='entry'),
	url(r'^$', views.index, name='index'),
    url(r'^events/$', views.EventListView.as_view(), name='events'),
    url(r'^jobs/$', views.JobListView.as_view(), name='jobs'),   
    url(r'^submit-post/$', login_required(views.post), name='post'),
    url(r'^submit-event/$', login_required(views.event), name='event'),
    url(r'^submit-job/$', login_required(views.job), name='job'),
    url(r'^panel/', views.PanelListView.as_view(), name='panel'), 
]