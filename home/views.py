import array
from dataclasses import field, fields
from pipes import Template
from sys import argv
from tokenize import group
from django.shortcuts import render
from django.views.generic import TemplateView
import xlrd
from datetime import date, datetime, time, timedelta
from icalendar import Calendar, Event
from .models import Field, Group
from django.http import Http404

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
        desc = row['prowadzacy']
        event.add('description', desc)
        if 'sala' in row.keys():
            event.add('location', row['sala'].replace('.0', ''))
        cal.add_component(event)

    f = open('icals/' + name, 'wb')
    f.write(cal.to_ical())
    f.close()

def uopolski(fieldSlug : str, week : int, groups : array):
    field_object = Field.objects.get(slug = fieldSlug)

    loc = (field_object.file.path)
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
        h1 = time(*h1e[-3:])
        h2 = time(*h2e[-3:])
        table[i-4]['dlugosc'] = int(timedelta(hours=h2.hour-h1.hour, minutes=h2.minute-h1.minute).total_seconds() / (60*15))
        for j in range(0, sheet.ncols):
            if j==0:
                cellDate = xlrd.xldate_as_tuple(sheet.cell_value(i, j), wb.datemode)
                table[i-4][labels[j]] = date(*cellDate[:-3]).strftime("%d-%m-%Y")
            elif j==2 or j==3:
                cellDate = xlrd.xldate_as_tuple(sheet.cell_value(i, j), wb.datemode)
                table[i-4][labels[j]] = time(*cellDate[-3:]).strftime("%H:%M")
            else:
                table[i-4][labels[j]] = str(sheet.cell_value(i, j))

    filtered = []
    if len(groups) == 0:
        groups = ['II', 3, 'cały rok']
    elif not 'cały rok' in groups:
        groups.append('cały rok')
    elif not 'caly rok' in groups:
        groups.append('caly rok')

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
    for i in range(5):
        filteredWeekdays[days[i]] = []
        for j in range(starting,ending+1):
            if filtered[j]['data'] == weekArr[days[i]]:
                filteredWeekdays[days[i]].append(filtered[j])

    for i in range(5):
        for j in range(len(filteredWeekdays[days[i]])):
            if j == 0:
                diff = int(((datetime.strptime(filteredWeekdays[days[i]][j]['od'],"%H:%M") - datetime.strptime(hours[0],"%H:%M")).total_seconds()) / (60*15))
                filteredWeekdays[days[i]][j]['diff'] = diff
            else:
                diff = int(((datetime.strptime(filteredWeekdays[days[i]][j]['od'],"%H:%M") - datetime.strptime(filteredWeekdays[days[i]][j-1]['do'],"%H:%M")).total_seconds()) / (60*15))
                filteredWeekdays[days[i]][j]['diff'] = diff
    
    for row in filtered:
        row['prowadzacy'] = row['stopien'] + " " + row['imie'] + " " + row['nazwisko']

    weekArr.pop(days[5])
    weekArr.pop(days[6])
    iCalPath = f'{field_object.slug}-grupy-{"-".join(groups[:-1])}.ics'
    genIcal(filtered, iCalPath)
    context = {'title': f'Timetable scrapper | {field_object.name}, {field_object.year} rok, {field_object.degree}, {field_object.type} gr.: {" ".join(groups[:-1])}', 'today' : today, 'weekday': days[todaysWeekday], 'weekArr': weekArr, 'planFiltered': filteredWeekdays, 'wNum': week, 'hours': hours, 'filePath': 'icals/' + iCalPath, 'groups': groups, 'field': field_object}
    return context

class timetable(TemplateView):
    template = 'timetable.html'

    def get(self, request):
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
        else:
            fieldSlug = request.session.get('fieldSlug', 'dietetyka-lic-1rok-stac')

        #try:
        field = Field.objects.get(slug = fieldSlug)
        note = f'{field.name}, {field.year} rok, {field.degree}, {field.type} - {field.university.name}'
        context = uopolski(fieldSlug, week, groups)
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

    def get(self, request): 
        return render(request, self.template, self.context)

    def post(self, request):
        return render(request, self.template, self.context)

class chooseField(TemplateView):
    template = 'fieldchooser.html'
    parentFields = Field.objects.filter(parent__isnull = True).values()
    fieldsFiltered = {}
    for p in parentFields:
        fieldsFiltered[p['name']] = Field.objects.filter(parent__slug = p['slug']).values()
    print(fieldsFiltered)
    fields = Field.objects.all().values()
    context = {'title': 'Timetable scrapper | wybierz kierunek', 'headertitle': 'wybierz odpowiadający plan', 'fields': fields}

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
        groups = Group.objects.filter(fields__slug = field).values()
        field = Field.objects.get(slug = field)
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