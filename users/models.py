from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
from random import randint
import os
# different images upload paths: 

def document_upload(instance, file):
    name, ext = os.path.splitext(os.path.basename(file))
    return f'users/documents/{instance.id}{ext}'

def fish_upload(instance, file):
    name, ext = os.path.splitext(os.path.basename(file))
    return f'users/fishs/{instance.id}{ext}'

def profile_upload(instance, file):
    name, ext = os.path.splitext(os.path.basename(file))
    return f'users/profile/{instance.id}-{randint(0, 99)}{ext}'

class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        user = self.model(
            phone_number=phone_number
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        user = self.create_user(
            phone_number=phone_number,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):

    phone_number = PhoneNumberField(region='IR', unique=True)
    is_admin     = models.BooleanField(default=False)
    is_verified  = models.BooleanField(default=False)

    objects         = UserManager()
    USERNAME_FIELD  = 'phone_number'


    def __str__(self) -> str:
        return str(self.phone_number)
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
    @property
    def is_staff(self):
        return self.is_admin
    
class OtpContainer(models.Model):
    otpCode = models.CharField('OTP Code', max_length=6 , blank=True,)
    user    = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="otp")

    def __str__(self):
        return f'{self.otpCode} - {self.user}'

# we using ProfileModel in PersonalInfoView view class
class ProfileModel(models.Model):
    first_name = models.CharField(max_length=60)
    last_name  = models.CharField(max_length=60)
    national_code = models.IntegerField(null=True, blank=True)
    email_address = models.EmailField(null=True, blank=True)
    address       = models.TextField(null=True, blank=True)
    profile_pic   = models.ImageField(upload_to=profile_upload, null=True, blank=True, default='/media/site/avatar.svg')
    user          = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="profile")

    def __str__(self) -> str:
        return str(self.first_name + ' ' + self.last_name)
    
class PaymentModel(models.Model):
    amount        = models.IntegerField(null=True, blank=True)
    card          = models.IntegerField(null=True, blank=True)
    shaba         = models.CharField(max_length=25,null=True, blank=True)
    document      = models.ImageField(upload_to=document_upload, null=True, blank=True)
    fish          = models.ImageField(upload_to=fish_upload, null=True, blank=True)
    user          = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="payment")

    def __str__(self):
        return str(self.id)