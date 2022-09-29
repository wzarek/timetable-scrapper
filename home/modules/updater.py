from os import remove
from urllib import request
from bs4 import BeautifulSoup
import requests
from lxml import etree

def updateSheet(link, x_path, filename):
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')
    dom = etree.HTML(str(soup))
    file = dom.xpath(x_path)[0]
    href = file.get('href')
    if file.text != filename:
        try:
            remove('sheets/' + filename)
        except Exception:
            print(Exception)
        with open('sheets/TEST-' + file.text + '.xls', 'wb') as created_file:
            res = requests.get(href)
            created_file.write(res.content)
        print(href)

updateSheet('https://wnoz.uni.opole.pl/plan-zajec-dietetyka-1/', '/html/body/div[1]/div[2]/div/article/div/div/div/div/div[2]/div/div/div/ul[1]/li[2]/strong/a', 'asd')