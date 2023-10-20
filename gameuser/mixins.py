from http import client
import random
from django.conf import settings
from twilio.rest import Client 

class MessageHandler:
    def __init__(self, phone_number, otp) -> None:
        self.phone_number = phone_number
        self.otp          = otp

    def send_otp_to_phone(self):
        client = Client(settings.ACCOUNT_SID,settings.AUTH_TOKEN)
        verification = client.verify \
                     .v2 \
                     .services('VA32e120535e6fb3674f8e0e2d67504ef4') \
                     .verifications \
                     .create(to=self.phone_number, channel='sms')

    def validate(self):
        client=Client(settings.ACCOUNT_SID,settings.AUTH_TOKEN)
        verification_check = client.verify \
                           .v2 \
                           .services('VA32e120535e6fb3674f8e0e2d67504ef4') \
                           .verification_checks \
                           .create(to=self.phone_number,code=self.otp)
        validation=verification_check.status
        print(validation)
        return validation    