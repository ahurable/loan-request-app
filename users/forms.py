from django import forms
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import RegionalPhoneNumberWidget
from .models import User, ProfileModel, PaymentModel

class UserForm(forms.ModelForm):
    password =  forms.CharField(max_length=12, widget=forms.PasswordInput(attrs={'class':'form-control w-75 my-2', 'placeholder':'رمز عبور خود را وارد کنید', 'name': 'password', 'id':'password'}))
    class Meta:
        model = User
        fields = ['phone_number']
        widgets = {
            'phone_number':RegionalPhoneNumberWidget(region='IR', attrs={'class':'form-control w-75 my-2', 'placeholder':'شماره تلفن همراه خود را وارد کنید', 'id':'phone_number'})
        }

    def clean(self):
        cd = self.cleaned_data
        if cd['phone_number'] and cd['password']:
            return cd
        else:
            raise ValidationError("You have to fill both fields of phone number and password!")

    def save(self, commit=False):
        instance = super().save(commit)
        cd = super().clean()
        instance.set_password(cd['password'])
        instance.save()


class ProfileForm(forms.ModelForm):
    class Meta:
        model = ProfileModel
        fields = ['first_name', 'last_name', 'national_code', 'email_address', 'address', 'profile_pic']
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control my-3 w-75', 'placeholder':'نام خود را وارد کنید'}),
            'last_name': forms.TextInput(attrs={'class':'form-control my-3 w-75', 'placeholder':'نام خانوادگی خود را وارد کنید'}),
            'national_code': forms.TextInput(attrs={'class':'form-control my-3 w-75', 'placeholder':'کد ملی خود را وارد کنید'}),
            'email_address': forms.TextInput(attrs={'class':'form-control my-3 w-75', 'placeholder':'آدرس ایمیل خود را وارد کنید'}),
            'address': forms.TextInput(attrs={'class':'form-control my-3 w-75', 'placeholder':'آدرس محل سکونت خود را وارد کنید'}),
            'profile_pic': forms.FileInput(attrs={'class':'form-control my-3 w-75'})
        }
        labels = {
            'profile_pic': 'عکس پروفایل کاربری',
            'first_name':'',
            'last_name':'',
            'national_code':'',
            'email_address':'',
            'address':'',
        }

class PaymentForm(forms.ModelForm):
    class Meta: 
        model = PaymentModel
        fields = ['amount', 'card', 'shaba', 'document', 'fish']
        widgets = {
            'amount': forms.TextInput(attrs={'class':'form-control my-3 w-75', 'placeholder':'مقدرا درخواستی خود را وارد کنید'}),
            'card': forms.TextInput(attrs={'class':'form-control my-3 w-75', 'placeholder':'شماره کارت خود را وارد کنید'}),
            'shaba': forms.TextInput(attrs={'class':'form-control my-3 w-75', 'placeholder':'شماره شبا خود را وارد کنید'}),
            'document': forms.FileInput(attrs={'class':'form-control my-3 w-75 d-none'}),
            'fish': forms.FileInput(attrs={'class':'form-control my-3 w-75 d-none'}),
        }
        labels = {
            'amount':'',
            'card':'',
            'shaba':'',
            'document':'',
            'fish':''
        }