from django import forms
from vendor.models import Vendor,OpeningHours
from accounts.validators import only_allow_images

class VendorForm(forms.ModelForm):
    vendor_license = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[only_allow_images])
    class Meta:
        model = Vendor
        fields = ['vendor_name', 'vendor_license']


class OpeningHoursForm(forms.ModelForm):
    class Meta:
        model = OpeningHours
        fields = ['day', 'from_hour', 'to_hour','is_closed']