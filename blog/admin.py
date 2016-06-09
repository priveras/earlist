from django.contrib import admin

from .models import Post, Evento, Job, Voter

class PostAdmin(admin.ModelAdmin):
    # exclude = ['created_at']
    prepopulated_fields = {'slug': ('title',)}

# class CategoryAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'slug': ('title',)}

class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

class JobAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('company','title')}

admin.site.register(Post, PostAdmin)
admin.site.register(Evento, EventAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(Voter)
# admin.site.register(Category, CategoryAdmin)