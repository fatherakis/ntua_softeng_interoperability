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


get_stations(PATH + "stations.csv")

get_vehicles(PATH + "vehicles.csv")

get_starting_passes(PATH + "passes.csv")

