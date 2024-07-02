import requests
getA34=[]
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
print(my_n2)
#getA34.append('特別獎 :'+ns+'特獎: '+n1+'頭獎: '+my_n2)
