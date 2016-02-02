from django.views import generic
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from .models import Post, Event, Job
from .forms import PostForm, JobForm,EventForm
from django.utils.text import slugify
from django.contrib.auth import logout
from django.contrib.auth.models import User

class PostListView(generic.ListView):
	template_name = 'blog/index.html'
	context_object_name = 'posts_list'

	def get_queryset(self):
		return Post.objects.order_by('-created_at')[:5]


class DetailView(generic.DetailView):
    model = Post
    template_name = 'blog/detail.html'

class ProfileListView(generic.ListView):
    model = Post
    template_name = 'blog/profile.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super(ProfileListView, self).get_context_data(**kwargs)
        context['posts_list'] = Post.objects.filter(user=self.request.user).order_by('-created_at')[:5]
        context['events_list'] = Event.objects.order_by('-created_at')[:5]
        context['my_events_list'] = Event.objects.filter(user=self.request.user).order_by('-created_at')[:5]
        context['jobs_list'] = Job.objects.order_by('-created_at')[:5]
        context['my_jobs_list'] = Job.objects.filter(user=self.request.user).order_by('-created_at')[:5]
        context['first_name'] = self.request.user.first_name
        context['last_name'] = self.request.user.last_name
        return context

class EventListView(generic.ListView):
	template_name = 'blog/events.html'
	context_object_name = 'events_list'

	def get_queryset(self):
		return Event.objects.order_by('event_date')[:5]

class JobListView(generic.ListView):
	template_name = 'blog/jobs.html'
	context_object_name = 'jobs_list'

	def get_queryset(self):
		return Job.objects.order_by('-created_at')[:5]

def logout_view(request):
    logout(request)

def post(request):
    if request.method == 'GET':
        form = PostForm()
    else:
        # A POST request: Handle Form Upload
        form = PostForm(request.POST) # Bind data from request.POST into a PostForm
 
        # If data is valid, proceeds to create a new post and redirect the user
        if form.is_valid():
            current_user = request.user
            title = form.cleaned_data['title']
            slogan = form.cleaned_data['slogan']
            body = form.cleaned_data['body']
            link = form.cleaned_data['link']
            image_url = form.cleaned_data['image_url']
            post = Post.objects.create(
                user = current_user,
            	title = title,
            	slug = slugify(title),
                slogan = slogan,
                body = body,
            	link = link,
                image_url = image_url,
            	created_at = timezone.now()
            	)
            return HttpResponseRedirect('/accounts/profile')
 
    return render(request, 'blog/submit_post.html', {
        'form': form,
    })

def job(request):
    if request.method == 'GET':
        form = JobForm()
    else:
        # A POST request: Handle Form Upload
        form = JobForm(request.POST) # Bind data from request.POST into a PostForm
 
        # If data is valid, proceeds to create a new post and redirect the user
        if form.is_valid():
            current_user = request.user
            title = form.cleaned_data['title']
            company = form.cleaned_data['company']
            link = form.cleaned_data['link']
            image_url = form.cleaned_data['image_url']
            job = Job.objects.create(
                user = current_user,
                title = title,
                slug = slugify(title),
                company = company,
                link = link,
                image_url = image_url,
                created_at = timezone.now()
                )
            return HttpResponseRedirect('/accounts/profile')
 
    return render(request, 'blog/submit_job.html', {
        'form': form,
    })

def event(request):
    if request.method == 'GET':
        form = EventForm()
    else:
        # A POST request: Handle Form Upload
        form = EventForm(request.POST) # Bind data from request.POST into a PostForm
 
        # If data is valid, proceeds to create a new post and redirect the user
        if form.is_valid():
            current_user = request.user
            title = form.cleaned_data['title']
            body = form.cleaned_data['body']
            link = form.cleaned_data['link']
            image_url = form.cleaned_data['image_url']
            cover_url = form.cleaned_data['cover_url']
            event_date = form.cleaned_data['event_date']
            event = Event.objects.create(
                user = current_user,
                title = title,
                slug = slugify(title),
                body = body,
                link = link,
                image_url = image_url,
                cover_url = cover_url,
                event_date = event_date,
                created_at = timezone.now()
                )
            return HttpResponseRedirect('/accounts/profile')
 
    return render(request, 'blog/submit_event.html', {
        'form': form,
    })


