# -*- coding: utf-8 -*-
from django.views import generic
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from .models import Post, Event, Job, Voter, Sponsor
from .forms import PostForm, JobForm,EventForm
from django.utils.text import slugify
from django.contrib.auth import logout
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context, RequestContext
from earlist.secret import api
from earlist.secret import cfg
import datetime as dt
from datetime import datetime, timedelta
from meta.views import Meta, MetadataMixin
import twitter
import facebook

meta = Meta(
        use_og = True,
        use_twitter = True,
        use_facebook = True,
        use_title_tag = True,
        url = "http://earlist.xyz/",
        title = 'Earlist | Descubre Startups y Eventos de innovación en México',
        description = 'Earlist es el lugar donde podrás publicar, votar o enterarte de las mejores startups, eventos y productos de tecnología en Mexico.',
        image = 'https://scontent.fmex8-2.fna.fbcdn.net/v/t31.0-8/19693860_1544598535590554_9103271582238767312_o.png?oh=c46969531924039baa120da86bc14fdf&oe=5A077A72',
        )

class NewsletterView(generic.TemplateView):
    template_name = "blog/emails/newsletter.html"

def events(
        request,
        template='blog/entry_events.html',
        page_template='blog/entry_events_page.html'):

    orders = [ '-created_at']
    today = dt.date.today()

    context = {
        'events_list': Event.objects.order_by('date').filter(date__year=today.year, date__month=today.month),
        'page_template': page_template,
        'meta': meta,
        'today': today,
        'sponsors': Sponsor.objects.order_by('-created_at')
    }

    if request.is_ajax():
        template = page_template
    return render(request, template, context)

class AboutView(generic.TemplateView):
    template_name = "blog/about.html"

class UnsubscribedView(generic.TemplateView):
    template_name = "blog/unsubscribed.html"

def unsubscribe(request, id):
    try:
        g = Group.objects.get(name='unsubscribed') 
    except:
        g = Group.objects.create(name='unsubscribed')

    id_user = User.objects.filter(id=id)
    
    g.user_set.add(id_user.user.id)

    return HttpResponseRedirect(reverse('blog:unsubscribed'))

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
        'meta': meta,
        'sponsors' : Sponsor.objects.order_by('-created_at')
    }

    if request.user.is_authenticated():
        events = Event.objects.filter(user=request.user).order_by('-created_at')
        votes = Voter.objects.filter(user=request.user)
        v_list = []
        for vote in votes:
            v_list.append(vote.post.slug)
            context['votes_list'] = v_list
            context['events'] = events

    if request.is_ajax():
        template = page_template
    
    return render(request, template, context)

def index(
        request,
        template='blog/index.html',
        page_template='blog/index_page.html'):

    orders = [ '-created_at', 'name' ]

    context = {
        'posts_list': Post.objects.order_by('-date', '-votes').filter(approved=1),
        'page_template': page_template,
        'meta': meta,
        'panel_count': Post.objects.filter(approved=0).count(),
        'sponsors': Sponsor.objects.order_by('-created_at')
    }

    if request.user.is_authenticated():
        votes = Voter.objects.filter(user=request.user)
        v_list = []
        for vote in votes:
            v_list.append(vote.post.slug)
            context['votes_list'] = v_list

    if request.is_ajax():
        template = page_template
    return render(request, template, context)

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

        api.PostMedia("%s: %s http://earlist.xyz/producto/%s via @%s" % (p.title, p.slogan, p.slug, p.user), request.build_absolute_uri(p.image_file.url))

        def main():
        # Fill in the values noted in previous steps here

            api = get_api(cfg)
            msg = "%s: %s http://earlist.xyz/producto/%s" % (p.title, p.slogan, p.slug)
            attachment =  {
                'name': p.title + " | Earlist",
                'link': "http://earlist.xyz/producto/" + p.slug,
                'caption': p.slogan,
                'description': p.body,
                'picture': request.build_absolute_uri(p.image_file.url)
            }
            status = api.put_wall_post(msg, attachment)

        def get_api(cfg):
            graph = facebook.GraphAPI(cfg['access_token'])
            # Get page token to post as the page. You can skip 
            # the following if you want to post as yourself. 
            resp = graph.get_object('me/accounts')
            page_access_token = None
            for page in resp['data']:
                if page['id'] == cfg['page_id']:
                    page_access_token = page['access_token']
            graph = facebook.GraphAPI(page_access_token)
            return graph

            # You can also skip the above if you get a page token:
            # http://stackoverflow.com/questions/8231877/facebook-access-token-for-pages
            # and make that long-lived token as in Step 3

        main()
        
    else:
        p.approved = 2

        if message == '2':
            error = 'Hay errores en la publicación. Te invitamos a revisar que la imagen se vea bien, que no haya errores en el texto y que se usen el número de caracteres adecuados en la descripción. Puedes editar la publicación en tu perfil.'

        elif message == '3':
            error = 'Por el momento no podremos publicar esto en nuestro sitio. Si lo deseas puedes ser un patrocinador del sitió y aparecer en la zona de los banners. Para más información por favor mandanos un mail a hola@earlist.xyz.'

        else:
            error = 'Este tipo de publicación no está en linea con el tipo de contenido que mostramos en Earlist. Lamentablemente no podremos publicar esto. Te invitamos a seguir siendo parte de nuestra comunidad y a hacer publicaciones que van de acuerdo a nuestro contenido.'

        d = Context({ 'first_name': p.user.first_name, 'error': error, 'title': p.title })
        plaintext = get_template('blog/emails/declined.txt')
        htmly     = get_template('blog/emails/declined.html')
        subject = 'Tu publicacion ha sido declinada'        

    from_email, to = 'Earlist <hola@earlist.xyz>', email
    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    mail = EmailMultiAlternatives(subject, text_content, from_email, [to])
    mail.attach_alternative(html_content, "text/html")
    mail.send()

    p.save()

    return HttpResponseRedirect(reverse('blog:panel'))
    # return HttpResponse("Hello")


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
            url = "http://earlist.xyz/producto/" + self.object.slug + '/',
            title = 'Earlist | ' + self.object.title,
            description = self.object.body,
            image = self.object.image_file.url,
            )

        context = super(DetailView, self).get_context_data(**kwargs)
        context['meta'] = meta
        context['sponsors'] = Sponsor.objects.order_by('-created_at')
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


# class EventListView(generic.ListView):
# 	template_name = 'blog/events.html'
# 	context_object_name = 'events_list'

# 	def get_queryset(self):
# 		return Event.objects.order_by('-date_time')

class JobListView(generic.ListView):
    template_name = 'blog/jobs.html'
    context_object_name = 'jobs_list'
    model = Job

    def get_context_data(self, **kwargs):
        context = super(JobListView, self).get_context_data(**kwargs)
        context['users_list'] = Job.objects.order_by('-created_at')
        context['meta'] = meta
        context['sponsors'] = Sponsor.objects.order_by('-created_at')

        return context


def logout_view(request):
    logout(request)


class SuccessPostView(generic.DetailView):
    model = Post
    template_name = 'blog/success-post.html'

class SuccessEventView(generic.DetailView):
    model = Event
    template_name = 'blog/success-event.html'

class ContributeView(generic.TemplateView):
    template_name = 'blog/contribute.html'
    

def post(request):
    if request.method == 'GET':
        form = PostForm()
    else:
        form = PostForm(request.POST, request.FILES)
 
        if form.is_valid():

            try: 
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

            except IntegrityError as e:
                if 'UNIQUE constraint failed: blog_post.slug' in e.message:
                    error = "¡Oops! Ese producto ya existe en Earlist."
                else:
                    error = "¡Oops! Esa url ya existe en Earlist."

                return render(request, 'blog/submit_post.html', {
                        'form': form,
                        'error': error
                        })
        else:
            print form.is_valid()   #form contains data and errors
            print form.errors
 
    return render(request, 'blog/submit_post.html', {
        'form': form,
        'meta': meta
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
                # slug = slugify(form.cleaned_data['title']),
                body = form.cleaned_data['body'],
                link = form.cleaned_data['link'],
                image_file = request.FILES['image_file'],
                date = form.cleaned_data['date_time'],
                time = form.cleaned_data['date_time'],
                created_at = timezone.now()
                )

            url = reverse('success-event', kwargs={'pk':event.pk})

            return HttpResponseRedirect(url)

        else:
            print form.is_valid()   #form contains data and errors
            print form.errors
 
    return render(request, 'blog/submit_event.html', {
        'form': form,
    })


    