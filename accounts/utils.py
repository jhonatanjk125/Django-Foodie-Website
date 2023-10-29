from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings
from .models import User


def detectUser(user):
    """ Defines if the user that's logged in is a customer/vendor/admin"""
    if user.role == 1:
        redirectUrl = 'vendorDashboard'
    elif user.role == 2:
        redirectUrl = 'customerDashboard'
    elif user.role == None and user.is_superadmin:
        redirectUrl = '/admin'
    return redirectUrl


def sendVerificationEmail(request, user, email_subject, email_template):
    """Helper function to send the verification email when a new account is created"""
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    context = {
        'user':user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    }
    message = render_to_string(email_template, context)
    to_email = user.email
    email = EmailMessage(email_subject, message, from_email, to=[to_email])
    email.send()


def getUserFromPK(uidb64):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
        return (user, uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None


def sendNotification(email_subject, email_template, context):
    from_email = settings.DEFAULT_FROM_EMAIL
    message = render_to_string(email_template, context)
    to_email = context['user'].email
    email = EmailMessage(email_subject, message, from_email, to=[to_email])
    email.send()