from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.http import HttpResponse
from backend.models import Pass,Vehicle,Station,TollCompany
from datetime import datetime
from django.db.models import Sum

# Back-end functional tests
class BackendFunctionalTests(TestCase):
    # Creation tests
    def test_company_creation (self): # creating one company, then counting them all
        TollCompany.objects.create(name = "egnatia", abbr = "EG")
        count = TollCompany.objects.count()
        self.assertEqual(count, 1)

    def test_station_creation (self): # creating one station, then counting them all
        company = TollCompany.objects.create(name = "egnatia", abbr = "EG")
        Station.objects.create(id="EG01", name="EG01", provider=company)
        count = Station.objects.count()
        self.assertEqual(count, 1)

    def test_vehicle_creation (self): # creating one vehicle, then counting them all
        company = TollCompany.objects.create(name = "egnatia", abbr = "EG")
        Vehicle.objects.create(id="EC02LZC49528", tag_id="AO13892", license_year="2012", tag_provider=company)
        count = Vehicle.objects.count()
        self.assertEqual(count, 1)

    def test_pass_creation (self): # creating one pass, then counting them all
        company = TollCompany.objects.create(name = "egnatia", abbr = "EG")
        station = Station.objects.create(id="EG01", name="EG01", provider=company)
        vehicle = Vehicle.objects.create(id="EC02LZC49528", tag_id="AO13892", license_year="2012", tag_provider=company)
        Pass.objects.create(id="AEL6739702", timestamp="2020-10-10 00:00:00", station=station, charge="2.20", vehicle=vehicle)
        count = Pass.objects.count()
        self.assertEqual(count, 1)

    # Parameter tests
    def test_pass_timestamp (self): # creating an old and a new pass, filtering to keep only the new one
        company = TollCompany.objects.create(name = "egnatia", abbr = "EG")
        station = Station.objects.create(id="EG01", name="EG01", provider=company)
        vehicle = Vehicle.objects.create(id="EC02LZC49528", tag_id="AO13892", license_year="2012", tag_provider=company)
        Pass.objects.create(id="OLDPASS", timestamp="2000-10-10 00:00:00", station=station, charge="2.20", vehicle=vehicle)
        Pass.objects.create(id="NEWPASS", timestamp="2022-02-02 00:00:00", station=station, charge="2.20", vehicle=vehicle)
        recent_passes = Pass.objects.filter(timestamp__gte='2022-01-01 00:00:00')
        count = recent_passes.count()
        self.assertEqual(count, 1)

    def test_pass_tag_provider (self):
        company1 = TollCompany.objects.create(name = "egnatia", abbr = "EG")
        company2 = TollCompany.objects.create(name = "aodos", abbr = "AO")
        station = Station.objects.create(id="EG01", name="EG01", provider=company1)
        vehicle1 = Vehicle.objects.create(id="firstone", tag_id="EG13892", license_year="2012", tag_provider=company1)
        vehicle2 = Vehicle.objects.create(id="secondone", tag_id="AO13896", license_year="2013", tag_provider=company2)
        Pass.objects.create(id="AEL6739702", timestamp="2020-10-10 00:00:00", station=station, charge="2.20", vehicle=vehicle1)
        Pass.objects.create(id="AEL6739703", timestamp="2020-10-10 00:01:32", station=station, charge="2.20", vehicle=vehicle2)
        egnatia_tag_passes = Pass.objects.filter(vehicle__tag_provider__abbr__exact=company1.abbr)
        count = egnatia_tag_passes.count()
        self.assertEqual(count, 1)
