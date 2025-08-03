from django import forms
from django.contrib.auth.models import User
from .models import FrontCard, BackCard,UserPaymentInfo
from django_countries.widgets import CountrySelectWidget

class FrontGiftForm(forms.ModelForm):
    class Meta:
        model = FrontCard
        fields = ['image']

class BackGiftForm(forms.ModelForm):
    class Meta:
        model = BackCard
        fields = ['image']

class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)


class PaymentInfo(forms.ModelForm):
    class Meta:
        model = UserPaymentInfo
        fields = ['name', 'email', 'country']
        widgets = {
            'country': CountrySelectWidget(attrs={'class': 'styled-select'}),
        }


class UserRegistrationForm(forms.ModelForm):
	password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={"rows":"4", "cols":"50px","placeholder":"Password !!!"}))
	password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput(attrs={"rows":"4", "cols":"50px","placeholder":"Repeat Password !!!"}))
	class Meta:
		model = User
		fields = ('username', 'first_name','last_name', 'email')

	def clean_password2(self):
		cd = self.cleaned_data
		if cd['password'] != cd['password2']:
			raise forms.ValidationError('Passwords don\'t match.')
		return cd['password2']