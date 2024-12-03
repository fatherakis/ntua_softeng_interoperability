#!/usr/bin/env python3
from os.path import dirname, abspath
d = dirname(dirname(abspath(__file__))) 
import sys
sys.path.append(d)
import os 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'interoperability.settings')
import django
django.setup()
from backend.db_control import *


args = len(sys.argv) - 1
if not args:
    PATH = "database/sampledata01/"
elif  args == 1:
    PATH = sys.argv[1]

else:
    print("Usage: python3 add_objects.py <optionalPATHto_data_folder>")
    exit()

print('File loading Process Started...')

path = os.getcwd() + "\\database\\sampledata01\\stations.csv"

id_list = {}
comp_list = {}

with open(path) as f:
    reader = csv.reader(f)
    next(reader, None)  #skip header row
    
    for row in reader:
        my_row = row[0].split(';')
        st_id = my_row[0]
        id_list[st_id] = 1
        comp = my_row[1]
        comp_list[comp] = 1
        name = my_row[2]
        try:
            company = TollCompany.objects.get(
                name = comp
            )
        except TollCompany.DoesNotExist:
            company = TollCompany.objects.create(
                name = comp,
                abbr = st_id[:2],
            )
        company.abbr = st_id[:2]
        company.save()
        try:
            station = Station.objects.get(
                id = st_id
            )
        except Station.DoesNotExist:
            station = Station.objects.create(
                id = st_id,
                name = name,
                provider = company,
            )
        station.name = name
        station.provider = company
        station.save()
for ii in TollCompany.objects.all().iterator():
    if ii.name in comp_list:
        continue 
    ii.delete()
for ii in Station.objects.all().iterator():
    if ii.id in id_list:
        continue 
    ii.delete()
    