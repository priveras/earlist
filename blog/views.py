# -*- coding: utf-8 -*-
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from .models import Post, Event, Job, Voter
from .forms import PostForm, JobForm,EventForm
from django.utils.text import slugify
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context, RequestContext
from earlist.secret import api
import datetime
from datetime import datetime, timedelta
import twitter
from meta.views import Meta
from meta.views import MetadataMixin

meta = Meta(
        use_og = True,
        use_twitter = True,
        use_facebook = True,
        use_title_tag = True,
        url = "http://earlist.club/",
        title = 'Earlist',
        description = 'Earlist es el lugar para descubrir los mejores startups de tecnología en México. Únete a nuestra comunidad de apasionados por la innovación y la tecnología.',
        image = 'http://postimg.org/image/68e46t3m9/',
        )

class AboutView(generic.TemplateView):
    template_name = "blog/about.html"

def newsletter(request):
    how_many_days = 7
    p = Post.objects.order_by('-votes').filter(date__gte=datetime.now()-timedelta(days=how_many_days))[:5]

    email = 'priveras@gmail.com'
    d = Context({ 'posts_list': p })
    plaintext = get_template('blog/emails/newsletter.txt')
    htmly     = get_template('blog/emails/newsletter.html')
    subject = 'Lo mejor de la semana en Earlist'
    from_email, to = 'Earlist <hey@earlist.club>', email
    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    mail = EmailMultiAlternatives(subject, text_content, from_email, [to])
    mail.attach_alternative(html_content, "text/html")

    if mail.send():
        return HttpResponse('Newsletter sent')
    

def profile(
        request,
        view,
        template='blog/entry_profile.html',
        page_template='blog/entry_profile_page.html'):

    context = {}

    voted = Voter.objects.filter(user=request.user).count()
    posted = Post.objects.filter(user=request.user).count()

    if view == "votes":
        context_list = Voter.objects.filter(user=request.user).order_by('-created_at').all()
        view = 'votes'
    else:
        context_list = Post.objects.filter(user=request.user).order_by('-created_at').all()
        view = 'posts'

    context = {
        'context_list': context_list,
        'page_template': page_template,
        'view' : view,
        'voted' : voted,
        'posted' : posted,
        'meta': meta
    }

    if request.user.is_authenticated():
        votes = Voter.objects.filter(user=request.user)
        v_list = []
        for vote in votes:
            v_list.append(vote.post.slug)
            context['votes_list'] = v_list

    if request.is_ajax():
        template = page_template
    return render_to_response(
        template, context, context_instance=RequestContext(request))

def index(
        request,
        template='blog/index.html',
        page_template='blog/index_page.html'):

    orders = [ '-created_at', 'name' ]

    context = {
        'posts_list': Post.objects.order_by('-date', '-votes').filter(approved=1),
        'page_template': page_template,
        'meta': meta
    }

    if request.user.is_authenticated():
        votes = Voter.objects.filter(user=request.user)
        v_list = []
        for vote in votes:
            v_list.append(vote.post.slug)
            context['votes_list'] = v_list

    if request.is_ajax():
        template = page_template
    return render_to_response(
        template, context, context_instance=RequestContext(request))

@csrf_exempt
def vote(request, slug, direction):

    p = Post.objects.get(slug=slug)

    num_results = Voter.objects.filter(user = request.user, post = p).count()

    if num_results < 1:

        p.votes += 1

        voter = Voter.objects.create(
            user = request.user,
            post = p
            )

    else:
        Voter.objects.filter(user=request.user, post = p).delete()
        p.votes -= 1

    p.save()

    return HttpResponse(p.votes)

@csrf_exempt
def status(request, slug, message):

    p = Post.objects.get(slug=slug)
    email = p.user.email

    if message == '1':
        p.approved = 1
        p.updated_at = datetime.now()
        p.date = datetime.now()
        d = Context({ 'first_name': p.user.first_name, 'title': p.title, 'slug': p.slug })
        plaintext = get_template('blog/emails/approved.txt')
        htmly     = get_template('blog/emails/approved.html')
        subject = 'Tu publicacion ha sido aprobada'

        api.PostMedia("%s: %s http://earlist.club/producto/%s via @%s" % (p.title, p.slogan, p.slug, p.user), request.build_absolute_uri(p.image_file.url))

    else:
        p.approved = 2

        if message == '2':
            error = 'Hay errores en la publicación. Te invitamos a revisar que la imagen se vea bien, que no haya errores en el texto y que se usen el número de caracteres adecuados en la descripción. Puedes editar la publicación en tu perfil.'

        elif message == '3':
            error = 'Patrocinar'

        else:
            error = 'Este tipo de publicación no está en linea con el tipo de contenido que mostramos en Earlist. Lamentablemente no podremos publicar esto.'

        d = Context({ 'first_name': p.user.first_name, 'error': error, 'title': p.title })
        plaintext = get_template('blog/emails/declined.txt')
        htmly     = get_template('blog/emails/declined.html')
        subject = 'Tu publicacion ha sido declinada'        

    from_email, to = 'Earlist <hey@earlist.club>', email
    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    mail = EmailMultiAlternatives(subject, text_content, from_email, [to])
    mail.attach_alternative(html_content, "text/html")
    mail.send()

    p.save()

    # return HttpResponseRedirect(reverse('blog:panel'))
    return HttpResponse("Hello")


class PostListView(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts_list'
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['posts_list'] = Post.objects.order_by('-created_at').filter(approved=1)[:5]

        if self.request.user.is_authenticated():
            votes = Voter.objects.filter(user=self.request.user)
            v_list = []

            for vote in votes:
                v_list.append(vote.post.slug)

                context['votes_list'] = v_list

        
        return context


class DetailView(MetadataMixin, generic.DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):

        meta = Meta(
            use_og = True,
            use_twitter = True,
            use_facebook = True,
            use_title_tag = True,
            twitter_card = 'summary_large_image',
            url = "http://earlist.club/producto/" + self.object.slug + '/',
            title = self.object.title + ' | Earlist',
            description = self.object.body,
            image = self.object.image_file.url,
            )

        context = super(DetailView, self).get_context_data(**kwargs)
        context['meta'] = meta
        return context


class PanelListView(generic.ListView):
    template_name = 'blog/panel.html'
    context_object_name = 'posts_list'

    def get_queryset(self):
        return Post.objects.order_by('-created_at')


# class ProfileListView(generic.ListView):
#     model = Post
#     template_name = 'blog/profile.html'
#     context_object_name = 'post'
    
#     def get_context_data(self, **kwargs):

#         context = super(ProfileListView, self).get_context_data(**kwargs)
#         context['posts_list'] = Post.objects.filter(user=self.request.user).order_by('-created_at')[:5]
#         context['votes_list'] = Voter.objects.filter(user=self.request.user).order_by('-created_at')[:5]
        
#         context['events_list'] = Event.objects.order_by('-created_at')[:5]
#         context['my_events_list'] = Event.objects.filter(user=self.request.user).order_by('-created_at')[:5]

#         context['jobs_list'] = Job.objects.order_by('-created_at')[:5]
#         context['my_jobs_list'] = Job.objects.filter(user=self.request.user).order_by('-created_at')[:5]
        
#         return context


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
        form = PostForm(request.POST, request.FILES)
 
        if form.is_valid():
            post = Post.objects.create(
                user = request.user,
            	title = form.cleaned_data['title'],
            	slug = slugify(form.cleaned_data['title']),
                slogan = form.cleaned_data['slogan'],
                body = form.cleaned_data['body'],
            	link = form.cleaned_data['link'],
                image_file = request.FILES['image_file'],
                # image_url = form.cleaned_data['image_url'],
                city = form.cleaned_data['city'],
                approved = 0,
            	created_at = timezone.now()
            	)

            url = reverse('success-post', kwargs={'slug':post.slug})

            return HttpResponseRedirect(url)

        else:
            print form.is_valid()   #form contains data and errors
            print form.errors

 
    return render(request, 'blog/submit_post.html', {
        'form': form,
    })

class PostUpdateView(generic.UpdateView):
    model = Post
    fields = ['slogan', 'body', 'link', 'image_file', 'city']
    template_name = 'blog/update_post.html'
    success_url = '/cuentas/perfil/posts/'


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
    success_url = '/cuentas/perfil/posts/'

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