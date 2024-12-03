import csv
from backend.models import *
from datetime import datetime


def get_stations(path):
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
        

def get_vehicles(path):
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



    
def get_starting_passes(path): 
    with open(path) as f:
        reader = csv.reader(f)
        next(reader, None)  #skip header row
        ctr = 0
        for row in reader:
            ctr+=1
            if(ctr%300 == 0):
                print(f'Completed another 300: {ctr}')
            my_row = row[0].split(';')
            pid = my_row[0]
            time_stamp = datetime.strptime(my_row[1], "%d/%m/%Y %H:%M")
            s_ref = my_row[2]
            v_ref = my_row[3]
            charge = float(format(float(my_row[4]),'.2f'))
            station = Station.objects.get(id = s_ref,)
            vehicle = Vehicle.objects.get(id = v_ref,)
            try:
                passes = Pass.objects.get_or_create(
                    id = pid,
                    timestamp = time_stamp,
                    station = station,
                    vehicle = vehicle,
                    charge = charge,
                )
            except Exception as e:
                print(e)