from django.core.management.base import BaseCommand, CommandError
from blog.models import Post, Event, Job, Voter, Sponsor, Newsletter
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
import datetime
import datetime as dt
from datetime import datetime, timedelta
from django.template.loader import get_template
from django.template import Context, RequestContext

class Command(BaseCommand):

    def handle(self, *args, **options):

        how_many_days = 100
        today = dt.date.today()
        p = Post.objects.order_by('-votes').filter(approved=1).filter(date__gte=datetime.now()-timedelta(days=how_many_days))[:5]
        events = Event.objects.order_by('date').filter(date__year=today.year, date__month=today.month)[:3]
        jobs = Job.objects.order_by('-created_at')[:10]
        sponsors = Sponsor.objects.order_by('-created_at')[:2]
        special = Post.objects.order_by('-created_at').filter(approved=1).filter(date__gte=datetime.now()-timedelta(days=how_many_days)).filter(sponsored=1)[:5]
            
        if p:

            u = User.objects.filter(groups__isnull=True)
            # email = 'priveras@gmail.com'
            plaintext = get_template('blog/emails/newsletter.txt')
            htmly     = get_template('blog/emails/newsletter.html')
            subject = 'Lo mejor de la semana en Earlist'

            for user in u:
                email = user.email
                d = Context({ 'posts_list': p, 'user_unsubscribe_id': user.id, 'username': user.username, 'events': events, 'jobs': jobs, 'sponsors':sponsors, 'special': special })
                text_content = plaintext.render(d)
                html_content = htmly.render(d)
                from_email, to = 'Earlist <hola@earlist.xyz>', email
                mail = EmailMultiAlternatives(subject, text_content, from_email, [to])
                mail.attach_alternative(html_content, "text/html")
                mail.send()

            u_n = Newsletter.objects.all()

            for user in u_n:
                email = user.email
                d = Context({ 'posts_list': p, 'events': events, 'jobs': jobs, 'sponsors':sponsors, 'special': special })
                text_content = plaintext.render(d)
                html_content = htmly.render(d)
                from_email, to = 'Earlist <hola@earlist.xyz>', email
                mail = EmailMultiAlternatives(subject, text_content, from_email, [to])
                mail.attach_alternative(html_content, "text/html")
                mail.send()
        
