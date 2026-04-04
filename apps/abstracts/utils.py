from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _


from settings.base import HOME_PAGE_URL
from apps.users.models import CustomUser 

def send_welcome_email(user: CustomUser) -> None:
    """Sends welcome Email on Users preferred language"""
    lang = user.preferred_language

    html = render_to_string(f'welcome/{lang}.html', {
        'user_name': user,
        'site_url': HOME_PAGE_URL
    })

    send_mail(
        subject=_('Welcome'),
        message='',
        html_message=html,
        from_email='noreply@blog.kz',
        recipient_list=[user.email]
    )