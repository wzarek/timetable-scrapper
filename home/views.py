import array
from dataclasses import field, fields
from pipes import Template
from sys import argv
from tkinter import E
from tokenize import group
from turtle import update
from xmlrpc.client import DateTime
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
import xlrd
from datetime import date, datetime, time, timedelta
from icalendar import Calendar, Event
from .models import Field
from django.http import Http404, JsonResponse


GROUPS_DEFAULT = {'caly rok', 'cały rok', 'caly-rok', 'cały-rok', 'całay rok'}

def floatToString(number : float):
    return str(int(number))

def updateGroups(slug : str):
    print(f'Group updating started for {slug}')

    field_object : Field = Field.objects.get(slug = slug)

    location : str = (field_object.file.path)
    workbook = xlrd.open_workbook(location)
    sheet = workbook.sheet_by_index(0)
    sheet.cell_value(0, 0)

    groups : set = set()

    for i in range(4, sheet.nrows):
        try:
            try:
                groups.add(floatToString(sheet.cell_value(i, 11)))
            except:
                groups.add(str(sheet.cell_value(i, 11)).strip())
        except:
            break

    groups_sorted : set = sorted(groups)
    groups_sorted = [group for group in groups_sorted if group not in GROUPS_DEFAULT]
    groups_string : str = ";".join(groups_sorted)
    if field_object.groups != groups_string:
        field_object.groups = groups_string
        field_object.save()
        print(f'Groups updated: [{groups_string}]')
    else:
        print('Groups are up to date')


def genIcal(arr : dict, name : str):
    # X-WR-CALNAME:katanaforumps2@gmail.com
    # X-WR-TIMEZONE:Europe/Warsaw
    cal = Calendar()
    cal.add('X-WR-CALNAME', 'Plan zajec')
    cal.add('X-WR-TIMEZONE', 'Europe/Warsaw')
    for row in arr:
        event = Event()

        event.add('summary', row['przedmiot'])
        date : datetime = datetime.strptime(row['data'],"%d-%m-%Y").date()
        try:
            time : datetime = datetime.strptime(row['od'],"%H:%M").time()
        except:
            time : datetime = datetime.strptime("06:00", "%H:%M").time()
        combined : datetime = datetime.combine(date, time)
        event.add('dtstart', combined)
        try:
            time : datetime = datetime.strptime(row['do'],"%H:%M").time()
        except:
            time : datetime = datetime.strptime("22:00", "%H:%M").time()
        combined : datetime = datetime.combine(date, time)
        event.add('dtend', combined)
        desc : str = row['prowadzacy']
        if row['od'] == 'brak daty':
            desc += ' WAZNE: godzina rozpoczęcia nieznana'
        if row['do'] == 'brak daty':
            desc += ' WAZNE: godzina zakończenia nieznana'
        event.add('description', desc)
        if 'sala' in row.keys():
            event.add('location', row['sala'].replace('.0', ''))
        cal.add_component(event)

    f = open('icals/' + name, 'wb')
    f.write(cal.to_ical())
    f.close()



def uopolski(fieldSlug : str, week : int, groups_request : array):
    field_object : Field = Field.objects.get(slug = fieldSlug)
    fieldType = field_object.type

    loc : str = (field_object.file.path)
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)
    sheet.cell_value(0, 0)

    labels : array =  []
    table : array = [{} for _ in range(0, sheet.nrows)]

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
        try:
            h1e = xlrd.xldate_as_tuple(sheet.cell_value(i, 2), wb.datemode)
            h1 = time(*h1e[-3:])
        except:
            h1 = 'brak daty'

        try:
            h2e = xlrd.xldate_as_tuple(sheet.cell_value(i, 3), wb.datemode)
            h2 = time(*h2e[-3:])
        except:
            h2 = 'brak daty'

        if h1 == 'brak daty' or h2 =='brak daty':
            table[i-4]['dlugosc'] = 1
        else:
            table[i-4]['dlugosc'] = int(timedelta(hours=h2.hour-h1.hour, minutes=h2.minute-h1.minute).total_seconds() / (60*15))
        
        for j in range(0, sheet.ncols):
            if j==0:
                cellDate = xlrd.xldate_as_tuple(sheet.cell_value(i, j), wb.datemode)
                table[i-4][labels[j]] = date(*cellDate[:-3]).strftime("%d-%m-%Y")
            elif j==2 or j==3:
                try:
                    cellDate = xlrd.xldate_as_tuple(sheet.cell_value(i, j), wb.datemode)
                    table[i-4][labels[j]] = time(*cellDate[-3:]).strftime("%H:%M")
                except:
                    table[i-4][labels[j]] = 'brak daty'
            else:
                table[i-4][labels[j]] = str(sheet.cell_value(i, j)).strip()

    filtered = []

    groups = groups_request.copy()
    if len(groups_request) == 0:
        groups = ['II', 3, 'cały rok']
    else:
        for group in GROUPS_DEFAULT:
            groups.append(group)

    for i in range(len(table)):
        if table[i]:
            if type(table[i]['grupa']) == float:
                table[i]['grupa'] = int(table[i]['grupa'])
            if table[i]['sala'][:-2].strip().isdigit():
                table[i]['sala'] = str(table[i]['sala'])[:-2]
            if str(table[i]['grupa']).strip() in groups:
                filtered.append(table[i])
            elif str(table[i]['grupa'])[:1].strip().isdigit():
                table[i]['grupa'] = int(table[i]['grupa'][:1])
                if str(table[i]['grupa'])[:1] in groups:
                    table[i]['grupa'] = str(table[i]['grupa'])[:1]
                    filtered.append(table[i])
    weekArr = {}
    days = ['poniedziałek', 'wtorek', 'środa', 'czwartek', 'piątek', 'sobota', 'niedziela']
    today = datetime.now()
    firstWeekDay = datetime.now()
    todaysWeekday = datetime.today().weekday()
    if todaysWeekday > 0:
        while(firstWeekDay.weekday() != 0):
            firstWeekDay = firstWeekDay - timedelta(days=1)
    firstWeekDay = firstWeekDay + timedelta(days = (week*7))
    for i in range(7):
        weekArr[days[i]] = (firstWeekDay + timedelta(days = i)).strftime("%d-%m-%Y")

    today = today.strftime("%d-%m-%Y")

    starting = 0
    ending = 6

    for i in range(len(filtered)):
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

            if filtered[i]['od'] == 'brak daty' or filtered[i]['do'] == 'brak daty':
                continue

            if int(filtered[i]['od'][:2]) < int(start_hour[:2]):
                start_hour = filtered[i]['od']
            if int(filtered[i]['do'][:2]) > int(end_hour[:2]):
                end_hour = filtered[i]['do']

    if start_hour != '99:99':
        start_hour = datetime.strptime(start_hour,"%H:%M")
        end_hour = datetime.strptime(end_hour,"%H:%M")
        while start_hour != end_hour:
            hours.append(start_hour.strftime("%H:%M"))
            start_hour = start_hour + timedelta(minutes = 15)
        hours.append(start_hour.strftime("%H:%M"))

    filteredWeekdays = {}
    if fieldType == 'niestacjonarne':
        for i in range(5,7):
            filteredWeekdays[days[i]] = []
            for j in range(starting,ending+1):
                if filtered[j]['data'] == weekArr[days[i]]:
                    filteredWeekdays[days[i]].append(filtered[j])

        for i in range(5,7):
            for j in range(len(filteredWeekdays[days[i]])):
                if j == 0:
                    try:
                        diff = int(((datetime.strptime(filteredWeekdays[days[i]][j]['od'],"%H:%M") - datetime.strptime(hours[0],"%H:%M")).total_seconds()) / (60*15))
                    except:
                        diff = 1
                    filteredWeekdays[days[i]][j]['diff'] = diff
                else:
                    try:
                        diff = int(((datetime.strptime(filteredWeekdays[days[i]][j]['od'],"%H:%M") - datetime.strptime(filteredWeekdays[days[i]][j-1]['do'],"%H:%M")).total_seconds()) / (60*15))
                    except:
                        diff = 1
                    filteredWeekdays[days[i]][j]['diff'] = diff
    else:
        for i in range(5):
            filteredWeekdays[days[i]] = []
            for j in range(starting,ending+1):
                if filtered[j]['data'] == weekArr[days[i]]:
                    filteredWeekdays[days[i]].append(filtered[j])

        for i in range(5):
            for j in range(len(filteredWeekdays[days[i]])):
                if j == 0:
                    try:
                        diff = int(((datetime.strptime(filteredWeekdays[days[i]][j]['od'],"%H:%M") - datetime.strptime(hours[0],"%H:%M")).total_seconds()) / (60*15))
                    except:
                        diff = 1
                    filteredWeekdays[days[i]][j]['diff'] = diff
                else:
                    try:
                        diff = int(((datetime.strptime(filteredWeekdays[days[i]][j]['od'],"%H:%M") - datetime.strptime(filteredWeekdays[days[i]][j-1]['do'],"%H:%M")).total_seconds()) / (60*15))
                    except:
                        diff = 1
                    filteredWeekdays[days[i]][j]['diff'] = diff
    
    for row in filtered:
        row['prowadzacy'] = row['stopien'] + " " + row['imie'] + " " + row['nazwisko']
    
    if fieldType == 'niestacjonarne':
        weekArr.pop(days[0])
        weekArr.pop(days[1])
        weekArr.pop(days[2])
        weekArr.pop(days[3])
        weekArr.pop(days[4])
    else:
        weekArr.pop(days[5])
        weekArr.pop(days[6])
    iCalPath = f'{field_object.slug}-grupy-{"-".join(groups[:-1])}.ics'
    genIcal(filtered, iCalPath)

    context = {'title': f'Timetable scrapper | {field_object.name}, {field_object.year} rok, {field_object.degree}, {field_object.type} gr.: {" ".join(groups[:-1])}', 'today' : today, 'weekday': days[todaysWeekday], 'weekArr': weekArr, 'planFiltered': filteredWeekdays, 'wNum': week, 'hours': hours, 'filePath': 'icals/' + iCalPath, 'groups': groups_request, 'field': field_object}
    return context

# VIEWS -----------

class timetable(TemplateView):
    template = 'timetable.html'

    def get(self, request):
        incrementViewcount = False

        try:
            week = int(request.GET['week'])
        except:
            week = 0

        if request.GET.getlist('groups'):
            groups = request.GET.getlist('groups')
            request.session['groups'] = groups
            request.session.modified = True
        else:
            groups = request.session.get('groups', [])

        if request.GET.get('field'):
            fieldSlug = request.GET['field']
            request.session['fieldSlug'] = fieldSlug
            incrementViewcount = True
        else:
            fieldSlug = request.session.get('fieldSlug', 'dietetyka-lic-1rok-stac')

        #try:
        field = Field.objects.get(slug = fieldSlug)
        note = f'{field.name}, {field.year} rok, {field.degree}, {field.type} - {field.university.name}'
        context = uopolski(fieldSlug, week, groups)

        # if incrementViewcount:
        #     if field.visitcount == None:
        #         field.visitcount = 1
        #     else:
        #         field.visitcount = field.visitcount + 1
        #     field.save()
        # except:
        #     pass
      
        context['note'] = note
        context['headertitle'] = f'dzisiaj jest  {context["weekday"]}, {context["today"]}'
        return render(request, self.template, context)

    def post(self, request):
        groups = []
        fieldSlug = 'dietetyka-lic-1rok-stac'
        note = f'(Przykładowy) Dietetyka, 1 rok, licencjackie, stacjonarne - Uniwersytet Opolski'
        context = uopolski(fieldSlug, 0, groups)
        context['note'] = note
        context['headertitle'] = f'dzisiaj jest  {context["weekday"]}, {context["today"]}'
        return render(request, self.template, context)

        # sprawdzenie czy zmienila sie data w porownaniu do poprzedniej, jak tak to przeskakujemy do nastepnej
        # w kazdym dniu bloki co 1h - position relative, w nich obiekt np godzina 9:30 przypinamy do 3 bloku(bo zaczynamy od 7) i dajemy top 50%
        
class home(TemplateView):
    template = 'home.html'
    context = {'title': 'Timetable scrapper | home', 'headertitle': 'narzędzie do upraszczania planu zajęć'}

    # ---- TEST
    # fields = Field.objects.filter(parent__isnull = False).values()
    # for field in fields:
    #     updateGroups(field['slug'])
    # ---- TEST


    def get(self, request): 
        return render(request, self.template, self.context)

    def post(self, request):
        return render(request, self.template, self.context)

class chooseField(TemplateView):
    template = 'fieldchooser.html'
    parentFields = Field.objects.filter(parent__isnull = True).values()
    fieldsFiltered : dict = {}
    for parent in parentFields:
        fieldsFiltered[parent['name']] = Field.objects.filter(parent__slug = parent['slug']).values()

    context = {'title': 'Timetable scrapper | wybierz kierunek', 'headertitle': 'wybierz odpowiadający plan', 'fieldsFiltered': fieldsFiltered}

    def get(self, request):
        return render(request, self.template, self.context)
    def post(self, request):
        return render(request, self.template, self.context)

class chooseGroup(TemplateView):
    template = 'groupchooser.html'
    context = {'title': 'Timetable scrapper | wybierz kierunek', 'headertitle': 'wybierz odpowiadający plan'}

    def get(self, request):
        try:
            field = request.GET['field']
        except:
            raise Http404

        field : Field = Field.objects.get(slug = field)
        groups : array = field.groups.split(";")

        if not field.groups:
            response = redirect('timetable')
            response['Location'] += f'?field={field.slug}&groups=brak%20grup'
            return response

        self.context['groups'] = groups
        self.context['field'] = field
        return render(request, self.template, self.context)
    def post(self, request):
        raise Http404

class tutorial(TemplateView):
    template = 'tutorial.html'
    context = {'title': 'Timetable scrapper | poradnik', 'headertitle': 'jak zacząć?'}

    def get(self, request):
        return render(request, self.template, self.context)
    def post(self, request):
        return render(request, self.template, self.context)

class about(TemplateView):
    template = 'about.html'
    context = {'title': 'Timetable scrapper | o nas'}

    def get(self, request):
        return render(request, self.template, self.context)
    def post(self, request):
        return render(request, self.template, self.context)

# ERROR CODES -----------

class error400(TemplateView):
    template = 'error.html'
    context = {'error': '400 Bad Request', 'errordesc': 'Podany URL nie został odnaleziony na serwerze.'}

    def get(self, request):
        return render(request, self.template, self.context)
    def post(self, request):
        return render(request, self.template, self.context)

class error403(TemplateView):
    template = 'error.html'
    context = {'error': '403 Forbidden', 'errordesc': 'Brak uprawnień do przeglądania podanego adresu.'}

    def get(self, request):
        return render(request, self.template, self.context)
    def post(self, request):
        return render(request, self.template, self.context)

class error404(TemplateView):
    template = 'error.html'
    context = {'error': '404 Not Found', 'errordesc': 'Podana strona nie została odnaleziona. Sprawdź podany link bądź wróć do formularza i uzupełnij go ponownie.'}

    def get(self, request):
        return render(request, self.template, self.context)
    def post(self, request):
        return render(request, self.template, self.context)

# API -----------

class getFieldsToUpdate(TemplateView):

    def get(self, request):
        timestamp = datetime.now()
        fields = Field.objects.filter(parent__isnull = False).values()
        fieldsToSend = []
        for field in fields:
            fieldsToSend.append({'slug': field['slug'], 'link': field['root_link'], 'xpath': field['x_path'], 'filename': field['file'].replace('sheets/', '')})
        return JsonResponse({'fields': fieldsToSend, 'date': timestamp})

    def post(self, request):
        raise Http404

class updateField(TemplateView):

    def get(self, request):
        isSuccess = True

        try:
            requestedSlug = request.GET['slug']
            requestedFileName = request.GET['file']
            requestedLink = request.GET['link']
        except:
            return JsonResponse({'success': False})
        
        try:
            field = Field.objects.get(slug = requestedSlug)
            field.file = f'sheets/{str(requestedFileName)}'
            field.link = requestedLink
            field.updated = datetime.now()
            field.save()
            try:
                updateGroups(requestedSlug)
            except Exception as e:
                print('Could not update groups' + str(e))
        except Exception:
            isSuccess = False
        return JsonResponse({'success': isSuccess})

    def post(self, request):
        raise Http404