from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from backend.models import Pass, Vehicle, Station
from backend.db_control import get_vehicles, get_stations
import os 

def reset(model):
    #this is going to be /somedir/TL21-21 + database/sampledata01
    path = os.getcwd() + "/database/sampledata01/"
    try:
        print("Deleting")
        #model.objects.all().delete()
    except Exception as e:
        print("Unexpected error when deleting:" + str(e))
        return JsonResponse({"status": "failed"})

    try:
        print("Beginning reset")
        if model == Vehicle:
            get_vehicles(path + "vehicles.csv")
        else:
            get_stations(path + "stations.csv")
    except Exception as e:
        print("Unexpected error when reseting:" + str(e))
        return JsonResponse({"status": "failed"})
    
    return JsonResponse({"status": "success"})


@api_view(['GET'])
def healthcheck(request):
    return JsonResponse({"status": "success"})          #we are always connected to db (the db is a file: .sqlite3)

#Deletes all current passes
@api_view(['POST'])
def resetpasses(request):
    path = os.getcwd() + "/database/sampledata01/"
    try:
        print("Deleting passes")
        Pass.objects.all().delete()
    except Exception as e:
        print("Unexpected error when deleting passes:" + str(e))
        return JsonResponse({"status": "failed"})
    return JsonResponse({"status": "success"})

#Resets vehicles to default ones 
@api_view(['POST'])
def resetvehicles(request):
    try: 
        reset(Vehicle)
    except:
        return JsonResponse({"status": "failed"})
    return JsonResponse({"status": "success"})

#Resets stations to default ones
@api_view(['POST'])
def resetstations(request):
    try:
        reset(Station)
    except:
        return JsonResponse({"status": "failed"})
    return JsonResponse({"status": "success"})

