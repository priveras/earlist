from django.contrib.sitemaps import Sitemap
from .models import Post
from django.core.urlresolvers import reverse

class BlogSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5
    
    def items(self):
        return Post.objects.filter(approved=True)
    
    def lastmod(self, obj):
        return obj.created_at

class ViewSitemap(Sitemap):

    def items(self):
        # Return list of url names for views to include in sitemap
        return ['blog:index', 'blog:post', 'blog:about']

    def location(self, item):
        return reverse(item)

 