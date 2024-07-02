import requests
from bs4 import BeautifulSoup

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
    # 如果 main-0-QuoteHeader-Proxy id 的 div 裡有 C($c-trend-down) 的 class
    # 表示狀態為下跌
    if soup.select('#main-0-QuoteHeader-Proxy')[0].select('.C($c-trend-down)')[0]:
        s = '-'
except:
    try:
        # 如果 main-0-QuoteHeader-Proxy id 的 div 裡有 C($c-trend-up) 的 class
        # 表示狀態為上漲
        if soup.select('#main-0-QuoteHeader-Proxy')[0].select('.C($c-trend-up)')[0]:
            s = '+'
    except:
        # 如果都沒有包含，表示平盤
        s = '-'

print(f'{title.get_text()} : {a.get_text()} ( {s}{b.get_text()} )')   # 印出結果