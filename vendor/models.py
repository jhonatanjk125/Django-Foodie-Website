from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import sendNotification

# Create your models here.
class Vendor(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=50)
    vendor_slug = models.SlugField(max_length=100, unique=True)
    vendor_license = models.ImageField(upload_to='vendor/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name

    def save(self, *args, **kwargs):
        # Check if the vendor object has already been created
        if self.pk is not None:
            orig = Vendor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                email_template = 'accounts/emails/admin_approval_email.html'
                context = {
                    'user' : self.user,
                    'is_approved' : self.is_approved,
                }
                if self.is_approved == True:
                    email_subject = 'Congratulations! Your business has been approved!'
                    sendNotification(email_subject, email_template, context)
                else:
                    email_subject = "Sorry, you're not eligible for publishing on the marketplace."
                    sendNotification(email_subject, email_template, context)
                    
                    

        return super().save(*args, **kwargs)