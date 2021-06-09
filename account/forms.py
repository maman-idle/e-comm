from django import forms
from django.db.models import fields
from django.forms import ModelForm
from django.forms.widgets import PasswordInput
from .models import Account, Product
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm


class MyCreateUserForm(UserCreationForm):
    password1 = forms.CharField(label="Password", max_length=16, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(label="Password Confirmation", max_length=16, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password confirmation'}))

    class Meta:
        model = Account
        fields = ['username', 'email', 'password1',
                  'password2', 'phone', 'address']
        widgets = {
            'username': forms.fields.TextInput(attrs={'class': 'form-control', 'autofocus': True, 'placeholder': 'Username'}),
            'email': forms.fields.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': forms.fields.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'address': forms.fields.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
        }

    def save(self, commit=True):
        user = super(MyCreateUserForm, self).save(commit=True)
        user.is_staff = False
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.password1 = self.cleaned_data['password1']
        user.password2 = self.cleaned_data['password2']
        user.phone = self.cleaned_data['phone']
        user.address = self.cleaned_data['address']
        user.group = Group.objects.get(name="customer")

        if commit:
            user.save()

        return user


class MyCreateStaffForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ['username', 'email', 'password1',
                  'password2', 'phone', 'address']

    def save(self, commit=True):
        user = super(MyCreateUserForm, self).save(commit=True)
        user.is_staff = True
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.password1 = self.cleaned_data['password1']
        user.password2 = self.cleaned_data['password2']
        user.phone = self.cleaned_data['phone']
        user.address = self.cleaned_data['address']

        if commit:
            user.save()

        return user


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
