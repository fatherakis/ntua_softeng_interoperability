
from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.http import HttpResponse
from backend.models import Pass,Vehicle,Station,TollCompany
from datetime import datetime
from django.db.models import Sum
import json
import click
import urllib3

c = Client(HTTP_USER_AGENT='Mozilla/1.1')
def passesperstation(station, datefrom, dateto, format):
    r = c.get(
         "/interoperability/api/PassesPerStation/"
             + station + "/"
             + datefrom + "/"
             + dateto+"/?format="+format,
        verify=False
    )

    if r.status_code == 200:
        if format == "csv":
            return r.content
        else:
            return r.json()

    else:
        return r

def passesanalysis(op1, op2, datefrom, dateto, format):
    r = c.get(
        "/interoperability/api/PassesAnalysis/"
             + op1 + "/" + op2 + "/"
             + datefrom + "/" + dateto +"/?format="+format,
        verify=False
    )

    if r.status_code == 200:
        if format == "csv":
            return r.content
        else:
            return r.json()

    else:
        return r


def passescost(op1, op2, datefrom, dateto, format):
    r = c.get(
        "/interoperability/api/PassesCost/"
             + op1 + "/" + op2 + "/"
             + datefrom + "/" + dateto+"/?format="+format,
        verify=False
    )

    if r.status_code == 200:
        if format == "csv":
            return r.content
        else:
            return r.json()

    else:
        return r

def chargesby(op1, datefrom, dateto, format):
    r = c.get(
        "/interoperability/api/ChargesBy/"
             + op1 + "/"
             + datefrom + "/" + dateto+"/?format="+format,
        verify=False
    )

    if r.status_code == 200:
        if format == "csv":
            return r.content
        else:
            return r.json()

    else:
        return r

def settlements(op, format):
    r = c.get(
        "/interoperability/api/Settlements/"
             + op + "/?format=" + format,
        verify=False
    )

    if r.status_code == 200:
        if format == "csv":
            return r.content
        else:
            return r.json()

    else:
        return r

class CLIUnitTests(TestCase):

    #----------------TYPICAL TESTS----------------#
    def test_passesperstation1_in_cli(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        company1 = TollCompany.objects.create(name = "aodos", abbr = "AO")
        company2 = TollCompany.objects.create(name = "engatia", abbr = "EG")
        station = Station.objects.create(id="AO01", name="AO01", provider=company1)
        vehicle = Vehicle.objects.create(id="EC05LZC49528", tag_id="EG13892", license_year="2012", tag_provider=company2)
        Pass.objects.create(id="CER6738702", timestamp="2021-10-14 00:00:00", station=station, charge="2.20", vehicle=vehicle)
        station = "AO01"
        datefrom = "20211013"
        dateto = "20211017"
        format = "json"
        r = passesperstation(station,datefrom,dateto,format)

        #response = c.get('/interoperability/api/PassesPerStation/'+station+'/'+datefrom+'/'+dateto+'/')
        #r=response.json()
        self.maxDiff = None
        l = json.dumps(r["PassesList"])
        #self.assertEqual(r.status_code,200)
        self.assertEqual(1,r["NumberOfPasses"])
        self.assertEqual("AO01",r["Station"])
        self.assertEqual('[{"PassIndex": 1, "PassID": "CER6738702", "PassTimeStamp": "2021-10-14 00:00:00", "VehicleID": "EC05LZC49528", "TagProvider": "engatia", "PassType": "visitor", "PassCharge": 2.2}]',l)


    def test_passesanalysis1_in_cli(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        company1 = TollCompany.objects.create(name = "egnatia", abbr = "EG")
        company2 = TollCompany.objects.create(name = "gefyra", abbr = "GF")
        station = Station.objects.create(id="EG01", name="EG01", provider=company1)
        station1 = Station.objects.create(id="EG02", name="EG02", provider=company1)
        vehicle = Vehicle.objects.create(id="EC05LZC49518", tag_id="GF13892", license_year="2012", tag_provider=company2)
        Pass.objects.create(id="CER6528702", timestamp="2021-10-13 16:43:12", station=station, charge="2.20", vehicle=vehicle)
        Pass.objects.create(id="CER6738632", timestamp="2021-10-14 21:03:08", station=station1, charge="1.10", vehicle=vehicle)
        op1="EG"
        op2="GF"
        datefrom = "20211013"
        dateto = "20211017"
        format = "json"
        r = passesanalysis(op1,op2,datefrom,dateto,format)
        #response = c.get('/interoperability/api/PassesAnalysis/'+op1+'/'+op2+'/'+datefrom+'/'+dateto+'/')
        #r=response.json()
        self.maxDiff = None
        l = json.dumps(r["PassesList"])
        #self.assertEqual(response.status_code,200)
        self.assertEqual(2,r["NumberOfPasses"])
        self.assertEqual("EG",r["op1_ID"])
        self.assertEqual("GF",r["op2_ID"])
        self.assertEqual('[{"PassIndex": 1, "PassID": "CER6528702", "StationID": "EG01", "PassTimeStamp": "2021-10-13 16:43:12", "VehicleID": "EC05LZC49518", "PassCharge": 2.2}, {"PassIndex": 2, "PassID": "CER6738632", "StationID": "EG02", "PassTimeStamp": "2021-10-14 21:03:08", "VehicleID": "EC05LZC49518", "PassCharge": 1.1}]',l)

    def test_passescost1_in_cli(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        company1 = TollCompany.objects.create(name = "egnatia", abbr = "EG")
        company2 = TollCompany.objects.create(name = "gefyra", abbr = "GF")
        station = Station.objects.create(id="EG01", name="EG01", provider=company1)
        station1 = Station.objects.create(id="EG02", name="EG02", provider=company1)
        vehicle = Vehicle.objects.create(id="EC05LZC49518", tag_id="GF13892", license_year="2012", tag_provider=company2)
        Pass.objects.create(id="CER6528702", timestamp="2021-10-13 16:43:12", station=station, charge="2.20", vehicle=vehicle)
        Pass.objects.create(id="CER6738632", timestamp="2021-10-14 21:03:08", station=station1, charge="1.10", vehicle=vehicle)
        op1="EG"
        op2="GF"
        datefrom = "20211013"
        dateto = "20211017"
        format = "json"
        r = passescost(op1,op2,datefrom,dateto,format)
        #response = c.get('/interoperability/api/PassesCost/'+op1+'/'+op2+'/'+datefrom+'/'+dateto+'/')
        #r=response.json()
        self.maxDiff = None
        l = json.dumps(r["PassesCost"])
        #self.assertEqual(response.status_code,200)
        self.assertEqual(2,r["NumberOfPasses"])
        self.assertEqual("EG",r["op1_ID"])
        self.assertEqual("GF",r["op2_ID"])
        self.assertEqual('3.3',l)

    def test_chagesby1_in_cli(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        company1 = TollCompany.objects.create(name = "egnatia", abbr = "EG")
        company2 = TollCompany.objects.create(name = "gefyra", abbr = "GF")
        company3 = TollCompany.objects.create(name = "aodos", abbr = "AO")
        station = Station.objects.create(id="EG01", name="EG01", provider=company1)
        station1 = Station.objects.create(id="EG02", name="EG02", provider=company1)
        vehicle = Vehicle.objects.create(id="EC05LZC49518", tag_id="GF13892", license_year="2012", tag_provider=company2)
        vehicle1 = Vehicle.objects.create(id="EC05LZC29518", tag_id="AO14892", license_year="2015", tag_provider=company3)
        Pass.objects.create(id="CER6528702", timestamp="2021-10-13 16:43:12", station=station, charge="2.20", vehicle=vehicle)
        Pass.objects.create(id="CER6738632", timestamp="2021-10-14 21:03:08", station=station1, charge="1.10", vehicle=vehicle1)
        op1="EG"
        datefrom = "20211013"
        dateto = "20211017"
        format = "json"
        r = chargesby(op1,datefrom,dateto,format)
        #response = c.get('/interoperability/api/ChargesBy/'+op1+'/'+datefrom+'/'+dateto+'/')
        #r=response.json()
        self.maxDiff = None
        l = json.dumps(r["PPOList"])
        #self.assertEqual(response.status_code,200)
        self.assertEqual("EG",r["op_ID"])
        self.assertEqual('[{"VisitingOperator": "GF", "NumberOfPasses": 1, "PassesCost": 2.2}, {"VisitingOperator": "AO", "NumberOfPasses": 1, "PassesCost": 1.1}]',l)

    def test_settlements1_in_cli(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        company1 = TollCompany.objects.create(name = "egnatia", abbr = "EG")
        company2 = TollCompany.objects.create(name = "gefyra", abbr = "GF")
        company3 = TollCompany.objects.create(name = "aodos", abbr = "AO")
        station = Station.objects.create(id="EG01", name="EG01", provider=company1)
        station1 = Station.objects.create(id="EG02", name="EG02", provider=company1)
        vehicle = Vehicle.objects.create(id="EC05LZC49518", tag_id="GF13892", license_year="2012", tag_provider=company2)
        vehicle1 = Vehicle.objects.create(id="EC05LZC29518", tag_id="AO14892", license_year="2015", tag_provider=company3)
        Pass.objects.create(id="CER6528702", timestamp="2021-10-13 16:43:12", station=station, charge="2.20", vehicle=vehicle)
        Pass.objects.create(id="CER6738632", timestamp="2021-10-14 21:03:08", station=station1, charge="1.10", vehicle=vehicle1)
        op1="EG"
        format = "json"
        r = settlements(op1,format)
        self.maxDiff = None
        l = json.dumps(r)
        self.assertEqual('[{"Operator": "GF", "Status": "They owe you", "Amount": 2.2}, {"Operator": "AO", "Status": "They owe you", "Amount": 1.1}]',l)

    #----------------BIG TESTS----------------#

    def test_passesperstation_big_in_cli(self):

        company1 = TollCompany.objects.create(name = "gefyra", abbr = "GF")
        company2 = TollCompany.objects.create(name = "engatia", abbr = "EG")
        company3 = TollCompany.objects.create(name = "aodos", abbr = "AO")
        company4 = TollCompany.objects.create(name = "moreas", abbr = "MR")
        station = Station.objects.create(id="GF01", name="GF01", provider=company1)
        vehicle = Vehicle.objects.create(id="EC05LZC49528", tag_id="EG13892", license_year="2012", tag_provider=company2)
        vehicle1 = Vehicle.objects.create(id="EC05LAC49528", tag_id="AO13892", license_year="2012", tag_provider=company3)
        vehicle2 = Vehicle.objects.create(id="EC05LZC49529", tag_id="GF13892", license_year="2012", tag_provider=company1)
        vehicle3 = Vehicle.objects.create(id="EC05LZC49521", tag_id="MR13892", license_year="2012", tag_provider=company4)
        Pass.objects.create(id="CYR6739702", timestamp="2021-10-14 00:05:13", station=station, charge="2.20", vehicle=vehicle)
        Pass.objects.create(id="CWR6721702", timestamp="2021-10-15 01:32:12", station=station, charge="2.30", vehicle=vehicle1)
        Pass.objects.create(id="CNR6736705", timestamp="2021-10-14 23:26:19", station=station, charge="2.80", vehicle=vehicle2)
        Pass.objects.create(id="CFE8738707", timestamp="2021-10-14 07:00:06", station=station, charge="2.70", vehicle=vehicle3)
        Pass.objects.create(id="CLE6733702", timestamp="2021-10-14 19:54:00", station=station, charge="3.20", vehicle=vehicle1)
        Pass.objects.create(id="CET6738704", timestamp="2021-10-14 16:00:43", station=station, charge="2.10", vehicle=vehicle2)
        Pass.objects.create(id="BYR6739702", timestamp="2021-10-14 00:05:13", station=station, charge="2.20", vehicle=vehicle3)
        Pass.objects.create(id="BWR6721702", timestamp="2021-10-15 01:32:12", station=station, charge="2.30", vehicle=vehicle1)
        Pass.objects.create(id="BNR6736705", timestamp="2021-10-14 23:26:19", station=station, charge="2.80", vehicle=vehicle2)
        Pass.objects.create(id="BFE8738707", timestamp="2021-10-14 07:00:06", station=station, charge="2.70", vehicle=vehicle3)
        Pass.objects.create(id="BLE6733702", timestamp="2021-10-14 19:54:00", station=station, charge="3.20", vehicle=vehicle1)
        Pass.objects.create(id="BET6738704", timestamp="2021-10-14 16:00:43", station=station, charge="2.10", vehicle=vehicle2)

        station = "GF01"
        datefrom = "20211013"
        dateto = "20211017"
        format = "json"
        r = passesperstation(station,datefrom,dateto,format)
        #response = c.get('/interoperability/api/PassesPerStation/'+station+'/'+datefrom+'/'+dateto+'/')
        #r=response.json()
        self.maxDiff = None
        l = json.dumps(r["PassesList"])
        #self.assertEqual(response.status_code,200)
        self.assertEqual(12,r["NumberOfPasses"])
        self.assertEqual("GF01",r["Station"])
        self.assertEqual('[{"PassIndex": 1, "PassID": "BET6738704", "PassTimeStamp": "2021-10-14 16:00:43", "VehicleID": "EC05LZC49529", "TagProvider": "gefyra", "PassType": "home", "PassCharge": 2.1}, {"PassIndex": 2, "PassID": "BFE8738707", "PassTimeStamp": "2021-10-14 07:00:06", "VehicleID": "EC05LZC49521", "TagProvider": "moreas", "PassType": "visitor", "PassCharge": 2.7}, {"PassIndex": 3, "PassID": "BLE6733702", "PassTimeStamp": "2021-10-14 19:54:00", "VehicleID": "EC05LAC49528", "TagProvider": "aodos", "PassType": "visitor", "PassCharge": 3.2}, {"PassIndex": 4, "PassID": "BNR6736705", "PassTimeStamp": "2021-10-14 23:26:19", "VehicleID": "EC05LZC49529", "TagProvider": "gefyra", "PassType": "home", "PassCharge": 2.8}, {"PassIndex": 5, "PassID": "BWR6721702", "PassTimeStamp": "2021-10-15 01:32:12", "VehicleID": "EC05LAC49528", "TagProvider": "aodos", "PassType": "visitor", "PassCharge": 2.3}, {"PassIndex": 6, "PassID": "BYR6739702", "PassTimeStamp": "2021-10-14 00:05:13", "VehicleID": "EC05LZC49521", "TagProvider": "moreas", "PassType": "visitor", "PassCharge": 2.2}, {"PassIndex": 7, "PassID": "CET6738704", "PassTimeStamp": "2021-10-14 16:00:43", "VehicleID": "EC05LZC49529", "TagProvider": "gefyra", "PassType": "home", "PassCharge": 2.1}, {"PassIndex": 8, "PassID": "CFE8738707", "PassTimeStamp": "2021-10-14 07:00:06", "VehicleID": "EC05LZC49521", "TagProvider": "moreas", "PassType": "visitor", "PassCharge": 2.7}, {"PassIndex": 9, "PassID": "CLE6733702", "PassTimeStamp": "2021-10-14 19:54:00", "VehicleID": "EC05LAC49528", "TagProvider": "aodos", "PassType": "visitor", "PassCharge": 3.2}, {"PassIndex": 10, "PassID": "CNR6736705", "PassTimeStamp": "2021-10-14 23:26:19", "VehicleID": "EC05LZC49529", "TagProvider": "gefyra", "PassType": "home", "PassCharge": 2.8}, {"PassIndex": 11, "PassID": "CWR6721702", "PassTimeStamp": "2021-10-15 01:32:12", "VehicleID": "EC05LAC49528", "TagProvider": "aodos", "PassType": "visitor", "PassCharge": 2.3}, {"PassIndex": 12, "PassID": "CYR6739702", "PassTimeStamp": "2021-10-14 00:05:13", "VehicleID": "EC05LZC49528", "TagProvider": "engatia", "PassType": "visitor", "PassCharge": 2.2}]',l)

    def test_passesanalysis_big_in_cli(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        company1 = TollCompany.objects.create(name = "egnatia", abbr = "EG")
        company2 = TollCompany.objects.create(name = "gefyra", abbr = "GF")
        company3 = TollCompany.objects.create(name = "aodos", abbr = "AO")
        company4 = TollCompany.objects.create(name = "moreas", abbr = "MR")
        station = Station.objects.create(id="EG01", name="EG01", provider=company1)
        station1 = Station.objects.create(id="EG02", name="EG02", provider=company1)
        vehicle = Vehicle.objects.create(id="EC05SZC49518", tag_id="GF13892", license_year="2012", tag_provider=company2)
        vehicle4 = Vehicle.objects.create(id="EC02LZC46528", tag_id="EG13892", license_year="2012", tag_provider=company1)
        vehicle1 = Vehicle.objects.create(id="EC08LAC49528", tag_id="AO13892", license_year="2012", tag_provider=company3)
        vehicle2 = Vehicle.objects.create(id="EC01LZC41529", tag_id="GF13892", license_year="2012", tag_provider=company2)
        vehicle3 = Vehicle.objects.create(id="EC09LZC49521", tag_id="MR13892", license_year="2012", tag_provider=company4)
        Pass.objects.create(id="CER6528702", timestamp="2021-10-13 16:43:12", station=station, charge="2.20", vehicle=vehicle)
        Pass.objects.create(id="CER6738632", timestamp="2021-10-14 21:03:08", station=station1, charge="1.10", vehicle=vehicle)
        Pass.objects.create(id="CWR6721702", timestamp="2021-10-15 01:32:12", station=station, charge="2.30", vehicle=vehicle1)
        Pass.objects.create(id="CNR6736705", timestamp="2021-10-14 23:26:19", station=station1, charge="2.80", vehicle=vehicle)
        Pass.objects.create(id="CFE8738707", timestamp="2021-10-14 07:00:06", station=station1, charge="2.70", vehicle=vehicle1)
        Pass.objects.create(id="CLE6733702", timestamp="2021-10-14 19:54:00", station=station, charge="3.20", vehicle=vehicle1)
        Pass.objects.create(id="CET6738704", timestamp="2021-10-14 16:00:43", station=station1, charge="2.10", vehicle=vehicle2)
        Pass.objects.create(id="BYR6739702", timestamp="2021-10-14 00:05:13", station=station, charge="2.20", vehicle=vehicle)
        Pass.objects.create(id="BWR6721702", timestamp="2021-10-15 01:32:12", station=station1, charge="2.30", vehicle=vehicle1)
        Pass.objects.create(id="BNR6736705", timestamp="2021-10-14 23:26:19", station=station, charge="2.80", vehicle=vehicle2)
        Pass.objects.create(id="BFE8738707", timestamp="2021-10-14 07:00:06", station=station1, charge="2.70", vehicle=vehicle)
        Pass.objects.create(id="BLE6733702", timestamp="2021-10-14 19:54:00", station=station, charge="3.20", vehicle=vehicle1)
        Pass.objects.create(id="BET6738704", timestamp="2021-10-14 16:00:43", station=station1, charge="2.10", vehicle=vehicle)
        op1="EG"
        op2="GF"
        datefrom = "20211013"
        dateto = "20211017"
        format = "json"
        r = passesanalysis(op1,op2,datefrom,dateto,format)
        #response = c.get('/interoperability/api/PassesAnalysis/'+op1+'/'+op2+'/'+datefrom+'/'+dateto+'/')
        #r=response.json()
        self.maxDiff = None
        l = json.dumps(r["PassesList"])
        #self.assertEqual(response.status_code,200)
        self.assertEqual(8,r["NumberOfPasses"])
        self.assertEqual("EG",r["op1_ID"])
        self.assertEqual("GF",r["op2_ID"])
        self.assertEqual('[{"PassIndex": 1, "PassID": "BNR6736705", "StationID": "EG01", "PassTimeStamp": "2021-10-14 23:26:19", "VehicleID": "EC01LZC41529", "PassCharge": 2.8}, {"PassIndex": 2, "PassID": "BYR6739702", "StationID": "EG01", "PassTimeStamp": "2021-10-14 00:05:13", "VehicleID": "EC05SZC49518", "PassCharge": 2.2}, {"PassIndex": 3, "PassID": "CER6528702", "StationID": "EG01", "PassTimeStamp": "2021-10-13 16:43:12", "VehicleID": "EC05SZC49518", "PassCharge": 2.2}, {"PassIndex": 4, "PassID": "BET6738704", "StationID": "EG02", "PassTimeStamp": "2021-10-14 16:00:43", "VehicleID": "EC05SZC49518", "PassCharge": 2.1}, {"PassIndex": 5, "PassID": "BFE8738707", "StationID": "EG02", "PassTimeStamp": "2021-10-14 07:00:06", "VehicleID": "EC05SZC49518", "PassCharge": 2.7}, {"PassIndex": 6, "PassID": "CER6738632", "StationID": "EG02", "PassTimeStamp": "2021-10-14 21:03:08", "VehicleID": "EC05SZC49518", "PassCharge": 1.1}, {"PassIndex": 7, "PassID": "CET6738704", "StationID": "EG02", "PassTimeStamp": "2021-10-14 16:00:43", "VehicleID": "EC01LZC41529", "PassCharge": 2.1}, {"PassIndex": 8, "PassID": "CNR6736705", "StationID": "EG02", "PassTimeStamp": "2021-10-14 23:26:19", "VehicleID": "EC05SZC49518", "PassCharge": 2.8}]',l)

    def test_passescost_big_in_cli(self):

        company1 = TollCompany.objects.create(name = "egnatia", abbr = "EG")
        company2 = TollCompany.objects.create(name = "gefyra", abbr = "GF")
        company3 = TollCompany.objects.create(name = "aodos", abbr = "AO")
        company4 = TollCompany.objects.create(name = "moreas", abbr = "MR")
        station = Station.objects.create(id="EG01", name="EG01", provider=company1)
        station1 = Station.objects.create(id="EG02", name="EG02", provider=company1)
        vehicle = Vehicle.objects.create(id="EC05SZC49518", tag_id="GF13892", license_year="2012", tag_provider=company2)
        vehicle4 = Vehicle.objects.create(id="EC02LZC46528", tag_id="EG13892", license_year="2012", tag_provider=company1)
        vehicle1 = Vehicle.objects.create(id="EC08LAC49528", tag_id="AO13892", license_year="2012", tag_provider=company3)
        vehicle2 = Vehicle.objects.create(id="EC01LZC41529", tag_id="GF13892", license_year="2012", tag_provider=company2)
        vehicle3 = Vehicle.objects.create(id="EC09LZC49521", tag_id="MR13892", license_year="2012", tag_provider=company4)
        Pass.objects.create(id="CER6528702", timestamp="2021-10-13 16:43:12", station=station, charge="2.20", vehicle=vehicle)
        Pass.objects.create(id="CER6738632", timestamp="2021-10-14 21:03:08", station=station1, charge="1.10", vehicle=vehicle)
        Pass.objects.create(id="CWR6721702", timestamp="2021-10-15 01:32:12", station=station, charge="2.30", vehicle=vehicle1)
        Pass.objects.create(id="CNR6736705", timestamp="2021-10-14 23:26:19", station=station1, charge="2.80", vehicle=vehicle)
        Pass.objects.create(id="CFE8738707", timestamp="2021-10-14 07:00:06", station=station1, charge="2.70", vehicle=vehicle1)
        Pass.objects.create(id="CLE6733702", timestamp="2021-10-14 19:54:00", station=station, charge="3.20", vehicle=vehicle1)
        Pass.objects.create(id="CET6738704", timestamp="2021-10-14 16:00:43", station=station1, charge="2.10", vehicle=vehicle2)
        Pass.objects.create(id="BYR6739702", timestamp="2021-10-14 00:05:13", station=station, charge="2.20", vehicle=vehicle)
        Pass.objects.create(id="BWR6721702", timestamp="2021-10-15 01:32:12", station=station1, charge="2.30", vehicle=vehicle1)
        Pass.objects.create(id="BNR6736705", timestamp="2021-10-14 23:26:19", station=station, charge="2.80", vehicle=vehicle2)
        Pass.objects.create(id="BFE8738707", timestamp="2021-10-14 07:00:06", station=station1, charge="2.70", vehicle=vehicle)
        Pass.objects.create(id="BLE6733702", timestamp="2021-10-14 19:54:00", station=station, charge="3.20", vehicle=vehicle1)
        Pass.objects.create(id="BET6738704", timestamp="2021-10-14 16:00:43", station=station1, charge="2.10", vehicle=vehicle)

        op1="EG"
        op2="GF"
        datefrom = "20211013"
        dateto = "20211017"
        format = "json"
        r = passescost(op1,op2,datefrom,dateto,format)
        #response = c.get('/interoperability/api/PassesCost/'+op1+'/'+op2+'/'+datefrom+'/'+dateto+'/')
        #r=response.json()
        self.maxDiff = None
        l = json.dumps(r["PassesCost"])
        #self.assertEqual(response.status_code,200)
        self.assertEqual(8,r["NumberOfPasses"])
        self.assertEqual("EG",r["op1_ID"])
        self.assertEqual("GF",r["op2_ID"])
        self.assertEqual('18.0',l)

    def test_chagesbybig_in_cli(self):
        company1 = TollCompany.objects.create(name = "egnatia", abbr = "EG")
        company2 = TollCompany.objects.create(name = "gefyra", abbr = "GF")
        company3 = TollCompany.objects.create(name = "aodos", abbr = "AO")
        company4 = TollCompany.objects.create(name = "moreas", abbr = "MR")
        station = Station.objects.create(id="EG01", name="EG01", provider=company1)
        station1 = Station.objects.create(id="EG02", name="EG02", provider=company1)
        vehicle = Vehicle.objects.create(id="EC05SZC49518", tag_id="GF13892", license_year="2012", tag_provider=company2)
        vehicle4 = Vehicle.objects.create(id="EC02LZC46528", tag_id="EG13892", license_year="2012", tag_provider=company1)
        vehicle1 = Vehicle.objects.create(id="EC08LAC49528", tag_id="AO13892", license_year="2012", tag_provider=company3)
        vehicle2 = Vehicle.objects.create(id="EC01LZC41529", tag_id="GF13892", license_year="2012", tag_provider=company2)
        vehicle3 = Vehicle.objects.create(id="EC09LZC49521", tag_id="MR13892", license_year="2012", tag_provider=company4)
        Pass.objects.create(id="CER6528702", timestamp="2021-10-13 16:43:12", station=station, charge="2.20", vehicle=vehicle)
        Pass.objects.create(id="CER6738632", timestamp="2021-10-14 21:03:08", station=station1, charge="1.10", vehicle=vehicle)
        Pass.objects.create(id="CWR6721702", timestamp="2021-10-15 01:32:12", station=station, charge="2.30", vehicle=vehicle1)
        Pass.objects.create(id="CNR6736705", timestamp="2021-10-14 23:26:19", station=station1, charge="2.80", vehicle=vehicle)
        Pass.objects.create(id="CFE8738707", timestamp="2021-10-14 07:00:06", station=station1, charge="2.70", vehicle=vehicle1)
        Pass.objects.create(id="CLE6733702", timestamp="2021-10-14 19:54:00", station=station, charge="3.20", vehicle=vehicle1)
        Pass.objects.create(id="CET6738704", timestamp="2021-10-14 16:00:43", station=station1, charge="2.10", vehicle=vehicle2)
        Pass.objects.create(id="BYR6739702", timestamp="2021-10-14 00:05:13", station=station, charge="2.20", vehicle=vehicle)
        Pass.objects.create(id="BWR6721702", timestamp="2021-10-15 01:32:12", station=station1, charge="2.30", vehicle=vehicle1)
        Pass.objects.create(id="BNR6736705", timestamp="2021-10-14 23:26:19", station=station, charge="2.80", vehicle=vehicle2)
        Pass.objects.create(id="BFE8738707", timestamp="2021-10-14 07:00:06", station=station1, charge="2.70", vehicle=vehicle)
        Pass.objects.create(id="BLE6733702", timestamp="2021-10-14 19:54:00", station=station, charge="3.20", vehicle=vehicle1)
        Pass.objects.create(id="BET6738704", timestamp="2021-10-14 16:00:43", station=station1, charge="2.10", vehicle=vehicle)

        op1="EG"
        datefrom = "20211013"
        dateto = "20211017"
        format = "json"
        r = chargesby(op1,datefrom,dateto,format)
        #response = c.get('/interoperability/api/ChargesBy/'+op1+'/'+datefrom+'/'+dateto+'/')
        #r=response.json()
        self.maxDiff = None
        l = json.dumps(r["PPOList"])
        #self.assertEqual(response.status_code,200)
        self.assertEqual("EG",r["op_ID"])
        self.assertEqual('[{"VisitingOperator": "GF", "NumberOfPasses": 8, "PassesCost": 18.0}, {"VisitingOperator": "AO", "NumberOfPasses": 5, "PassesCost": 13.7}]',l)

    def test_settlementsbig_in_cli(self):
        company1 = TollCompany.objects.create(name = "egnatia", abbr = "EG")
        company2 = TollCompany.objects.create(name = "gefyra", abbr = "GF")
        company3 = TollCompany.objects.create(name = "aodos", abbr = "AO")
        company4 = TollCompany.objects.create(name = "moreas", abbr = "MR")
        station = Station.objects.create(id="EG01", name="EG01", provider=company1)
        station1 = Station.objects.create(id="EG02", name="EG02", provider=company1)
        vehicle = Vehicle.objects.create(id="EC05SZC49518", tag_id="GF13892", license_year="2012", tag_provider=company2)
        vehicle4 = Vehicle.objects.create(id="EC02LZC46528", tag_id="EG13892", license_year="2012", tag_provider=company1)
        vehicle1 = Vehicle.objects.create(id="EC08LAC49528", tag_id="AO13892", license_year="2012", tag_provider=company3)
        vehicle2 = Vehicle.objects.create(id="EC01LZC41529", tag_id="GF13892", license_year="2012", tag_provider=company2)
        vehicle3 = Vehicle.objects.create(id="EC09LZC49521", tag_id="MR13892", license_year="2012", tag_provider=company4)
        Pass.objects.create(id="CER6528702", timestamp="2021-10-13 16:43:12", station=station, charge="2.20", vehicle=vehicle)
        Pass.objects.create(id="CER6738632", timestamp="2021-10-14 21:03:08", station=station1, charge="1.10", vehicle=vehicle)
        Pass.objects.create(id="CWR6721702", timestamp="2021-10-15 01:32:12", station=station, charge="2.30", vehicle=vehicle1)
        Pass.objects.create(id="CNR6736705", timestamp="2021-10-14 23:26:19", station=station1, charge="2.80", vehicle=vehicle)
        Pass.objects.create(id="CFE8738707", timestamp="2021-10-14 07:00:06", station=station1, charge="2.70", vehicle=vehicle1)
        Pass.objects.create(id="CLE6733702", timestamp="2021-10-14 19:54:00", station=station, charge="3.20", vehicle=vehicle1)
        Pass.objects.create(id="CET6738704", timestamp="2021-10-14 16:00:43", station=station1, charge="2.10", vehicle=vehicle2)
        Pass.objects.create(id="BYR6739702", timestamp="2021-10-14 00:05:13", station=station, charge="2.20", vehicle=vehicle)
        Pass.objects.create(id="BWR6721702", timestamp="2021-10-15 01:32:12", station=station1, charge="2.30", vehicle=vehicle1)
        Pass.objects.create(id="BNR6736705", timestamp="2021-10-14 23:26:19", station=station, charge="2.80", vehicle=vehicle2)
        Pass.objects.create(id="BFE8738707", timestamp="2021-10-14 07:00:06", station=station1, charge="2.70", vehicle=vehicle)
        Pass.objects.create(id="BLE6733702", timestamp="2021-10-14 19:54:00", station=station, charge="3.20", vehicle=vehicle1)
        Pass.objects.create(id="BET6738704", timestamp="2021-10-14 16:00:43", station=station1, charge="2.10", vehicle=vehicle)

        op1="EG"
        format = "json"
        r = settlements(op1,format)
        l = json.dumps(r)
        self.assertEqual('[{"Operator": "GF", "Status": "They owe you", "Amount": 18.0}, {"Operator": "AO", "Status": "They owe you", "Amount": 13.7}, {"Operator": "MR", "Status": "You owe them", "Amount": 0.0}]',l)


    #----------------  CSV TESTS----------------#
    def test_passesperstation1_in_cli_csv(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        company1 = TollCompany.objects.create(name = "aodos", abbr = "AO")
        company2 = TollCompany.objects.create(name = "engatia", abbr = "EG")
        station = Station.objects.create(id="AO01", name="AO01", provider=company1)
        vehicle = Vehicle.objects.create(id="EC05LZC49528", tag_id="EG13892", license_year="2012", tag_provider=company2)
        Pass.objects.create(id="CER6738702", timestamp="2021-10-14 00:00:00", station=station, charge="2.20", vehicle=vehicle)
        station = "AO01"
        datefrom = "20211013"
        dateto = "20211017"
        format = "csv"
        r = passesperstation(station,datefrom,dateto,format)
        #response = c.get('/interoperability/api/PassesPerStation/'+station+'/'+datefrom+'/'+dateto+'/?format=csv')
        #r=response.content
        #self.assertEqual(response.status_code,200)
        self.assertEqual(b'CER6738702',r[76:86]) #PassID
        self.assertEqual(b'visitor',r[128:135]) #PassType
        self.assertEqual(b'2.2',r[136:139]) #PassCharge

    def test_passesanalysis1_in_cli_csv(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        company1 = TollCompany.objects.create(name = "egnatia", abbr = "EG")
        company2 = TollCompany.objects.create(name = "gefyra", abbr = "GF")
        station = Station.objects.create(id="EG01", name="EG01", provider=company1)
        station1 = Station.objects.create(id="EG02", name="EG02", provider=company1)
        vehicle = Vehicle.objects.create(id="EC05LZC49518", tag_id="GF13892", license_year="2012", tag_provider=company2)
        Pass.objects.create(id="CER6528702", timestamp="2021-10-13 16:43:12", station=station, charge="2.20", vehicle=vehicle)
        Pass.objects.create(id="CER6738632", timestamp="2021-10-14 21:03:08", station=station1, charge="1.10", vehicle=vehicle)
        format = "csv"
        op1="EG"
        op2="GF"
        datefrom = "20211013"
        dateto = "20211017"
        format = "csv"
        r = passesanalysis(op1,op2,datefrom,dateto,format)
        #response = self.client.get('/interoperability/api/PassesAnalysis/'+op1+'/'+op2+'/'+datefrom+'/'+dateto+'/?format=csv')
        #r=response.content
        self.maxDiff = None

        #self.assertEqual(response.status_code,200)
        self.assertEqual(b'EC05LZC49518',r[101:113]) #VehicleID
        self.assertEqual(b'EG01',r[76:80])      #StationID
        self.assertEqual(b'2.2',r[114:117])      #PassCharge

    def test_passescost1_in_cli_csv(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        company1 = TollCompany.objects.create(name = "egnatia", abbr = "EG")
        company2 = TollCompany.objects.create(name = "gefyra", abbr = "GF")
        station = Station.objects.create(id="EG01", name="EG01", provider=company1)
        station1 = Station.objects.create(id="EG02", name="EG02", provider=company1)
        vehicle = Vehicle.objects.create(id="EC05LZC49518", tag_id="GF13892", license_year="2012", tag_provider=company2)
        Pass.objects.create(id="CER6528702", timestamp="2021-10-13 16:43:12", station=station, charge="2.20", vehicle=vehicle)
        Pass.objects.create(id="CER6738632", timestamp="2021-10-14 21:03:08", station=station1, charge="1.10", vehicle=vehicle)
        op1="EG"
        op2="GF"
        datefrom = "20211013"
        dateto = "20211017"
        format = "csv"
        r = passescost(op1,op2,datefrom,dateto,format)
        #response = c.get('/interoperability/api/PassesCost/'+op1+'/'+op2+'/'+datefrom+'/'+dateto+'/?format=csv')
        #r=response.content
        self.maxDiff = None
        #self.assertEqual(response.status_code,200)
        self.assertEqual(b'EG',r[78:80]) #op1_ID
        self.assertEqual(b'2',r[126:127]) #NumberOfPasses
        self.assertEqual(b'3.3',r[128:131]) #PassesCost


    def test_chagesby1_in_cli_csv(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        company1 = TollCompany.objects.create(name = "egnatia", abbr = "EG")
        company2 = TollCompany.objects.create(name = "gefyra", abbr = "GF")
        company3 = TollCompany.objects.create(name = "aodos", abbr = "AO")
        station = Station.objects.create(id="EG01", name="EG01", provider=company1)
        station1 = Station.objects.create(id="EG02", name="EG02", provider=company1)
        vehicle = Vehicle.objects.create(id="EC05LZC49518", tag_id="GF13892", license_year="2012", tag_provider=company2)
        vehicle1 = Vehicle.objects.create(id="EC05LZC29518", tag_id="AO14892", license_year="2015", tag_provider=company3)
        Pass.objects.create(id="CER6528702", timestamp="2021-10-13 16:43:12", station=station, charge="2.20", vehicle=vehicle)
        Pass.objects.create(id="CER6738632", timestamp="2021-10-14 21:03:08", station=station1, charge="1.10", vehicle=vehicle1)
        op1="EG"
        datefrom = "20211013"
        dateto = "20211017"
        format = "csv"
        r = chargesby(op1,datefrom,dateto,format)
        #response = c.get('/interoperability/api/ChargesBy/'+op1+'/'+datefrom+'/'+dateto+'/?format=csv')
        #r=response.content
        self.maxDiff = None
        #self.assertEqual(response.status_code,200)
        self.assertEqual(b'GF',r[44:46]) #VisitingOperator
        self.assertEqual(b'1',r[47:48]) #NumberOfPasses
        self.assertEqual(b'2.2',r[49:52]) #PassesCost

    def test_settlements1_in_cli_csv(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        company1 = TollCompany.objects.create(name = "egnatia", abbr = "EG")
        company2 = TollCompany.objects.create(name = "gefyra", abbr = "GF")
        company3 = TollCompany.objects.create(name = "aodos", abbr = "AO")
        station = Station.objects.create(id="EG01", name="EG01", provider=company1)
        station1 = Station.objects.create(id="EG02", name="EG02", provider=company1)
        vehicle = Vehicle.objects.create(id="EC05LZC49518", tag_id="GF13892", license_year="2012", tag_provider=company2)
        vehicle1 = Vehicle.objects.create(id="EC05LZC29518", tag_id="AO14892", license_year="2015", tag_provider=company3)
        Pass.objects.create(id="CER6528702", timestamp="2021-10-13 16:43:12", station=station, charge="2.20", vehicle=vehicle)
        Pass.objects.create(id="CER6738632", timestamp="2021-10-14 21:03:08", station=station1, charge="1.10", vehicle=vehicle1)
        op1="EG"
        format = "csv"
        r = settlements(op1,format)
        self.maxDiff = None
        self.assertEqual(b'GF',r[24:26])
        self.assertEqual(b'They owe you',r[27:39])
        self.assertEqual(b'2.2',r[40:43])

        self.assertEqual(b'AO',r[45:47])
        self.assertEqual(b'They owe you',r[48:60])
        self.assertEqual(b'1.1',r[61:64])
