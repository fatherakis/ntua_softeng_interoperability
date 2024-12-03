from multiprocessing.sharedctypes import Value
from django.db.models import Sum
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import bad_request

from api.serializers import *
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework_csv.renderers import CSVRenderer
from backend.models import Pass,Vehicle,Station,TollCompany
from datetime import datetime


#--1st endpoint: {baseURL}/PassesPerStation/:stationID/:date_from/:date_to--
class PPScsv(CSVRenderer):
    header = ["PassIndex", "PassID", "PassTimeStamp",
        "VehicleID", "TagProvider", "PassType", "PassCharge",]
    writer_opts = {"delimiter": ";"}
@api_view(['GET'])
@renderer_classes([JSONRenderer, PPScsv,])
def passes_per_station(request, stationID, date_from, date_to, format=None):
    try:
        station = Station.objects.get(pk=stationID)
    except Station.DoesNotExist:
        return bad_request(request, Station.DoesNotExist)
    comp_name = station.provider.name
    try:
        PeriodFrom = datetime.strptime(str(date_from), "%Y%m%d")
        PeriodTo = datetime.strptime(str(date_to), "%Y%m%d")
    except ValueError:
        return bad_request(request, ValueError) #error 400


    serializer = StationSerializer(station,
        context={
            "RequestTimestamp":
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "StationOperator":comp_name,
            "From":PeriodFrom, "To":PeriodTo,
        }
    )

    data = serializer.data
    if request.query_params.get("format") == "csv":
         data = data["PassesList"]

    response = Response(data)
    if data is None:
        response.status_code = 402
    return response
#---------------------------------------------------------------------------



class Analysiscsv(CSVRenderer):
    header = ["PassIndex", "PassID","StationID","PassTimeStamp",
        "VehicleID","PassCharge",]
    writer_opts = {"delimiter": ";"}
@api_view(['GET'])
@renderer_classes([JSONRenderer, Analysiscsv,])
def passes_analysis(request, op1_ID, op2_ID, date_from, date_to):
    try:
        station0 = TollCompany.objects.get(abbr__exact=op1_ID)
    except TollCompany.DoesNotExist:
        return bad_request(request, Station.DoesNotExist)
    try:
        station1 = TollCompany.objects.get(abbr__exact=op2_ID)
    except TollCompany.DoesNotExist:
        return bad_request(request, Station.DoesNotExist)
    try:
        date_to_formated = datetime.strptime(date_to, '%Y%m%d')
        date_from_formated = datetime.strptime(date_from, '%Y%m%d')
    except ValueError:
        return bad_request(request, ValueError) #400
    serializer = TollAnalysisSerializer(station0,
        context={"RequestTimestamp":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "From":date_from_formated, "To":date_to_formated, "Of":op2_ID})
    data = serializer.data
    if request.query_params.get("format") == "csv":
        data = data["PassesList"]

    response = Response(data)
    if data is None:
        response.status_code = 402
    return response
#---------------------------------------------------------------------------
class PassesCostcsv(CSVRenderer):
    header = ["op1_ID", "op2_ID","RequestTimestamp","PeriodFrom",
        "PeriodTo","NumberOfPasses","PassesCost"]
    writer_opts = {"delimiter": ";"}

class PassesCostInfo:
    def __init__(self, op1_ID, op2_ID, date_from, date_to, num, cost):
        self.op1_ID = op1_ID
        self.op2_ID = op2_ID
        self.RequestTimestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.PeriodFrom = date_from.strftime("%Y-%m-%d")
        self.PeriodTo = date_to.strftime("%Y-%m-%d")
        self.NumberOfPasses = num
        self.PassesCost = float(round(cost,2))
@api_view(['GET'])
@renderer_classes([JSONRenderer, PassesCostcsv,])
def passes_cost(request, op1_ID, op2_ID, date_from, date_to):
    # Ensuring station providers exist
    try:
        station0 = TollCompany.objects.get(abbr__exact=op1_ID)
    except TollCompany.DoesNotExist:
        return bad_request(request, Station.DoesNotExist)
    try:
        station1 = TollCompany.objects.get(abbr__exact=op2_ID)
    except TollCompany.DoesNotExist:
        return bad_request(request, Station.DoesNotExist)
    try:
    # Change date format
        reconstructed_date_from = datetime.strptime(date_from, '%Y%m%d')
        reconstructed_date_to = datetime.strptime(date_to, '%Y%m%d')
    except ValueError:
        return bad_request(request, ValueError) #400
    # Filter the passes
    passes_after = Pass.objects.filter(timestamp__gte=reconstructed_date_from)
    passes_timeframe = passes_after.filter(timestamp__lte=reconstructed_date_to)
    # Filter the operators
    passes_op1 = passes_timeframe.filter(station__provider__abbr=station0.abbr)
    passes_complete = passes_op1.filter(vehicle__tag_id__startswith=station1.abbr)
    # Now we need the count of the objects and the sum of the costs
    count = passes_complete.count()
    if count != 0:
        total_charge = passes_complete.aggregate(Sum('charge'))['charge__sum']
    else:
        total_charge = 0
    passescostinfo = PassesCostInfo(op1_ID, op2_ID, reconstructed_date_from, reconstructed_date_to, count, total_charge)
    passescostserializer = PassesCostSerializer(passescostinfo)
    data = passescostserializer.data

    response = Response(data)
    if data is None:
        response.status_code = 402
    return response
#----------------------------------------------------------------------------
class ChargesBycsv(CSVRenderer):
    header = ["VisitingOperator","NumberOfPasses","PassesCost"]
    writer_opts = {"delimiter": ";"}
@api_view(['GET'])
@renderer_classes([JSONRenderer, ChargesBycsv,])
def charges_by(request,op_ID,date_from,date_to):
    try:
        station = TollCompany.objects.get(abbr__exact=op_ID)
    except TollCompany.DoesNotExist:
        return bad_request(request, Station.DoesNotExist)
    try:
        date_to_formated = datetime.strptime(date_to, '%Y%m%d')
        date_from_formated = datetime.strptime(date_from, '%Y%m%d')
    except ValueError:
        return bad_request(request, ValueError) #400
    serializer = ChargesBySerializer(station,
        context={"RequestTimestamp":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "From":date_from_formated, "To":date_to_formated})

    data = serializer.data
    if request.query_params.get("format") == "csv":
        data = data["PPOList"]

    response = Response(data)
    if data is None:
        response.status_code = 402
    return response

#----------------------------------------------------------------------------
class Settlementscsv(CSVRenderer):
    header = ["Operator", "Status", "Amount"]
    writer_opts = {"delimiter": ";"}

@api_view(['GET'])
@renderer_classes([JSONRenderer, Settlementscsv,])
def settlements(request, op_ID):
    # Ensuring Toll Company exists
    try:
        company = TollCompany.objects.get(abbr__exact=op_ID)
    except TollCompany.DoesNotExist:
        return bad_request(request, TollCompany.DoesNotExist)

    # Making a list of the other companies
    other_companies = TollCompany.objects.exclude(name__exact=company.name)
    companies_list = []
    for comp in other_companies:
        companies_list.append(comp.abbr)

    # Filter the operator (for passes they owe to our company)
    passes_theyowe = Pass.objects.filter(station__provider__abbr=company.abbr)

    # Filter the vehicle tags (for the passes our company owes to them)
    passes_weowe = Pass.objects.filter(vehicle__tag_id__startswith=company.abbr)

    settlements = []

    for comp_abbr in companies_list:
        current_passes_theyowe = passes_theyowe.filter(vehicle__tag_id__startswith=comp_abbr)
        current_passes_weowe = passes_weowe.filter(station__provider__abbr=comp_abbr)
        count = current_passes_theyowe.count()
        if count != 0:
            total_charge_theyowe = current_passes_theyowe.aggregate(Sum('charge'))['charge__sum']
        else:
            total_charge_theyowe = 0
        count = current_passes_weowe.count()
        if count != 0:
            total_charge_weowe = current_passes_weowe.aggregate(Sum('charge'))['charge__sum']
        else:
            total_charge_weowe = 0
        difference = total_charge_theyowe - total_charge_weowe
        if difference <= 0: # we owe more
            difference = difference*(-1)
            difference = float(round(difference,2))
            status = "You owe them"
        else:               # they owe more
            difference = float(round(difference,2))
            status = "They owe you"
        current_settlements_info = {"Operator": comp_abbr,
            "Status": status,
            "Amount": difference,
        }
        settlements.append(current_settlements_info)

    settlementsserializer = SettlementsSerializer(settlements, many=True)

    data = settlementsserializer.data
    response = Response(data)
    if data is None:
        response.status_code = 402
    return response

#@api_view(['GET'])
#def index(request):
#    return Response("WIP")

#@api_view(['POST'])
#def login(request):
#    return Response("WIP")

#@api_view(['POST'])
#def logout(request):
#    return Response("WIP")
