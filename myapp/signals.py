from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from allauth.socialaccount.signals import social_account_added
from django.dispatch import receiver

@receiver(user_signed_up)
def set_username(request, user, **kwargs):
    if user.first_name:
        user.username = user.first_name
        user.save()


@receiver(social_account_added)
def link_existing_account(request, sociallogin, **kwargs):
    user = sociallogin.user

    if user.email:
        from django.contrib.auth.models import User

        existing = User.objects.filter(email=user.email).first()

        if existing:
            sociallogin.connect(request, existing)