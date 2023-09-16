from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.messages import success, error
from .forms import UserForm, ProfileForm, PaymentForm, ProfileModel
from .models import User, PaymentModel, Messages
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponse, JsonResponse
from .utils import generate_otp
from .decorators import is_admin, is_get, login_required, is_post
import csv

# Create your views here.


class SignupView(View):

    def get(self, request):
        form = UserForm()
        return render(request, 'signup.html', {'form':form})
    
    def post(self, request):
        user = UserForm(request.POST)

        
        if user.is_valid():
            cd = user.cleaned_data
            if User.objects.filter(phone_number=cd['phone_number']).exists():
                error(request, 'قبلا کاربری با این شماره تلفن در سیستم ثبت شده است', extra_tags='danger')
                return redirect('signup_url')
            user.save()
        else:
            print('something went wrong')
        success(request, "ثبت شما با موفقیت انجام شد جهت ادامه شماره همراه خود را از طریق کد پیامکی تایید کنید.", extra_tags='success')
        return redirect('login_url')


class LoginView(View):
    def get(self, request):
        
        return render(request, 'login.html')
    
    def post(self, request):
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        
        if str(phone_number).startswith('0'):
            pn = str(phone_number)
            phone_number = '+98' + pn[1:]

        if phone_number and password:
            user = authenticate(phone_number=phone_number, password=password)
            if user:
                login(request, user)
                success(request, 'شما با موفقیت وارد سیستم شدید!', extra_tags='success')
                return redirect('otp_url')
            else:
                error(request, 'شماره همراه یا رمز عبور اشتباه می باشد', extra_tags="danger")
                return redirect('login_url')
        error(request, 'برای ورود به حساب کاربری هر دو فیلد را باید پر کنید', extra_tags="danger")
        return redirect('login_url')

def logout_view(request):
    logout(request)
    error(request, "شما با موفقیت از سیستم خارج شدید", extra_tags="danger")
    return redirect('home_url')

class ProfileView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            error(request, "شما باید برای دسترسی به این صفحه ابتدا وارد حساب کاربری خود شوید.", extra_tags="danger")
            return redirect('home_url')
        user = User.objects.get(id=request.user.id)
        return render(request, 'profile.html', {'user_':user})
    

class PersonalInfoView(View):

    def get(self, request):
        if request.user.profile.first_name != "":
            return redirect('profile_url')
        profile_form = ProfileForm()
        payment_form = PaymentForm()
        # print(request.user)
        return render(request, 'personalinfo.html', {'profile_form': profile_form, 'payment_form':payment_form})
    def post(self, request):
        user = User.objects.get(id = request.user.id)
        payment = PaymentModel.objects.get(user__id=user.id)
        profile = ProfileModel.objects.get(user__id=user.id)
        payment_form = PaymentForm(request.POST, files=request.FILES)
        profile_form = ProfileForm(request.POST, files=request.FILES)
        if payment_form.is_valid() and profile_form.is_valid():
            cd_pay = payment_form.cleaned_data
            cd_pro = profile_form.cleaned_data
            payment.amount = cd_pay['amount']
            payment.card   = cd_pay['card']
            payment.shaba   = cd_pay['shaba']
            payment.document = cd_pay['document']
            payment.fish = cd_pay['fish']
            payment.save()
            profile.first_name = cd_pro['first_name']
            profile.last_name = cd_pro['last_name']
            profile.national_code = cd_pro['national_code']
            profile.email_address = cd_pro['email_address']
            profile.address = cd_pro['address']
            profile.profile_pic = cd_pro['profile_pic']
            profile.save()
            # PaymentModel.objects.update(amount=cd_pay['amount'], card=cd_pay['card'], shaba=cd_pay['shaba'], document=cd_pay['document'], fish=cd_pay['fish'], user=user)
            # ProfileModel.objects.update(first_name=cd_pro['first_name'], last_name=cd_pro['last_name'], national_code=cd_pro['national_code'], email_address=cd_pro['email_address'], address=cd_pro['address'], profile_pic=cd_pro['profile_pic'], user=user)
            success(request, "ثبت و ارسال اطالاعات شما با موفقیت انجام شد پس از تایید اطلاعات از طریق پیامک به شما اطلاع رسانی خواهد شد.", extra_tags="success")
            return redirect('home_url')
        return redirect('personal_info_url')
    
class OtpView(View):
    def get(self, request):
        if request.user.is_verified:
            return redirect('personal_info_url')
        return render(request, 'otp_verification.html', {'phone': request.user.phone_number})
    
    def post(self, request):
        otp_code = request.POST['otp_code']
        user = User.objects.get(id=request.user.id)
        if otp_code == user.otpcontainer.otpCode:
            user.is_verified = True
            user.save()
            success(request, "تایید شماره شما با موفقیت انجام شد. هم اکنون جهت درخواست وام میتوانید اطلاعات پروفایل خود را تکمیل کنید", extra_tags="success")
            return redirect("personal_info_url")
        else:
            error(request, "در روند تایید شماره همراه شما مشکلی به وجود آمده دوباره تلاش کنید", extra_tags="danger")
            return redirect('otp_url')
    
@api_view(['get'])
def ret_otp(request, phone):
    otp_code = generate_otp(phone)
    return Response({'otp_code':otp_code})
    
@login_required
@is_admin
@is_get
def manage_requests(request):
    profiles = ProfileModel.objects.all()
    payments = PaymentModel.objects.all()
    return render (request,'requests.html', {'profiles':profiles, 'payments':payments})

@is_admin
def delete_user(request, id):
    user = User.objects.get(id=id)
    user.delete()
    success(request, 'کاربر با موفقیت حذف شد', extra_tags='danger')
    return redirect(request.META['HTTP_REFERER'])

def export_csv(request):
    users = User.objects.all()
    data = [
        ['نام', 'نام خانوادگی', 'آدرس ایمیل', 'شماره همراه', 'آدرس محل سکونت', 'شماره کارت', 'شماره شبا', 'مقدار درخواستی'],
    ] + [[_user.profile.first_name, _user.profile.last_name, _user.profile.email_address, _user.phone_number.national_number, _user.profile.address, _user.payment.card, _user.payment.shaba, _user.payment.amount] for _user in users]
    print(data)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'
    writer = csv.writer(response)
    for row in data:
        writer.writerow(row)
    success(request, 'خروجی فایل csv با موفقیت ذخیره و دانلود شد.', extra_tags='success')
    return response

@login_required
@is_admin
def user_detail(request, id):
    user = get_object_or_404(User, id=id)
    return render(request, 'profile.html', {'user_':user, 'is_admin':True})

@is_post
def handle_message(request):
    try:
        Messages.objects.create(email=request.POST['email'], description = request.POST['description'])
        success(request, "پیام شما با موفقیت در سامانه ثبت شد به زودی با شما ارتباط میگیریم.", extra_tags="success")
        return redirect(request.META['HTTP_REFERER'])
    except:
        error(request,"خطا در ارسال پیام.",extra_tags="danger")
        return redirect(request.META['HTTP_REFERER'])