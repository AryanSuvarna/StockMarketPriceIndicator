'''
Here I have created a stock market application that sends the user an email and a system notification when a specified stock
or cryptocurrency has crossed below a specified target. I have utilized the Financial Modeling Prep API to make this possible.

Follow this video to send emails using Python: https://www.youtube.com/watch?v=g_j6ILT-X0k
(other methods are currently not working so watch the above link^)
'''

# imports
import requests
from email.message import EmailMessage
import ssl
import smtplib
import time
from plyer import notification as noti  # module for system notifications

# API Key from the website
API_KEY = ""

# App password to connect gmail with Python (see video linked above)
PASSWORD = ""

# password of the email address you are sending emails from
EMAIL_PASS = ""

# Variables (change these based on what you are looking for and how you want to send your emails)
TARGET = 20500
TICKER = "BTCUSD"
EMAIL_SENDER = "aryantestingemail@gmail.com"
EMAIL_RECEIVER = "aryansat@hotmail.com"


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


def check():
    info = requests.get(
        f"https://financialmodelingprep.com/api/v3/quote/{TICKER}?apikey={API_KEY}").json()

    name = info[0]['name']
    current_price = info[0]['price']
    current_time = info[0]['timestamp']
    converted_time = time_converter(current_time)
    print(f"Current {name} Price: ${current_price}  Time: {converted_time}")

    if current_price < TARGET:
        noti.notify(title="Message from PC",
                    message="Hello World!",
                    timeout=10)
        send_email(name, current_price)


while(True):
    check()
    # With free plan on Financial Modeling Prep website, can send a request call once every 6 minutes (250 calls/day)
    time.sleep(360)
