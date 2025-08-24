from dataclasses import field
from django import forms
from django.contrib.auth.models import User
from localflavor.in_.forms import INStateSelect
from django.core.validators import RegexValidator
from .models import Location, Profile
from .widgets import CustomPictureImageFieldWidget

class UserForm(forms.ModelForm):
    username = forms.CharField(disabled=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    photo = forms.ImageField(widget=CustomPictureImageFieldWidget)
    bio = forms.TextInput()

    class Meta:
        model = Profile
        fields = ('photo', 'bio', 'phone_number')


pincode_validator = RegexValidator(
    regex=r'^\d{6}$',
    message="Enter a valid 6-digit Indian PIN code."
)

class LocationForm(forms.ModelForm):
    address_1 = forms.CharField(required=True)
    zip_code = forms.CharField(
        required=True,
        max_length=6,
        validators=[pincode_validator]
    )
    state = forms.ChoiceField(choices=INStateSelect().choices)

    class Meta:
        model = Location
        fields = ['address_1', 'address_2', 'city', 'state', 'zip_code']