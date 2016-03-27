from django.views import generic
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from .models import Post, Event, Job
from .forms import PostForm, JobForm,EventForm
from django.utils.text import slugify
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from earlist.secret import api
import twitter


def status(request, slug, message):

    p = Post.objects.get(slug=slug)
    email = p.user.email
    d = Context({ 'first_name': p.user.first_name })

    if message == '1':
        p.approved = 1
        plaintext = get_template('blog/emails/approved.txt')
        htmly     = get_template('blog/emails/approved.html')
        subject = 'Tu publicacion ha sido aprobada'

        api.PostMedia("%s: %s http://earlist.club/post/%s via @%s" % (p.title, p.slogan, p.slug, p.user), p.image_url)

    else:
        p.approved = 2
        plaintext = get_template('blog/emails/approved.txt')
        htmly     = get_template('blog/emails/approved.html')
        subject = 'Tu publicacion ha sido declinada'

    from_email, to = 'Earlist <hey@earlist.club>', email
    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    mail = EmailMultiAlternatives(subject, text_content, from_email, [to])
    mail.attach_alternative(html_content, "text/html")
    mail.send()

    p.save()

    return HttpResponseRedirect(reverse('panel'))


class PostListView(generic.ListView):
	template_name = 'blog/index.html'
	context_object_name = 'posts_list'

	def get_queryset(self):
		return Post.objects.order_by('-created_at')


class DetailView(generic.DetailView):
    model = Post
    template_name = 'blog/detail.html'


class PanelListView(generic.ListView):
    template_name = 'blog/panel.html'
    context_object_name = 'posts_list'

    def get_queryset(self):
        return Post.objects.order_by('-created_at')


class ProfileListView(generic.ListView):
    model = Post
    template_name = 'blog/profile.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):

        context = super(ProfileListView, self).get_context_data(**kwargs)
        context['posts_list'] = Post.objects.filter(user=self.request.user).order_by('-created_at')[:5]
        
        context['events_list'] = Event.objects.order_by('-created_at')[:5]
        context['my_events_list'] = Event.objects.filter(user=self.request.user).order_by('-created_at')[:5]

        context['jobs_list'] = Job.objects.order_by('-created_at')[:5]
        context['my_jobs_list'] = Job.objects.filter(user=self.request.user).order_by('-created_at')[:5]
        
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


class SuccessPostView(generic.DetailView):
    model = Post
    template_name = 'blog/success-post.html'

class ContributeView(generic.TemplateView):
    template_name = 'blog/contribute.html'
    

def post(request):
    if request.method == 'GET':
        form = PostForm()
    else:
        form = PostForm(request.POST)
 
        if form.is_valid():
            post = Post.objects.create(
                user = request.user,
            	title = form.cleaned_data['title'],
            	slug = slugify(form.cleaned_data['title']),
                slogan = form.cleaned_data['slogan'],
                body = form.cleaned_data['body'],
            	link = form.cleaned_data['link'],
                image_url = form.cleaned_data['image_url'],
                city = form.cleaned_data['city'],
                approved = 0,
            	created_at = timezone.now()
            	)

            url = reverse('success-post', kwargs={'slug':post.slug})

            return HttpResponseRedirect(url)
 
    return render(request, 'blog/submit_post.html', {
        'form': form,
    })

class PostUpdateView(generic.UpdateView):
    model = Post
    fields = ['slogan', 'body', 'link', 'image_url', 'city']
    template_name = 'blog/update_post.html'
    success_url = '/accounts/profile/'

    def user_passes_test(self, request):
        if request.user.is_authenticated():
            self.object = self.get_object()
            return self.object.user == request.user
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return HttpResponseRedirect('/')
        return super(PostUpdateView, self).dispatch(
            request, *args, **kwargs)

class PostDeleteView(generic.DeleteView):
    model = Post
    success_url = '/accounts/profile/'

    def user_passes_test(self, request):
        if request.user.is_authenticated():
            self.object = self.get_object()
            return self.object.user == request.user
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return HttpResponseRedirect('/')
        return super(PostDeleteView, self).dispatch(
            request, *args, **kwargs)

def job(request):
    if request.method == 'GET':
        form = JobForm()
    else:
        form = JobForm(request.POST)

        if form.is_valid():
            job = Job.objects.create(
                user = request.user,
                title = form.cleaned_data['title'],
                slug = slugify(form.cleaned_data['title']),
                company = form.cleaned_data['company'],
                link = form.cleaned_data['link'],
                image_url = form.cleaned_data['image_url'],
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
        form = EventForm(request.POST)
 
        if form.is_valid():
            event = Event.objects.create(
                user = request.user,
                title = form.cleaned_data['title'],
                slug = slugify(form.cleaned_data['title']),
                body = form.cleaned_data['body'],
                link = orm.cleaned_data['link'],
                image_url = form.cleaned_data['image_url'],
                cover_url = form.cleaned_data['cover_url'],
                event_date = form.cleaned_data['event_date'],
                created_at = timezone.now()
                )
            return HttpResponseRedirect('/accounts/profile')
 
    return render(request, 'blog/submit_event.html', {
        'form': form,
    })

