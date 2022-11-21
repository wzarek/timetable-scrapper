from genericpath import isfile
from os import remove, rename
from urllib import request
from bs4 import BeautifulSoup
import requests
from lxml import etree
from mailer.emailsender import EmailSender

rootEndpoint = 'https://timetable.wzarek.me'
rootPath = '/home/wzarek/media'

changed_sheets = []

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
        print('Proccessing sheet for: ' + field['slug'])
        try:
            updateSheet(field['link'], field['xpath'], field['filename'], field['slug'])
        except Exception as e:
            print(str(e) + ' Could not update ' + field['slug'])
            return
    EmailSender(['kontakt.wzarek@gmail.com']).sendReport(changed_sheets)

def updateSheet(link, x_path, filename, slug):
    try:
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')
        dom = etree.HTML(str(soup))
        file = dom.xpath(x_path)[0]
        href = file.get('href')
    except Exception as e:
        print('Could not get the response from link', str(e))
        return
    if f'{file.text}.xls' != filename or not isfile(f'{rootPath}/sheets/{filename}'):
        try:
            if isfile(f'{rootPath}/sheets/{filename}'):
                rename(f'{rootPath}/sheets/{filename}', f'{rootPath}/sheets_archive/{filename}')
        except Exception as e:
            print('Could not archive: ' + filename + ' ' + str(e))
        try:
            with open(f'{rootPath}/sheets/{file.text}.xls', 'wb') as created_file:
                res = requests.get(href)
                created_file.write(res.content)
        except Exception as e:
            print('Could not create new file: ' + file.text + ' ' + str(e))
        try:
            sendUpdatedSheet(slug, f'{file.text}.xls', href)
        except:
            print('Could not update the sheet: ' + file.text)
    else:
        print('Sheet did not change')

def sendUpdatedSheet(slug, file, link):
    apiEndpoint = f'{rootEndpoint}/api/change-field?slug={slug}&file={file}&link={link}'
    response = requests.get(apiEndpoint)
    changed_sheets.append(slug)
    print(response.json())

getSheetsToUpdate()