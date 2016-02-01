from django.views import generic
from .models import Post, Event, Job

class PostListView(generic.ListView):
	template_name = 'blog/index.html'
	context_object_name = 'posts_list'

	def get_queryset(self):
		return Post.objects.order_by('-created_at')[:5]


class DetailView(generic.DetailView):
    model = Post
    template_name = 'blog/detail.html'

class ProfileView(generic.TemplateView):
    template_name = "blog/profile.html"

class EventListView(generic.ListView):
	template_name = 'blog/events.html'
	context_object_name = 'events_list'

	def get_queryset(self):
		return Event.objects.order_by('-event_date')[:5]

class JobListView(generic.ListView):
	template_name = 'blog/jobs.html'
	context_object_name = 'jobs_list'

	def get_queryset(self):
		return Job.objects.order_by('-created_at')[:5]