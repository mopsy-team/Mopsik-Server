# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.management.base import BaseCommand
from mops_api.models import MOP, Operator
import os
import urllib.request
import filecmp
from openpyxl import load_workbook

mops_api_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#XLSX_URL = 'https://www.mimuw.edu.pl/~pawelg/RID/MOPy/MOP%202016-08-02.xlsx'
XLSX_URL = 'https://students.mimuw.edu.pl/~pp371308/zpp/mopsik/mopy.xlsx'
NEW_XLSX_LOCATION = mops_api_dir + '/data/mopy_new.xlsx'
OLD_XLSX_LOCATION = mops_api_dir + '/data/mopy_old.xlsx'
LOCAL_CSV_LOCATION = ''


def get_boolean(x):
    if x is None:
        return None
    if 'tak' in x:
        return 1
    elif 'nie' in x:
        return 0
    else:
        raise ValueError("WRONG BOOLEAN")


def get_mop_type(x):
    x = str(x)
    if 'III' in x:
        return 3
    elif 'II' in x:
        return 2
    elif 'I' in x:
        return 1
    else:
        return 1
        #    raise ValueError("WRONG MOP TYPE")


# def get_mop_name(x):
#     x = str(x)
#     mop_type_length = get_mop_type(x)
#     # In given Excel we have format "MOP mop_type name"
#     if len(x) < 4 + mop_type_length:
#         raise ValueError
#     elif len(x) == 4 + mop_type_length:
#         return ''
#     else:
#         return x[5 + mop_type_length:]


def download_new_file():
    urllib.request.urlretrieve(XLSX_URL, NEW_XLSX_LOCATION)


def create_operator(attr):
    if not 'operator_name' in attr.keys():
        return Operator(name='-')
    operator, _ = Operator.objects.get_or_create(name=attr['operator_name'])
    for (key, value) in attr.items():
        if key != 'operator_name' and value is not None:
            setattr(operator, key, value)
    print(operator)
    operator.save()
    return operator


def create_mop(attr, _operator):
    mop, created = MOP.objects.get_or_create(x=attr['x'], y=attr['y'], operator=_operator)
    for (key, value) in attr.items():
        if value is not None:
            setattr(mop, key, value)
    print(mop)
    mop.save()
    return mop


def parse_phone_number(x):
    if x is None or x == '-':
        return '-'
    x = str(x).replace(' ', '')
    x = str(int(x))
    print(x)
    assert len(x) == 9
    return x


def parse_email(x):
    if x is None or x == '-':
        return '-'
    return x


class Command(BaseCommand):
    def parse(self):
        wb = load_workbook(filename=NEW_XLSX_LOCATION, data_only=True)
        ws = wb.get_active_sheet()
        for row in ws.iter_rows():
            if row[1].value is not None:

                mop_attr = {}
                operator_attr = {}
                it = 0
                try:
                    it += 1
                    mop_attr['number_in_excel'] = int(row[it].value)
                except:
                    continue

                print(row)
                try:
                    it += 1
                    mop_attr['department'] = row[it].value
                    it += 1
                    print('lol')
                    mop_attr['town'] = str(row[it].value)
                    it += 1
                    mop_attr['type'] = get_mop_type(row[it].value)
                    mop_attr['name'] = row[it].value

                    it += 1
                    mop_attr['x_92'] = row[it].value
                    it += 1
                    mop_attr['y_92'] = row[it].value
                    it += 1
                    print(row[it].value)
                    mop_attr['x'] = row[it].value
                    it += 1
                    print(row[it].value)
                    mop_attr['y'] = row[it].value

                    it += 1
                    mop_attr['road_technical_class'] = row[it].value
                    it += 1
                    mop_attr['road_number'] = row[it].value

                    # chainage
                    it += 1

                    it += 1
                    mop_attr['direction'] = row[it].value

                    # turnoff
                    it += 1

                    it += 1
                    mop_attr['passenger_places'] = row[it].value
                    it += 1
                    mop_attr['truck_places'] = row[it].value
                    it += 1
                    mop_attr['bus_dedicated_places'] = row[it].value

                    it += 1
                    mop_attr['security'] = get_boolean(row[it].value)
                    it += 1
                    mop_attr['fence'] = get_boolean(row[it].value)
                    it += 1
                    mop_attr['monitoring'] = get_boolean(row[it].value)
                    it += 1
                    mop_attr['lighting'] = get_boolean(row[it].value)
                    it += 1
                    mop_attr['petrol_station'] = get_boolean(row[it].value)
                    it += 1
                    mop_attr['dangerous_cargo_places'] = get_boolean(row[it].value)
                    it += 1
                    mop_attr['restaurant'] = get_boolean(row[it].value)
                    it += 1
                    mop_attr['sleeping_places'] = get_boolean(row[it].value)
                    it += 1
                    mop_attr['toilets'] = get_boolean(row[it].value)
                    it += 1
                    mop_attr['car_wash'] = get_boolean(row[it].value)
                    it += 1
                    mop_attr['garage'] = get_boolean(row[it].value)

                    it += 1

                    if row[it].value != '-' and row[it].value is not None:
                        operator_attr['operator_name'] = row[it].value
                        it += 1
                        operator_attr['phone'] = parse_phone_number(row[it].value)
                        it += 1
                        operator_attr['email'] = parse_email(row[it].value)
                        it += 1
                        operator_attr['permission'] = get_boolean(row[it].value)
                except ValueError as e:
                    print(e)
                    print('lol')
                    return False

                operator = create_operator(operator_attr)

                mop = create_mop(mop_attr, operator)

        return True

    def handle(self, *args, **options):
        download_new_file()
        # if filecmp.cmp(NEW_XLSX_LOCATION, OLD_XLSX_LOCATION):
        #    os.remove(NEW_XLSX_LOCATION)
        # else:
        if self.parse():
            os.rename(NEW_XLSX_LOCATION, OLD_XLSX_LOCATION)
        else:
            print("Incorrect file on server")