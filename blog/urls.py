from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'blog'
urlpatterns = [
	# url(r'^$entry/', views.PostListView.as_view(), name='entry'),
	url(r'^$', views.index, name='index'),
    url(r'^eventos/$', views.EventListView.as_view(), name='events'),
    url(r'^trabajos/$', views.JobListView.as_view(), name='jobs'),   
    url(r'^publicar-producto/$', login_required(views.post), name='post'),
    url(r'^submit-event/$', login_required(views.event), name='event'),
    url(r'^submit-job/$', login_required(views.job), name='job'),
    url(r'^panel/', views.PanelListView.as_view(), name='panel'), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)