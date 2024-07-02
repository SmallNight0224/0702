import os
from bs4 import BeautifulSoup
from linebot.models import *
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from flask import Flask, request, abort, render_template
import requests

app = Flask(__name__)

line_bot_api = LineBotApi('LINE_CHANNEL_ACCESS_TOKEN')
line_handler = WebhookHandler('LINE_CHANNEL_SECRET')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

get34=[]
get12=[]
def get34():    
    url = 'https://invoice.etax.nat.gov.tw/index.html'
    web = requests.get(url)
    web.encoding='utf-8'    
    soup = BeautifulSoup(web.text, "html.parser")
    td = soup.select('.container-fluid')[0].select('.etw-tbiggest')
    n0 = td[0].getText()  # 特別獎
    n1 = td[1].getText()  # 特獎
    # 頭獎，因為存入串列會出現 /n 換行符，使用 [-8:] 取出最後八碼
    n2 = [td[2].getText()[-8:], td[3].getText()[-8:], td[4].getText()[-8:]]
    #print(ns)
    #print(n1)
    #print(n2)
    my_n2 = ",".join(str(element) for element in n2)


def get12():    
    url = 'https://invoice.etax.nat.gov.tw/lastNumber.html'
    web = requests.get(url)
    web.encoding='utf-8'   
    soup = BeautifulSoup(web.text, "html.parser")
    td = soup.select('.container-fluid')[0].select('.etw-tbiggest')
    n3 = td[0].getText()  # 特別獎
    n4 = td[1].getText()  # 特獎
    # 頭獎，因為存入串列會出現 /n 換行符，使用 [-8:] 取出最後八碼
    n5 = [td[2].getText()[-8:], td[3].getText()[-8:], td[4].getText()[-8:]]
    #print(ns)
    #print(n1)
    #print(n2)
    my_n5 = ",".join(str(element) for element in n5)
    



# handle text message
@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    
    if "1" in msg:
        get34()             
        line_bot_api.reply_message(event.reply_token, [TextSendMessage(text=n0),TextSendMessage(text=n1),TextSendMessage(text=my_n2)])
    elif "2" in msg:
        get12()        
        line_bot_api.reply_message(event.reply_token, [TextSendMessage(text=n3),TextSendMessage(text=n4),TextSendMessage(text=my_n5)])
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="輸入1 2")
        )


if __name__ == "__main__":
    app.run()