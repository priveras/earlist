from django.core.management.base import BaseCommand, CommandError
from blog.models import Post, Event, Job, Voter
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
import datetime
from datetime import datetime, timedelta
from django.template.loader import get_template
from django.template import Context, RequestContext

class Newsletter(BaseCommand):
    how_many_days = 7
    p = Post.objects.order_by('-votes').filter(date__gte=datetime.now()-timedelta(days=how_many_days))[:5]

    if p:

        u = User.objects.filter(groups__isnull=True)
        # email = 'priveras@gmail.com'
        plaintext = get_template('blog/emails/newsletter.txt')
        htmly     = get_template('blog/emails/newsletter.html')
        subject = 'Lo mejor de la semana en Earlist'

        for user in u:
            email = user.email
            d = Context({ 'posts_list': p, 'user_unsubscribe_id': user.id })
            text_content = plaintext.render(d)
            html_content = htmly.render(d)
            from_email, to = 'Earlist <hey@earlist.club>', email
            mail = EmailMultiAlternatives(subject, text_content, from_email, [to])
            mail.attach_alternative(html_content, "text/html")
            mail.send()
        
