from django.contrib import admin
from .models import User, OtpContainer, PaymentModel, ProfileModel
# Register your models here.


admin.site.register(User)
admin.site.register(OtpContainer)
admin.site.register(ProfileModel)
admin.site.register(PaymentModel)
