# import requests
# import json

from .models import *

# url = "https://api2.ippanel.com/api/v1/sms/pattern/normal/send"

# payload = json.dumps({
#   "code": "g6jn2zy91pami2b",
#   "sender": "+98500010707",
#   "recipient": "09903392645",
#   "variable": {
#     "otp_code": "123456"
#   }
# })
# headers = {
#   'apikey': 'NBWiGcNJje96Wnul1geCbf412JsCsMIFfJwGBqMkDJU=',
#   'Content-Type': 'application/json'
# }

# response = requests.request("POST", url, headers=headers, data=payload)

# print(response.text)

# data = [
#     ['phone_number', 'is_admin'],
#     [phone_number, is_admin] for [phone_number, is_admin] in ...]
# ]

users = User.objects.all()
print(users)