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

path = path = os.getcwd() + "\\database\\sampledata01\\vehicles.csv"
vh_list = {}

with open(path) as f:
        reader = csv.reader(f)
        next(reader, None)  #skip header row

        for row in reader:
            my_row = row[0].split(';')
            v_id = my_row[0]
            vh_list[v_id] = 1
            t_id = my_row[1]
            t_p = my_row[2]
            l_year = my_row[4]
            # This might throw exception if ran before TollCompany insertion
            try: 
                company = TollCompany.objects.get(name = t_p,)
            except: 
                print(t_p)
                continue
            try: 
                veh = Vehicle.objects.get(
                    id = v_id,
                )                
            except Vehicle.DoesNotExist:
                veh = Vehicle.objects.create(
                    id = v_id, 
                    tag_id = t_id,
                    license_year = l_year,
                    tag_provider = company,
                )
            veh.license_year = l_year
            veh.tag_provider = company
            veh.tag_id = t_id
            veh.save()
            
for ii in Vehicle.objects.all().iterator():
    if ii.id in vh_list:
        continue
    ii.delete()
