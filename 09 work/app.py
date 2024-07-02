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
        url = 'https://invoice.etax.nat.gov.tw/index.html'
        web = requests.get(url)
        web.encoding='utf-8'        
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(web.text, "html.parser")
        td = soup.select('.container-fluid')[0].select('.etw-tbiggest')
        ns = td[0].getText()  # 特別獎
        n1 = td[1].getText()  # 特獎
        # 頭獎，因為存入串列會出現 /n 換行符，使用 [-8:] 取出最後八碼
        n2 = [td[2].getText()[-8:], td[3].getText()[-8:], td[4].getText()[-8:]]
        my_n2 = ",".join(str(element) for element in n2)
        line_bot_api.reply_message(event.reply_token, [TextSendMessage(text='特別獎'+ns),TextSendMessage(text='特獎'+n1),TextSendMessage(text='頭獎'+my_n2)])
    
    elif "2" in msg:
        url = 'https://invoice.etax.nat.gov.tw/lastNumber.html'
        web = requests.get(url)
        web.encoding='utf-8'        
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(web.text, "html.parser")
        td = soup.select('.container-fluid')[0].select('.etw-tbiggest')
        n3 = td[0].getText()  # 特別獎
        n4 = td[1].getText()  # 特獎
        # 頭獎，因為存入串列會出現 /n 換行符，使用 [-8:] 取出最後八碼
        n5 = [td[2].getText()[-8:], td[3].getText()[-8:], td[4].getText()[-8:]]
        my_n5 = ",".join(str(element) for element in n5)
        line_bot_api.reply_message(event.reply_token, [TextSendMessage(text='特別獎'+n3),TextSendMessage(text='特獎'+n4),TextSendMessage(text='頭獎'+my_n5)])    
    
    
    else:
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text="輸入1 3.4月中獎發票"),TextMessage(text="輸入2 1.2月中獎發票")]
        )


if __name__ == "__main__":
    app.run()