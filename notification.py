from twilio.rest import Client

TWILIO_SID = "AC520b8a6df173dde831e9ccad505fda04"
TWILIO_AUTH_TOKEN = "5f13e5bca16a2cbc659bed228fccdea4"
TWILIO_VIRTUAL_NUMBER = "+16188935313"
TWILIO_VERIFIED_NUMBER = "+37064448830"


class NotificationManager:

    def __init__(self):
        self.client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    def send_sms(self, message):
        message = self.client.messages.create(
            body=message,
            from_=TWILIO_VIRTUAL_NUMBER,
            to=TWILIO_VERIFIED_NUMBER,
        )
        # Prints if successfully sent.
        print(message.sid)
