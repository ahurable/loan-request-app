from  django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
from .models import User, OtpContainer, ProfileModel,PaymentModel
from .utils import generate_otp

@receiver(post_save, sender=User)
def create_otp(sender, instance, created, **kwargs):
    if created:
        
        OtpContainer.objects.create(user=instance)
        ProfileModel.objects.create(user=instance)
        PaymentModel.objects.create(user=instance)