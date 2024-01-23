from http import client
import random
from django.conf import settings
from django.shortcuts import redirect,render
from twilio.rest import Client 
from twilio.base.exceptions import TwilioException
from django.http import HttpResponse, HttpResponseServerError


class MessageHandler:
    def __init__(self, phone_number, otp) -> None:
        self.phone_number = phone_number
        self.otp          = otp

    def send_otp_to_phone(self,request):
        try:
            client = Client(settings.ACCOUNT_SID,settings.AUTH_TOKEN)
            print("CAMEDA AHETER")
            verification = client.verify \
                         .v2 \
                         .services('VAc38a04f413d33237a17135c36ece12b9') \
                         .verifications \
                         .create(to=self.phone_number, channel='sms')
            return "Succesfully send OTP"
        except TwilioException as e:
            print(f"TwilioException: {e}")
            return "Failed to send OTP"
        except Exception as e:
            print(f"Exception: {e}")
        else:
            print("No Exception Occured..!")


    def validate(self):
        print("SURCOME STANCES")
        client=Client(settings.ACCOUNT_SID,settings.AUTH_TOKEN)
        verification_check = client.verify \
                           .v2 \
                           .services('VAc38a04f413d33237a17135c36ece12b9') \
                           .verification_checks \
                           .create(to=self.phone_number,code=self.otp)
        validation=verification_check.status
        print("BBJHBHHJBJ")
        print(validation)
        return validation    