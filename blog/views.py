from django.views import generic
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Post, Event, Job
from .forms import PostForm

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

def post(request):
    if request.method == 'GET':
        form = PostForm()
    else:
        # A POST request: Handle Form Upload
        form = PostForm(request.POST) # Bind data from request.POST into a PostForm
 
        # If data is valid, proceeds to create a new post and redirect the user
        if form.is_valid():
            title = form.cleaned_data['title']
            slug = form.cleaned_data['slug']
            link = form.cleaned_data['link']
            created_at = form.cleaned_data['created_at']
            post = Post.objects.create(
            	title=title,
            	slug = slug,
            	link=link,
            	created_at=created_at
            	)
            return HttpResponseRedirect('/accounts/profile')
 
    return render(request, 'blog/submit_post.html', {
        'form': form,
    })