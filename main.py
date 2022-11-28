# import modules for system notification and email
import requests
from email.message import EmailMessage
import ssl
import smtplib
from plyer import notification as noti  # module for system notifications

# import modules for SMS service
from twilio.rest import Client

# import module for GUI
import PySimpleGUI as sg

# API Key from the website
API_KEY = ""

# App password to connect gmail with Python (see video linked above)
PASSWORD = ""

# password of the email address you are sending emails from
EMAIL_PASS = ""

# Twilio SMS requirements
account_sid = ""
auth_token = ""

# Variables (change email info based on how you want to send your emails)
EMAIL_SENDER = ""  # make sure this is a gmail account
EMAIL_RECEIVER = ""
PHONE_NUMBER = ""
global TARGET, TICKER
states=  {"BUY" : "below", "SELL": "above"}

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# GUI initilization

font = ('Arial', 16)
sg.theme('DarkAmber')
sg.set_options(font=font)

layout = [
    [sg.Text("Stock Market Price Indicator", font=('Arial-Bold', 40))],
    [sg.Text("Enter Ticker Name:"), sg.Input(
        size=(40, 1), key="ticker", enable_events=True)],
    [sg.Text("Enter Target Price:"), sg.Input(
        size=(40, 1), key="target", enable_events=True)],
    [sg.Button("Enter", pad=((150, 50), (10, 0)), size=(10, 1)),
     sg.Button("Clear", pad=((50, 0), (10, 0)), size=(10, 1))],
    [sg.Text("Ticker: ", pad=((0, 0), (30, 0))),
     sg.Text(size=(50, 1), key="ticker_out", pad=((0, 0), (30, 0)))],
    [sg.Text("Target Price: $"), sg.Text(size=(50, 1), key="target_out")],
    [sg.Text("Current Price: $"), sg.Text(size=(15, 1), key="current_out")],
    [sg.Button('BUY',key='state',button_color = ("white", "green"), pad=((150, 150), (20, 0)), size=(30,1))]
]

# Creating the window
window = sg.Window("Stock Market Price Indicator", layout, size=(700, 400))

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# send a SMS
def send_sms(name, current_price,state):

    client = Client(account_sid, auth_token)
    client.messages.create(
        body=f"\n\n{name} has crossed {states[state]} ${TARGET} \n\nCurrent Price: ${current_price}",
        from_='', # Twilio's number that sends the SMS to your number
        to= PHONE_NUMBER
    )

    print("SMS sent!")


def send_email(name, current_price,state):
    subject = f"{name} target reached"
    body = f"{name} has crossed {states[state]} ${TARGET} \n\nCurrent Price: ${current_price}"

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


def check(state,values):
    global TARGET, TICKER
    info = requests.get(
        f"https://financialmodelingprep.com/api/v3/quote/{TICKER}?apikey={API_KEY}").json()

    # if ticker name is not valid
    if info == []:
        print("Ticker and/or API key is not valid!")
        window["ticker_out"].update("Ticker and/or API key is not valid!")
        window["target_out"].update("")
        return
    
    try:
        TARGET = float(values["target"])
    except:
        window["ticker_out"].update("")
        window["target_out"].update("Invalid target input! Make sure 1 decimal place")
        return

    name = info[0]['name']
    current_price = info[0]['price']
    window["ticker_out"].update(name)
    window["target_out"].update(values["target"])
    window["current_out"].update(current_price)
    print(f"Current {name} Price: ${current_price}")
    
    if state == "BUY":
        if current_price < TARGET:
            window["current_out"].update(current_price + " (Good time to buy!)")
            noti.notify(title="Stock Market Price Indicator",
                        message=f"{name} has crossed below desired target price!",
                        timeout=10)
            send_email(name, current_price,state)
            send_sms(name, current_price,state)
        return

    if state == "SELL":
        if current_price > TARGET:
            window["current_out"].update(current_price + " (Good time to sell!)")
            noti.notify(title="Stock Market Price Indicator",
                        message=f"{name} has crossed above desired target price!",
                        timeout=10)
            send_email(name, current_price, state)
            send_sms(name, current_price, state)
        return

def main():
    index = 0
    button_colors = {0: ('white','red'), 1: ('white','green')}
    button_texts = {0: "SELL", 1: "BUY"}
    state = "BUY"
    global TARGET, TICKER
    while True:
        # With free plan on Financial Modeling Prep website, can send a request call once every 6 minutes (250 calls/day)
        # Change timeout value accordingly
        event, values = window.read(timeout=120000)
        
        if event == sg.WIN_CLOSED:
            break

        elif event == "Clear":
            window["ticker"].update("")
            values["ticker"]= ""
            window["target"].update("")
            values["target"]= ""

        elif event == 'state':
            window['state'].update(button_color = button_colors[index %2])
            window['state'].Update(button_texts[index %2])
            state = button_texts[index %2]
            index += 1

        # restricts target input to integers/floats
        elif event == "target" and values["target"] and (values['target'][-1] not in ('0123456789.') or len(values['target']) > 11):
            window["target"].update(values['target'][: -1])

        # restrict ticker input to alphabet characters only
        elif event == "ticker" and values["ticker"] and values['ticker'][-1] not in ('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'):
            window["ticker"].update(values['ticker'][: -1])

        elif event == "Enter" or event == sg.TIMEOUT_KEY:
            TICKER = values["ticker"].upper()
            TARGET = values["target"]
            check(state,values)

    window.close()

if __name__ == "__main__":
    main()