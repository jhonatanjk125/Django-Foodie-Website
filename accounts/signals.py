from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, UserProfile


@receiver(post_save, sender=User)
def post_save_profile_receiver(sender, instance, created, **kwargs):
    print('executed')
    #Create profile when user is created
    if created:
        UserProfile.objects.create(user=instance)
        print('created') 
    #Update profile when user is updated
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except:
            # Create user profile when user is updated (in case it doesn't exist)
            UserProfile.objects.create(user=instance)