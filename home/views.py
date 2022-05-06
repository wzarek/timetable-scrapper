from os import read
from django.shortcuts import render
from django.views.generic import TemplateView
import xlrd
from datetime import date, datetime, time, timedelta
from icalendar import Calendar, Event
from tabula import read_pdf
import numpy as np

# Create your views here.

def genIcal(arr, name):
    # X-WR-CALNAME:katanaforumps2@gmail.com
    # X-WR-TIMEZONE:Europe/Warsaw
    cal = Calendar()
    cal.add('X-WR-CALNAME', 'Plan zajec')
    cal.add('X-WR-TIMEZONE', 'Europe/Warsaw')
    for row in arr:
        event = Event()

        event.add('summary', row['przedmiot'])
        date = datetime.strptime(row['data'],"%d-%m-%Y").date()
        time = datetime.strptime(row['od'],"%H:%M").time()
        combined = datetime.combine(date, time)
        event.add('dtstart', combined)
        time = datetime.strptime(row['do'],"%H:%M").time()
        combined = datetime.combine(date, time)
        event.add('dtend', combined)
        desc = row['stopien'] + " " + row['imie'] + " " + row['nazwisko']
        event.add('description', desc)
        if 'sala' in row.keys():
            event.add('location', row['sala'].replace('.0', ''))
        cal.add_component(event)

    f = open('icals/' + name, 'wb')
    f.write(cal.to_ical())
    f.close()

def readPDF():
    df = read_pdf("pdfs/plan1.pdf",multiple_tables=True, pages=1)
    # print(df[0])
    dfDict = df[0].to_dict()
    print(dfDict)
    rows = df[0]['Przedmiot'].keys()[-1]
    print(rows)
    arr = []
    print(df[1].to_dict())
    # print(df[0].keys())
    if df[0].keys()[0] != 'Czas od':
        data = datetime.strptime(df[0][df[0].keys()[0]][0].split(" ")[2], "%Y-%m-%d").strftime("%d-%m-%Y")
        i=1
        j=0
        while i != rows+1:
            arr.append({})
            if str(df[0]['Sala'][i]) == 'nan' and str(df[0]['Przedmiot'][i+1]) == 'nan':
                arr[j]['przedmiot'] = str(df[0]['Przedmiot'][i]).replace('\r', ' ') + ' ' + str(df[0]['Przedmiot'][i+2]).replace('\r', ' ')
                if str(df[0]['Sala'][i+1]) != 'nan':
                    arr[j]['sala'] = str(df[0]['Sala'][i+1])
                rows = rows
                i = i+3
            else:
                arr[j]['przedmiot'] = str(df[0]['Przedmiot'][i]).replace('\r', ' ')
                if str(df[0]['Sala'][i]) != 'nan':
                    arr[j]['sala'] = str(df[0]['Sala'][i])
                arr[j]['od'] = str(df[0][df[0].keys()[0]][i]).split(" ")[0]
                arr[j]['do'] = str(df[0][df[0].keys()[0]][i]).split(" ")[1]
                i = i+1
            arr[j]['data'] = data
            j = j+1

    # data = datetime.strptime(dfDict['Czas od'][0].split(" ")[2], "%Y-%m-%d").strftime("%d-%m-%Y")
    # for i in range(rows):
    #     arr[i]['od'] = df[0]['Czas od'][i+1]
    #     arr[i]['do'] = df[0]['Czas do'][i+1]
    #     arr[i]['przedmiot'] = df[0]['Przedmiot'][i+1].replace('\r', ' ')
    #     prowadzacy = df[0]['Prowadzący'][i+1].split(" ")
    #     arr[i]['stopien'] = prowadzacy[0]
    #     arr[i]['imie'] = prowadzacy[1]
    #     arr[i]['nazwisko'] = prowadzacy[2]
    #     arr[i]['data'] = data
    # print(arr)
    # genIcal(arr, 'julka.ics')
    return arr

def uopolski(week):
    loc = ("sheets/plan-wik.xls")
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)
    sheet.cell_value(0, 0)

    labels =  []
    table = [{} for _ in range(0, sheet.nrows)]

    for i in range(sheet.ncols):
        labels.append(sheet.cell_value(3,i))

    labels[0] = 'data'
    labels[2] = 'od'
    labels[3] = 'do'
    labels[5] = 'rodzaj'
    labels[6] = 'stopien'
    labels[7] = 'imie'
    labels[10] = 'kierunek'
    for i in range(4, sheet.nrows):
        h1e = xlrd.xldate_as_tuple(sheet.cell_value(i, 2), wb.datemode)
        h2e = xlrd.xldate_as_tuple(sheet.cell_value(i, 3), wb.datemode)
        #print(h1e)
        h1 = time(*h1e[-3:])
        h2 = time(*h2e[-3:])
        table[i-4]['dlugosc'] = int(timedelta(hours=h2.hour-h1.hour, minutes=h2.minute-h1.minute).total_seconds() / (60*15))
        #print(table[i-4]['dlugosc'])
        for j in range(0, sheet.ncols):
            if j==0:
                cellDate = xlrd.xldate_as_tuple(sheet.cell_value(i, j), wb.datemode)
                table[i-4][labels[j]] = date(*cellDate[:-3]).strftime("%d-%m-%Y")
                # table[i-4].append(date(*cellDate[:-3]))
            elif j==2 or j==3:
                cellDate = xlrd.xldate_as_tuple(sheet.cell_value(i, j), wb.datemode)
                table[i-4][labels[j]] = time(*cellDate[-3:]).strftime("%H:%M")
                # table[i-4].append(time(*cellDate[-3:]))
            else:
                # table[i-4].append(sheet.cell_value(i, j))
                table[i-4][labels[j]] = str(sheet.cell_value(i, j))

    # print(labels)
    # print(table)
    filtered = []
    grupy = ['II', 3, 'cały rok']

    for i in range(len(table)):
        if table[i]:
            if type(table[i]['grupa']) == float:
                table[i]['grupa'] = int(table[i]['grupa'])
            if type(table[i]['sala']) == float:
                table[i]['sala'] = int(table[i]['sala'])
            if table[i]['grupa'] in grupy:
                filtered.append(table[i])
            elif table[i]['grupa'][:1].strip().isdigit():
                table[i]['grupa'] == int(table[i]['grupa'][:1])
                if int(table[i]['grupa'][:1]) in grupy:
                    filtered.append(table[i])

    # print(filtered[2])

    #today = datetime.today()

    weekArr = {}
    days = ['poniedziałek', 'wtorek', 'środa', 'czwartek', 'piątek', 'sobota', 'niedziela']
    # today = datetime.now().strftime("%d-%m-%Y")
    today = datetime.now()
    firstWeekDay = datetime.now()
    todaysWeekday = datetime.today().weekday()
    # print(today - timedelta(days = 2))
    if todaysWeekday > 0:
        while(firstWeekDay.weekday() != 0):
            firstWeekDay = firstWeekDay - timedelta(days=1)
    firstWeekDay = firstWeekDay + timedelta(days = (week*7))
    for i in range(7):
        weekArr[days[i]] = (firstWeekDay + timedelta(days = i)).strftime("%d-%m-%Y")

    # print(weekArr)
    today = today.strftime("%d-%m-%Y")

    starting = 0
    ending = 6


    for i in range(len(filtered)):
        # print(filtered[i]['data'])
        if filtered[i]['data'] in weekArr.values():
            starting = i
            break

    start_hour = '99:99'
    end_hour = '00:00'
    hours = []

    for i in range(starting, len(filtered)-1):
        if (int(filtered[i]['data'][:2]) > int(weekArr[days[6]][:2]) and int(filtered[i]['data'][3:5]) == int(weekArr[days[6]][3:5])) or (int(filtered[i]['data'][3:5]) > int(weekArr[days[6]][3:5])):
            break
        else:
            ending = i
            if int(filtered[i]['od'][:2]) < int(start_hour[:2]):
                start_hour = filtered[i]['od']
            if int(filtered[i]['do'][:2]) > int(end_hour[:2]):
                end_hour = filtered[i]['do']

    # print(filtered[ending])
    # print(starting, ending)
    if start_hour != '99:99':
        start_hour = datetime.strptime(start_hour,"%H:%M")
        end_hour = datetime.strptime(end_hour,"%H:%M")
        # print(datetime.strptime(start_hour,"%H:%M"))
        while start_hour != end_hour:
            hours.append(start_hour.strftime("%H:%M"))
            start_hour = start_hour + timedelta(minutes = 15)
        hours.append(start_hour.strftime("%H:%M"))
    # print(starting, ending)

    filteredWeekdays = {}
    for i in range(5):
        #print(weekArr[days[i]])
        filteredWeekdays[days[i]] = []
        for j in range(starting,ending+1):
            #print(filtered[j]['data'])
            if filtered[j]['data'] == weekArr[days[i]]:
                filteredWeekdays[days[i]].append(filtered[j])
                #print('masno')

    for i in range(5):
        # print(days[i])
        for j in range(len(filteredWeekdays[days[i]])):
            # print(filteredWeekdays[days[i]][j])
            if j == 0:
                diff = int(((datetime.strptime(filteredWeekdays[days[i]][j]['od'],"%H:%M") - datetime.strptime(hours[0],"%H:%M")).total_seconds()) / (60*15))
                filteredWeekdays[days[i]][j]['diff'] = diff
            else:
                diff = int(((datetime.strptime(filteredWeekdays[days[i]][j]['od'],"%H:%M") - datetime.strptime(filteredWeekdays[days[i]][j-1]['do'],"%H:%M")).total_seconds()) / (60*15))
                filteredWeekdays[days[i]][j]['diff'] = diff

    # print(filtered[2])
    #print(filteredWeekdays)
    weekArr.pop(days[5])
    weekArr.pop(days[6])
    # print(filtered[5])
    # print(filteredWeekdays)
    iCalPath = 'plan.ics'
    genIcal(filtered, iCalPath)
    context = {'title': 'plan v0.1', 'today' : today, 'weekday': days[todaysWeekday], 'weekArr': weekArr, 'planFiltered': filteredWeekdays, 'wNum': week, 'hours': hours, 'filePath': 'icals/' + iCalPath}
    return context

class index(TemplateView):
    template = 'home.html'
    #readPDF()

    def get(self, request):
        context = uopolski(0)
        return render(request, self.template, context)

    def post(self, request):
        try:
            week = int(request.POST['w'])
        except:
            week = 0
        context = uopolski(week)
        return render(request, self.template, context)

        # sprawdzenie czy zmienila sie data w porownaniu do poprzedniej, jak tak to przeskakujemy do nastepnej
        # w kazdym dniu bloki co 1h - position relative, w nich obiekt np godzina 9:30 przypinamy do 3 bloku(bo zaczynamy od 7) i dajemy top 50%
