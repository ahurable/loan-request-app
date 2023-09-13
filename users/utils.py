from .models import User, OtpContainer
from random import randint
from ippanel import Client
import requests
import json

api_key = "NBWiGcNJje96Wnul1geCbf412JsCsMIFfJwGBqMkDJU="
sms = Client(api_key)

def send_otp(phone_number):
    sms.send(originator="+9810001", recipients=[phone_number], message="")

def generate_otp(phone_number: str):
    # Generate OTP and Send it to the phone number.
    if phone_number:
        if phone_number.startswith('9'):
            phone_number = '+' + phone_number
        otp = randint(100000, 999999)
        print(otp)
        user = User.objects.get(phone_number=phone_number)
        instance = OtpContainer.objects.get(user=user)
        instance.otpCode = otp
        instance.save()
        sms_send(phone_number, otp)
        return otp
    
    return Exception("you have to set the value of phone number")


def sms_send(phone_number, otp_code):
    url = "https://api2.ippanel.com/api/v1/sms/pattern/normal/send"

    payload = json.dumps({
    "code": "g6jn2zy91pami2b",
    "sender": "+98500010707",
    "recipient": str(phone_number),
    "variable": {
        "otp_code": str(otp_code)
    }
    })
    headers = {
    'apikey': 'NBWiGcNJje96Wnul1geCbf412JsCsMIFfJwGBqMkDJU=',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)