from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required


from . import views

from django.contrib.sitemaps.views import sitemap
from sitemap import BlogSitemap, ViewSitemap

# a dictionary of sitemaps
sitemaps = {
	'views': ViewSitemap,
    'blog': BlogSitemap
}

app_name = 'blog'
urlpatterns = [
	# url(r'^$entry/', views.PostListView.as_view(), name='entry'),
	url(r'^$', views.index, name='index'),
    url(r'^events/$', views.events, name='events'),
    url(r'^jobs/$', views.JobListView.as_view(), name='jobs'),   
    url(r'^share/$', views.post, name='post'),
    url(r'^publish-event/$', login_required(views.event), name='event'),
    # url(r'^publicar-evento/$', login_required(views.event), name='event'),
    url(r'^submit-job/$', login_required(views.job), name='job'),
    url(r'^panel/', login_required(views.PanelListView.as_view()), name='panel'), 
    # url(r'^dashboard/', views.dashboard, name='dashboard'), 
    url(r'^about/', views.AboutView.as_view(), name='about'), 
    url(r'^faq/', views.FaqView.as_view(), name='faq'), 
    url(r'^terms/', views.TermsView.as_view(), name='terms'), 
    url(r'^privacy/', views.PrivacyView.as_view(), name='privacy'), 
    url(r'^bye/', views.UnsubscribedView.as_view(), name='unsubscribed'), 
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    url(r'^newsletter/', views.NewsletterView.as_view(), name='newsletter'), 
    url(r"^checkout$", views.checkout, name="checkout_page")
]