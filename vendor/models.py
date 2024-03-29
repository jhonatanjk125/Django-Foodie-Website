from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import sendNotification
from datetime import time, date, datetime

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

    def is_open(self):
        today = date.today().isoweekday()
        current_opening_hours = OpeningHours.objects.filter(vendor=self,day=today)
        now = datetime.now()
        current_time = now.strftime('%H:%M:%S')
        is_open_now = None
        try:
            for hour in current_opening_hours:
                start_time = str(datetime.strptime(hour.from_hour, '%I:%M %p').time())
                end_time = str(datetime.strptime(hour.to_hour, '%I:%M %p').time())
                if start_time<current_time<end_time:
                    is_open_now = True
                    break
                else:
                    is_open_now = False
        except ValueError:
            pass

        return is_open_now

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

DAYS = [
    (1, ('Monday')),
    (2, ('Tuesday')),
    (3, ('Wednesday')),
    (4, ('Thursday')),
    (5, ('Friday')),
    (6, ('Saturday')),
    (7, ('Sunday')),
]

TIME_CHOICES = [(time(h,m).strftime('%I:%M %p'), time(h,m).strftime('%I:%M %p')) for h in range(0,24) for m in(0,30)]
class OpeningHours(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    day = models.IntegerField(choices=DAYS)
    from_hour= models.CharField(choices=TIME_CHOICES, max_length=10, blank=True)
    to_hour = models.CharField(choices=TIME_CHOICES, max_length=10, blank=True)
    is_closed = models.BooleanField(default=False)

    class Meta:
        ordering = ('day', '-from_hour')
        unique_together = ('vendor', 'day', 'from_hour', 'to_hour')


    def __str__(self):
        return self.get_day_display()
