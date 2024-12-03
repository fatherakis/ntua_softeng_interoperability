from django.db import models
from django.db.models.deletion import CASCADE
from django.core.validators import MinLengthValidator, MinValueValidator


class TollCompany(models.Model):
    name = models.CharField(max_length=50)
    abbr = models.CharField(max_length=10)

    def __str__(self):
        return self.name


"""def pays_owes(pk1, pk2, amount, message):
    return TollCompany.objects.filter(pk=pk1) + str(message) +\
        str(amount) + " to " + TollCompany.objects.filter(pk=pk2)

#Some problems with 2 foreign keys i guess?
class Payment(models.Model):
    amount = models.DecimalField(decimal_places=2, max_digits=20)
    payment_details = models.TextField(blank=True)
    station_provider1 = models.ForeignKey(TollCompany,
        on_delete=CASCADE, related_name="payment_ower")
    station_provider2 = models.ForeignKey(TollCompany,
        on_delete=CASCADE, related_name="payment_receiver")

    def __str__(self):
        return pays_owes(self.station_provider1,
            self.station_provider2, self.amount, " paid")



class Settlement(models.Model):
    value_owed = models.DecimalField(decimal_places=2, max_digits=20)
    settlement_agreement = models.TextField()
    station_provider1 = models.ForeignKey(TollCompany,
        on_delete=CASCADE, related_name="settlement_ower")
    station_provider2 = models.ForeignKey(TollCompany,
        on_delete=CASCADE, related_name="settlement_receiver")

    def __str__(self):
        return pays_owes(self.station_provider1,
            self.station_provider2, self.value_owed, " owes")
"""


class Vehicle(models.Model):
    id = models.CharField(primary_key=True, max_length=12,
        validators=[MinLengthValidator(12)])
    tag_id = models.CharField(max_length=9,
        validators=[MinLengthValidator(9)])
    license_year = models.IntegerField(
        validators=[MinValueValidator(1886)])
    tag_provider = models.ForeignKey(TollCompany,
        on_delete=CASCADE, related_name="vehicles")

    def __str__(self):
        return "Car with ID: " + str(self.pk) + " of year: " +\
            str(self.license_year)


class Station(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=100)
    provider = models.ForeignKey(TollCompany,
    on_delete=CASCADE, related_name="StationsList")
    #^^^^^^^^^^^This is really important for the serializer of Station to
    #know how to get the list of stations related to an instance of it

    def __str__(self):
        return self.name

from django.db.models import Window, F
from django.db.models.functions import DenseRank
class Pass(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    timestamp = models.DateTimeField()
    station = models.ForeignKey(Station,
        on_delete=CASCADE, related_name="PassesList")
    charge = models.FloatField()
    vehicle = models.ForeignKey(Vehicle,
        on_delete=CASCADE, related_name="PassesList")

    def rank_and_annotate(PassesList, no=0):
        return PassesList.annotate(
            PassIndex=Window(expression=DenseRank(),
            order_by=F('id').asc() )+no)

    def pass_type(self):
        tag_prov = self.vehicle.tag_provider.pk
        station_prov = self.station.provider.pk
        if tag_prov == station_prov:
            return "home"
        return "visitor"

    def from_to(From, To, PassesList, of=None, no=0):
        passesQ = PassesList.filter(timestamp__gte=From)
        passesQ = passesQ.filter(timestamp__lte=To)

        if of:
            passesQ = passesQ.filter(
                vehicle__tag_provider__abbr__exact=of)

        return Pass.rank_and_annotate(passesQ, no)

    def __str__(self):
        return "Vehicle with ID" +  self.vehicle.pk +\
            " passed at: " + str(self.timestamp)
