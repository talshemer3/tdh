
import http.cookiejar
import urllib.request
from bs4 import BeautifulSoup




url = "https://main.knesset.gov.il/pages/default.aspx"
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
r = opener.open(url)
link = 'https://main.knesset.gov.il/About/History/Pages/KnessetHistory.aspx?kns=19'
content = opener.open(link).read()
soup = BeautifulSoup(content, "lxml")
print(soup.text)
# for comments in soup.findAll(text=lambda text:isinstance(text, Comment)):
#     print(comments)
#     comments.extract()


# print(soup.find('div',{'id':"KnessetHistoryMainContainerDiv"}))
# print(soup.find('div',{'class':"HistElectDetails"}))
# print(soup.find('h3'))




