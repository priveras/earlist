"""earlist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from blog import views
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^cuentas/perfil/(?P<slug>[^\.]+)/vote/(?P<direction>[^\.]+)/$', views.vote, name='vote'),
    url(r'^panel/status/(?P<slug>[^\.]+)/(?P<message>[0-9]+)/$', login_required(views.status), name='status'),
    url(r'^admin/', admin.site.urls),
    # url('^', include('django.contrib.auth.urls')),
	url(r'^', include('blog.urls')),
    url(r'^cuentas/perfil/(?P<view>[^\.]+)/$', login_required(views.profile), name='profile'),
    url(r'^producto/(?P<slug>[^\.]+)/$', views.DetailView.as_view(), name='detail'), 
    url(r'^cuentas/', include('allauth.urls')),
    url(r'^exito-producto/(?P<slug>[^\.]+)/$', login_required(views.SuccessPostView.as_view()), name='success-post'), 
    url(r'^contribuir/', views.ContributeView.as_view(), name='contribute'), 
    url(r'^actualizar-producto/(?P<slug>[^\.]+)/$', login_required(views.PostUpdateView.as_view()), name='update-post'), 
    url(r'^eliminar-producto/(?P<slug>[^\.]+)/$', login_required(views.PostDeleteView.as_view()), name='delete-post'),
    url(r'^(?P<slug>[^\.]+)/vote/(?P<direction>[^\.]+)$', views.vote, name='vote'),
    url(r'^newsletter', views.newsletter, name='newsletter'),

]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)