from django.contrib import admin
from .models import User, OtpContainer, PaymentModel, ProfileModel, Messages
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['phone_number',]
    list_filter = ['is_verified', 'is_admin']

@admin.register(PaymentModel)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'card']
    list_filter = ['amount']


@admin.register(ProfileModel)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['national_code', 'first_name', 'last_name', 'email_address']

@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ['email', 'description']
    list_filter = ['email', 'created']


admin.site.register(OtpContainer)