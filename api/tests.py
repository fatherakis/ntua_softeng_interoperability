from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.http import HttpResponse
from backend.models import Pass,Vehicle,Station,TollCompany
from datetime import datetime
from django.db.models import Sum

# API functional tests
class APIFunctionalTests(TestCase):
    def test_200 (self): # 200 success
        c = Client(HTTP_USER_AGENT='Mozilla/1.1')
        company = TollCompany.objects.create(name = "egnatia", abbr = "EG")
        station = Station.objects.create(id="EG01", name="EG01", provider=company)
        response = c.get('/interoperability/api/PassesPerStation/EG01/20000101/20211010/')
        self.assertEqual(response.status_code, 200)

    def test_all_pages_work (self): # all pages return 200 success
        c = Client(HTTP_USER_AGENT='Mozilla/1.1')
        company1 = TollCompany.objects.create(name = "egnatia", abbr = "EG")
        company2 = TollCompany.objects.create(name = "aodos", abbr = "AO")
        station = Station.objects.create(id="EG01", name="EG01", provider=company1)
        response = c.get('/interoperability/')
        self.assertEqual(response.status_code, 200)
        response = c.get('/interoperability/api/PassesPerStation/EG01/20000101/20211010/')
        self.assertEqual(response.status_code, 200)
        response = c.get('/interoperability/api/PassesAnalysis/EG/AO/20000101/20211010/')
        self.assertEqual(response.status_code, 200)
        response = c.get('/interoperability/api/PassesCost/EG/AO/20000101/20211010/')
        self.assertEqual(response.status_code, 200)
        response = c.get('/interoperability/api/ChargesBy/EG/20000101/20211010/')
        self.assertEqual(response.status_code, 200)
        response = c.get('/interoperability/api/Settlements/EG/')
        self.assertEqual(response.status_code, 200)

    def test_400 (self): # 400 bad request
        c = Client(HTTP_USER_AGENT='Mozilla/1.1')
        response = c.get('/interoperability/api/PassesPerStation/invalid/20000101/20211010/')
        self.assertEqual(response.status_code, 400)

    def test_invalidurl_404 (self): # 404 page not found
        c = Client(HTTP_USER_AGENT='Mozilla/1.1')
        response = c.get('/congratulations-you-just-won-an-iphone-11/')
        self.assertEqual(response.status_code, 404)

# --- apo edw kai katw de douleuoun gt den ta emfanizoume -------------------

#    def test_401 (self): # 401 no authorization
#        c = Client(HTTP_USER_AGENT='Mozilla/1.1')
#        response = c.get('/admin/healthcheck/')
#        self.assertEqual(response.status_code, 401)

#    def test_402 (self): # 402 no data
#        c = Client(HTTP_USER_AGENT='Mozilla/1.1')
#        company = TollCompany.objects.create(name = "egnatia", abbr = "EG")
#        station = Station.objects.create(id="EG01", name="EG01", provider=company)
#        response = c.get('/interoperability/api/PassesPerStation/EG01/20000101/20211010/')
#        self.assertEqual(response.status_code, 402)

#    def test_402 (self): # 402 no data
#            c = Client(HTTP_USER_AGENT='Mozilla/1.1')
#            company1 = TollCompany.objects.create(name = "egnatia", abbr = "EG")
#            company2 = TollCompany.objects.create(name = "aodos", abbr = "AO")
#            response = c.get('/interoperability/api/PassesCost/EG/AO/20000101/20211010/')
#            self.assertEqual(response.status_code, 402)

#    def test_500 (self): # 500 internal server error
#        c = Client(HTTP_USER_AGENT='Mozilla/1.1')
#        company1 = TollCompany.objects.create(name = "egnatia", abbr = "EG")
#        company2 = TollCompany.objects.create(name = "aodos", abbr = "AO")
#        station = Station.objects.create(id="EG01", name="EG01", provider=company1)
#        vehicle = Vehicle.objects.create(id="EC02LZC49528", tag_id="AO13892", license_year="2012", tag_provider=company2)
#        Pass.objects.create(id="AEL6739702", timestamp="2020-10-10 00:00:00", station=station, charge="2.20", vehicle=vehicle)
#        response = c.get('/interoperability/api/PassesPerStation/EG01/20500101/20211010/')
#        self.assertEqual(response.status_code, 500)
