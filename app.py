from flask import Flask,request
from twilio.rest import Client
from marketstack import get_stock_price
import os

app = Flask(__name__)

ACCOUNT_ID = os.environ.get('TWILIO_ACCOUNT')
TWILIO_TOKEN = os.environ.get('TWILIO_TOKEN')

client = Client(ACCOUNT_ID,TWILIO_TOKEN)
TWILIO_NUMBER = 'whatsapp:+14155238886'
def send_msg(msg,recipient):
    client.messages.create(
        from_=TWILIO_NUMBER,
        body=msg,
        to=recipient
    )

def process_msg(msg):
    res = ""
    if msg == "hi":
        res = "Welcome to the stock market bot"
        res = "Type sym:<stock_symbol> to ge the price of the stock"
    elif 'sym:' in msg:
        data = msg.split(":")
        stock_symbol = data[1]
        stock_price = get_stock_price(stock_symbol)
        last_price = stock_price['last_price']
        last_price_str = str(last_price)
        res = "the stock price of " + stock_symbol + " is $" + last_price_str
    else:
        res = "please type hi to get started"
    return res

@app.route('/webhook',methods=["POST"])
def webhook():
    f = request.form
    msg = f['Body']
    sender = f['From']
    res = process_msg(msg)
    send_msg(res,sender)

    return "OK",200

    app.run(port=5000)