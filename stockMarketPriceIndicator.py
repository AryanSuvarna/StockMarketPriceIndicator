'''
TESTING FOR SMS, EMAIL, SYS NOTI. working all together
'''

# imports
import requests
from email.message import EmailMessage
import ssl
import smtplib
import time
from plyer import notification as noti  # module for system notifications

# modules for SMS service
import os
from twilio.rest import Client


# API Key from the website
API_KEY = ""

# App password to connect gmail with Python (see video linked above)
PASSWORD = ""

# password of the email address you are sending emails from
EMAIL_PASS = ""

# Twilio SMS requirements
account_sid = ""
auth_token = ""

# Variables (change these based on what you are looking for and how you want to send your emails)
TARGET = 0
TICKER = ""
EMAIL_SENDER = ""  # make sure this is a gmail account
EMAIL_RECEIVER = ""


# send a SMS
def send_sms(name, current_price):
    client = Client(account_sid, auth_token)
    client.messages.create(
        body=f"\n\n{name} has crossed ${TARGET} \n\nCurrent Price: ${current_price}",
        from_='+19785156670',
        to=os.environ.get('MY_NUMBER')
    )


def send_email(name, current_price):
    subject = f"{name} target reached"
    body = f"{name} has crossed ${TARGET} \n\nCurrent Price: ${current_price}"

    em = EmailMessage()
    em['From'] = EMAIL_SENDER
    em['To'] = EMAIL_RECEIVER
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(EMAIL_SENDER, PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, em.as_string())

    print("Email sent!")


def time_converter(timeInput):
    return time.strftime('%H:%M', time.localtime(timeInput))


def check(valid):
    info = requests.get(
        f"https://financialmodelingprep.com/api/v3/quote/{TICKER}?apikey={API_KEY}").json()

    # if ticker name is not valid
    if info == []:
        valid = False
        print("Ticker and/or API key is not valid!")
        return valid

    name = info[0]['name']
    current_price = info[0]['price']
    current_time = info[0]['timestamp']
    converted_time = time_converter(current_time)
    print(f"Current {name} Price: ${current_price}  Time: {converted_time}")

    if current_price < TARGET:
        noti.notify(title="Stock Market Price Indicator",
                    message=f"{name} has crossed desired target price!",
                    timeout=10)
        send_email(name, current_price)
        send_sms(name, current_price)
    return valid


valid = True
while(valid):
    # With free plan on Financial Modeling Prep website, can send a request call once every 6 minutes (250 calls/day)
    if not check(valid):
        break
    time.sleep(360)
