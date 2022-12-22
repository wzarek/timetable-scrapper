from datetime import date, timedelta, time
import xlrd
import pandas as pd

GROUPS_DEFAULT = {'caly rok', 'cały rok', 'caly-rok', 'cały-rok', 'całay rok'}

def get_worksheet_dict(path : str, groups_request : list):
    loc : str = (path)
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
            table[i-4]['dlugosc'] = 3
        else:
            table[i-4]['dlugosc'] = int(timedelta(hours=h2.hour-h1.hour, minutes=h2.minute-h1.minute).total_seconds() / (60*15))

        for j in range(0, sheet.ncols):
            if j==0:
                try:
                    cellDate = xlrd.xldate_as_tuple(sheet.cell_value(i, j), wb.datemode)
                    table[i-4][labels[j]] = date(*cellDate[:-3]).strftime("%d-%m-%Y")
                except Exception as e:
                    print(str(e))
                    table[i-4][labels[j]] = 'brak daty'
            elif j==2 or j==3:
                try:
                    cellDate = xlrd.xldate_as_tuple(sheet.cell_value(i, j), wb.datemode)
                    table[i-4][labels[j]] = time(*cellDate[-3:]).strftime("%H:%M")
                except Exception as e:
                    print(str(e))
                    table[i-4][labels[j]] = 'brak daty'
            else:
                table[i-4][labels[j]] = str(sheet.cell_value(i, j)).strip()

    filtered = []

    groups = groups_request.copy()
    if len(groups_request) == 0:
        groups = []
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
            if len(groups) == 0:
                    filtered.append(table[i])

    return filtered

def get_diff(path_first : str, path_second : str, groups : list, field_name : str):
    list1 = get_worksheet_dict(path_first, groups)
    list2 = get_worksheet_dict(path_second, groups)
    diff = [i for i in list1 + list2 if i not in list1 or i not in list2]
    diff_added = [i for i in list2 if i not in list1]
    diff_deleted = [i for i in list1 if i not in list2]
    
    note = 'Zwróć uwagę na arkusze na dole (dodano/usunięto) - mówią one o tym, jakie zajęcia zostały dodane i jakie usunięte w nowym, zmienionym planie.'

    if len(diff) == 0:
        message = f'Twój plan się zmienił, ale zmiany nie obejmują wybranych przez Ciebie grup. Mimo to przygotowaliśmy arkusz całościowych zmian na planie.'
    else:
        message = f'Twój plan się zmienił, a dla Twoich grup znaleźliśmy {len(diff)} zmian. W załączniku znajduje się arkusz ukazujący co się zmieniło.'

    if len(diff) == 0 and len(groups) > 0:
        list1 = get_worksheet_dict(path_first, [])
        list2 = get_worksheet_dict(path_second, [])
        diff_added = [i for i in list2 if i not in list1]
        diff_deleted = [i for i in list1 if i not in list2]
    generate_xls_diff(diff_added, diff_deleted, f'difference-{field_name}.xlsx')

def generate_xls_diff(diff_list_added : list, diff_list_removed : list, file_name : str):
    writer = pd.ExcelWriter(f'media/sheets_diff/{file_name}')

    df_added = pd.DataFrame.from_dict(diff_list_added)
    df_added['prowadzący'] = df_added['stopien'] + ' ' + df_added['imie'] + ' ' + df_added['nazwisko']
    df_added = df_added.reindex(['data', 'dzień tygodnia', 'od', 'do', 'przedmiot', 'rodzaj', 'prowadzący', 'sala', 'grupa'], axis=1)
    df_added.to_excel(writer, sheet_name='dodano')

    df_removed = pd.DataFrame.from_dict(diff_list_removed)
    df_removed['prowadzący'] = df_removed['stopien'] + ' ' + df_removed['imie'] + ' ' + df_removed['nazwisko']
    df_removed = df_removed.reindex(['data', 'dzień tygodnia', 'od', 'do', 'przedmiot', 'rodzaj', 'prowadzący', 'sala', 'grupa'], axis=1)
    df_removed.to_excel(writer, sheet_name='usunięto')

    writer.close()

get_diff("media/sheets/F_s_II_jmgr_14_12_2022.xls", "media/sheets/F_s_II_jmgr_19_12_2022.xls", [], 'fizjoterapia-stac-mag-1rok')