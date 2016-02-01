from django.conf.urls import include, url

from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.PostListView.as_view(), name='index'),   
    url(r'^events/$', views.EventListView.as_view(), name='events'),
    url(r'^jobs/$', views.JobListView.as_view(), name='jobs'),   
    url(r'^submit-post/$', views.post, name='post'),
]