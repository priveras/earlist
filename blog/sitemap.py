from django.contrib.sitemaps import Sitemap
from .models import Post
from django.core.urlresolvers import reverse

class BlogSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5
    
    def items(self):
        return Post.objects.filter(approved=1)
    
    def lastmod(self, obj):
        return obj.created_at

class ViewSitemap(Sitemap):

    def items(self):
        # Return list of url names for views to include in sitemap
        return ['blog:index', 'blog:events', 'blog:jobs', 'blog:post', 'blog:about']

    def location(self, item):
        return reverse(item)

 