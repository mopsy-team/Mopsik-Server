# -*- coding: utf-8 -*-
import filecmp
import os
import random
import urllib.request

from django.core.management.base import BaseCommand
from openpyxl import load_workbook

from mops_api.models import MOP, Operator

mops_api_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
XLSX_URL = 'https://www.mimuw.edu.pl/~pawelg/RID/MOPy/MOP%202016-08-02.xlsx'
# XLSX_URL = 'https://students.mimuw.edu.pl/~pp371308/zpp/mopsik/mopy.xlsx'
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
        print("Wrong Boolean")
        return 0
        # raise ValueError("WRONG BOOLEAN")


def get_mop_type(nr, x):
    x = str(x)
    if 'III' in x:
        return 3
    elif 'II' in x:
        return 2
    elif 'I' in x:
        return 1
    else:
        print("Wrong MOP type in line " + str(nr))
        return 1


def randomize_free_places(mop):
    mop.taken_bus_dedicated_places = random.randint(0, mop.bus_dedicated_places)
    mop.taken_truck_places = random.randint(0, mop.truck_places)
    mop.taken_passenger_places = random.randint(0, mop.passenger_places)


def download_new_file():
    urllib.request.urlretrieve(XLSX_URL, NEW_XLSX_LOCATION)


def create_operator(attr):
    if not 'name' in attr.keys() or attr['permission'] == 'nie':
        return Operator(name='-')
    operator, _ = Operator.objects.get_or_create(name=attr['name'])
    for (key, value) in attr.items():
        if key != 'name' and value is not None:
            setattr(operator, key, value)
    operator.save()
    return operator


def create_mop(attr, _operator):
    if attr['title'] is not None and attr['x'] is not None and attr['y'] is not None:
        mop, created = MOP.objects.get_or_create(x=attr['x'], y=attr['y'], title=attr['title'], operator=_operator)
        for (key, value) in attr.items():
            if value is not None:
                setattr(mop, key, value)
        randomize_free_places(mop)
        mop.save()
        return mop


def parse_phone_number(x):
    if x is None or x == '-':
        return '-'
    x = str(x)
    ret = ''
    counter = 0
    for c in x:
        if not c.isspace():
            counter += 1
            ret += c
        if counter == 9:
            break
    return ret


def parse_email(x):
    if x is None or x == '-':
        return '-'
    return x.strip()


def parse_name(x):
    if x is None or x == '-':
        return '-'
    return x.strip()


class Command(BaseCommand):
    def parse(self):
        wb = load_workbook(filename=NEW_XLSX_LOCATION, data_only=True)
        ws = wb.active
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

                try:
                    it += 1
                    mop_attr['department'] = row[it].value
                    it += 1
                    mop_attr['town'] = str(row[it].value)
                    it += 1
                    mop_attr['type'] = get_mop_type(mop_attr['number_in_excel'], row[it].value)
                    mop_attr['title'] = row[it].value

                    it += 1
                    mop_attr['x_92'] = row[it].value
                    it += 1
                    mop_attr['y_92'] = row[it].value
                    it += 1
                    mop_attr['x'] = row[it].value
                    it += 1
                    mop_attr['y'] = row[it].value

                    it += 1
                    mop_attr['road_technical_class'] = row[it].value
                    it += 1
                    mop_attr['road_number'] = row[it].value

                    it += 1
                    mop_attr['chainage'] = row[it].value

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
                    operator_attr['name'] = parse_name(row[it].value)
                    it += 1
                    operator_attr['phone'] = parse_phone_number(row[it].value)
                    it += 1
                    operator_attr['email'] = parse_email(row[it].value)
                    it += 1
                    operator_attr['permission'] = get_boolean(row[it].value)

                except ValueError as e:
                    print(e)
                    print(mop_attr['number_in_excel'])
                    return False

                operator = create_operator(operator_attr)

                mop = create_mop(mop_attr, operator)

        return True

    def handle(self, *args, **options):
        download_new_file()
        if filecmp.cmp(NEW_XLSX_LOCATION, OLD_XLSX_LOCATION):
            os.remove(NEW_XLSX_LOCATION)
        else:
            if self.parse():
                os.rename(NEW_XLSX_LOCATION, OLD_XLSX_LOCATION)
            else:
                print("Incorrect file on server")
