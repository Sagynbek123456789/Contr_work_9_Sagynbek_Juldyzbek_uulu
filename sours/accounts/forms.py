from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.validators import RegexValidator

from accounts.models import Profile


class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']
        labels = {'first_name': 'Имя', 'last_name': 'Фамилия', 'email': 'Email', 'phone_number': 'Телефон'}


class ProfileChangeForm(forms.ModelForm):
    phone_regex = RegexValidator(regex=r'^\+996 \d{3} \d{3} \d{3}$', message="Номер телефона должен быть в формате: '+996 XXX XXX XXX'.")
    phone_number = forms.CharField(validators=[phone_regex], max_length=17, required=False)  # validators should be a list
    class Meta:
        model = Profile
        fields = ['avatar', 'birth_date', 'phone_number']
