from django.contrib import admin

from .models import Post, Event, Job, Voter, Sponsor, Newsletter, Unsubscribed

class PostAdmin(admin.ModelAdmin):
    # exclude = ['created_at']
    prepopulated_fields = {'slug': ('title',)}

# class CategoryAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'slug': ('title',)}

# class EventAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'slug': ('title',)}

class JobAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('company','title')}

admin.site.register(Post, PostAdmin)
admin.site.register(Event)
admin.site.register(Job, JobAdmin)
admin.site.register(Voter)
admin.site.register(Sponsor)
admin.site.register(Newsletter)
admin.site.register(Unsubscribed)
# admin.site.register(Category, CategoryAdmin)