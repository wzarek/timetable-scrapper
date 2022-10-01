from genericpath import isfile
from os import remove, rename
from urllib import request
from bs4 import BeautifulSoup
import requests
from lxml import etree

rootEndpoint = 'http://localhost:8000'

def getSheetsToUpdate():
    try:
        apiEndpoint = f'{rootEndpoint}/api/get-fields'
        response = requests.get(apiEndpoint)
        fieldsJSON = response.json()
        print('Succesfully got sheets to update')
    except:
        print('Could not get sheets to update')
        return
    for field in fieldsJSON['fields']:
        try:
            updateSheet(field['link'], field['xpath'], field['filename'], field['slug'])
        except Exception as e:
            print(e + ' Could not update ' + field['slug'])
            return

def updateSheet(link, x_path, filename, slug):
    try:
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')
        dom = etree.HTML(str(soup))
        file = dom.xpath(x_path)[0]
        href = file.get('href')
    except Exception as e:
        print('Could not get the response from link', e)
        return
    if f'{file.text}.xls' != filename or not isfile(f'/home/wzarek/sheets/{filename}'):
        try:
            rename(f'/home/wzarek/sheets/{filename}', f'/home/wzarek/sheets_archive/{filename}')
        except Exception as e:
            print('Could not archive: ' + filename + ' ' + e)
        try:
            with open('/home/wzarek/sheets/' + file.text + '.xls', 'wb') as created_file:
                res = requests.get(href)
                created_file.write(res.content)
        except Exception as e:
            print('Could not create new file: ' + file.text + ' ' + e)
        try:
            sendUpdatedSheet(slug, f'{file.text}.xls', href)
        except:
            print('Could not update the sheet: ' + file.text)

def sendUpdatedSheet(slug, file, link):
    apiEndpoint = f'{rootEndpoint}/api/change-field?slug={slug}&file={file}&link={link}'
    response = requests.get(apiEndpoint)
    print(response.json())

getSheetsToUpdate()
# updateSheet('https://wnoz.uni.opole.pl/plan-zajec-dietetyka-1/', '/html/body/div[1]/div[2]/div/article/div/div/div/div/div[2]/div/div/div/ul[1]/li[2]/strong/a', 'asd')