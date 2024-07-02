import requests
from bs4 import BeautifulSoup
import os
from linebot.models import *
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from flask import Flask, request, abort, render_template

app = Flask(__name__)
line_bot_api = LineBotApi('gThtNtgyKmz49kcApR6Gc/0sGvpbtPXlfJC85+p6bJ2ugBb4w0UDjj/HEpVUARLIcoLOyPHXY3VRrSwSgg6qKcgKIPZzxiAGe9o4sEoDCpNfRNlnTapgOPp3ww3Ps3K0fDOlFUddxfAaMcmm4a9lcQdB04t89/1O/w1cDnyilFU=')
line_handler = WebhookHandler('acde6b0819d2d8b86f8e932c394e7da9')

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



@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text

    if "1" in msg:        
        url = 'https://tw.stock.yahoo.com/quote/2330'    # 台積電 Yahoo 股市網址
        web = requests.get(url)
        soup = BeautifulSoup(web.text, "html.parser")
        title = soup.find('h1')
        #a = soup.select('.Fz(32px)')[0] 
        #b = soup.select('.Fz(20px)')[0] 
        a = soup.select('.Fz\(32px\)')[0]     # 找到第一個 class 為 Fz(32px) 的內容，如果出現錯誤，可以使用 .Fz\(32px\) 轉義
        b = soup.select('.Fz\(20px\)')[0]     # 找到第一個 class 為 Fz(20px) 的內容，如果出現錯誤，可以使用 .Fz\(20px\) 轉義
        s = ''
        try:
            if soup.select('#main-0-QuoteHeader-Proxy')[0].select('.C($c-trend-down)')[0]:
                s = '-'
        except:
            try:
                if soup.select('#main-0-QuoteHeader-Proxy')[0].select('.C($c-trend-up)')[0]:
                    s = '+'
            except:
                s = '-'
        print(f'{title.get_text()} : {a.get_text()} ( {s}{b.get_text()} )')   # 印出結果
        mya=title.get_text()+a.get_text()+b.get_text()
        line_bot_api.reply_message(event.reply_token, [TextSendMessage(text=title.get_text()), TextSendMessage(text=a.get_text()),TextSendMessage(text=b.get_text())])
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="輸入1")
        )


if __name__ == "__main__":
    app.run()