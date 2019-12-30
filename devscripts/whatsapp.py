import os
import configparser
from twilio.rest import Client

config = configparser.ConfigParser()
config.read('../config.ini')

TWILIO_ACCOUNT_SID = config['TWILLIO']['TWILIO_ACCOUNT_SID']
TWILIO_AUTH_TOKEN = config['TWILLIO']['TWILIO_AUTH_TOKEN']
TWILLIO_SANDBOX_WA = config['TWILLIO']['TWILLIO_SANDBOX_WA']
KONT_WA = config['TWILLIO']['KONT_WA']
MY_WA = config['TWILLIO']['MY_WA']

os.environ['TWILIO_ACCOUNT_SID'] = TWILIO_ACCOUNT_SID
os.environ['TWILIO_AUTH_TOKEN'] = TWILIO_AUTH_TOKEN

# client credentials are read from TWILIO_ACCOUNT_SID and AUTH_TOKEN
client = Client()

# this is the Twilio sandbox testing number
from_whatsapp_number = KONT_WA
# replace this number with your own WhatsApp Messaging number
to_whatsapp_number = MY_WA

client.messages.create(body='Ahoy, world!',
                       #                        application_sid=TWILIO_ACCOUNT_SID,
                       from_=from_whatsapp_number,
                       to=to_whatsapp_number)
