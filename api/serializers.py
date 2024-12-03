from rest_framework import serializers
from backend.models import Pass, Station, TollCompany
from django.db.models import Window, F
from django.db.models.functions import DenseRank
from datetime import datetime
from decimal import Decimal, getcontext


class PassPSS(serializers.ModelSerializer):
    PassIndex = serializers.IntegerField()
    PassID = serializers.CharField(source="id")
    PassTimeStamp = serializers.CharField(source="timestamp")
    VehicleID = serializers.PrimaryKeyRelatedField(
        source="vehicle", read_only=True)
    TagProvider = serializers.SerializerMethodField()
    PassType = serializers.SerializerMethodField()
    PassCharge = serializers.FloatField(source="charge")

    def get_TagProvider(self, obj):
        return obj.vehicle.tag_provider.name
    def get_PassType(self, obj):
        return obj.pass_type()

    class Meta:
        model = Pass
        fields = ["PassIndex", "PassID", "PassTimeStamp",
        "VehicleID", "TagProvider", "PassType", "PassCharge",]


class StationSerializer(serializers.ModelSerializer):
    Station = serializers.CharField(source="id")
    StationOperator = serializers.SerializerMethodField()
    RequestTimestamp = serializers.SerializerMethodField()
    PeriodFrom = serializers.SerializerMethodField()
    PeriodTo = serializers.SerializerMethodField()
    NumberOfPasses = serializers.SerializerMethodField()
    PassesList =  serializers.SerializerMethodField()

    def get_StationOperator(self, obj):
        return self.context["StationOperator"]
    def get_RequestTimestamp(self, obj):
        return self.context["RequestTimestamp"]
    def get_PeriodFrom(self, obj):
        dt = self.context["From"]
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    def get_PeriodTo(self, obj):
        dt = self.context["To"]
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    def get_PassesList(self, obj):
        passesQ = Pass.from_to(self.context["From"],
            self.context["To"], obj.PassesList)
        return PassPSS(passesQ, many=True).data
    def get_NumberOfPasses(self, obj):
        passesQ = Pass.from_to(self.context["From"],
            self.context["To"], obj.PassesList)
        return passesQ.count()

    class Meta:
        model = Station
        fields = ["Station", "StationOperator",
            "RequestTimestamp", "PeriodFrom",
            "PeriodTo", "NumberOfPasses",
            "PassesList",]


class PassAnalysis(serializers.ModelSerializer):
    PassIndex = serializers.IntegerField()
    PassID = serializers.CharField(source="id")
    PassTimeStamp = serializers.CharField(source="timestamp")
    VehicleID = serializers.PrimaryKeyRelatedField(
        source="vehicle", read_only=True)
    PassCharge = serializers.FloatField(source="charge")
    StationID = serializers.SerializerMethodField()
    def get_StationID(self,obj):
        return obj.station.id
    class Meta:
        model = Pass
        fields = ["PassIndex", "PassID","StationID","PassTimeStamp",
        "VehicleID","PassCharge",]

class TollAnalysisSerializer(serializers.ModelSerializer):
    op1_ID = serializers.CharField(source="abbr")
    RequestTimestamp = serializers.SerializerMethodField()
    PeriodFrom = serializers.SerializerMethodField()
    PeriodTo = serializers.SerializerMethodField()
    op2_ID = serializers.SerializerMethodField()
    PassesList = serializers.SerializerMethodField()
    NumberOfPasses = serializers.SerializerMethodField()

    def get_RequestTimestamp(self, obj):
        return self.context["RequestTimestamp"]
    def get_PeriodFrom(self, obj):
        dt = self.context["From"]
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    def get_PeriodTo(self, obj):
        dt = self.context["To"]
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    def get_op2_ID(self,obj):
        return self.context["Of"]
    def get_PassesList(self, obj):
        all_stations = obj.StationsList.all()
        full_list = []
        no = 0
        for station in all_stations:
            passes_of_station = PassAnalysis(Pass.from_to(
                self.context["From"], self.context["To"],
                station.PassesList, of=self.context["Of"],  no=no), many=True)
            full_list += passes_of_station.data
            no = len(full_list)
        return full_list
    def get_NumberOfPasses(self, obj):
        all_stations = obj.StationsList.all()
        full_list = []
        no = 0
        for station in all_stations:
            passes_of_station = PassAnalysis(Pass.from_to(
                self.context["From"], self.context["To"],
                station.PassesList, of=self.context["Of"], no=no), many=True)
            full_list += passes_of_station.data
        return len(full_list)

    class Meta:
        model = TollCompany
        fields = ["op1_ID", "op2_ID",
            "RequestTimestamp", "PeriodFrom",
            "PeriodTo", "NumberOfPasses",
            "PassesList",]
# ---------------------------------------------------
# PassesCost Serializer starts here
class PassesCostSerializer(serializers.Serializer):
    op1_ID = serializers.CharField()
    op2_ID = serializers.CharField()
    RequestTimestamp = serializers.DateTimeField()
    PeriodFrom = serializers.DateTimeField()
    PeriodTo = serializers.DateTimeField()
    NumberOfPasses = serializers.IntegerField()
    PassesCost = serializers.FloatField()

#-----------------------------------------------------

#<------------ Internal Serializers for ChargesBy Start Here --------------->
#PassAnalysisSerializer duplicate minimized for internal use Dont Touch pls
class PassAnalysisCharges(serializers.ModelSerializer):
    TagProvider = serializers.SerializerMethodField()
    PassCharge = serializers.FloatField(source="charge")
    def get_TagProvider(self, obj):
        return obj.vehicle.tag_provider.abbr
    class Meta:
        model = Pass
        fields = ["TagProvider","PassCharge"]

#ChargeSerializer takes our Lists with (company_name, number, cost) and serializes accordingly
class ChargeSerializer(serializers.Serializer):
    VisitingOperator = serializers.SerializerMethodField()
    NumberOfPasses = serializers.SerializerMethodField()
    PassesCost = serializers.SerializerMethodField()
    def get_VisitingOperator(self,obj):
        return obj[0]
    def get_NumberOfPasses(self,obj):
        return obj[1]
    def get_PassesCost(self,obj):
        return obj[2]

    class Meta:
        fields = ["VisitingOperator","NumberOfPasses","PassesCost"]

#<------------ Internal Serializers for ChargesBy End Here --------------->
class ChargesBySerializer(serializers.ModelSerializer):
    op_ID = serializers.CharField(source="abbr")
    RequestTimestamp = serializers.SerializerMethodField()
    PeriodFrom = serializers.SerializerMethodField()
    PeriodTo = serializers.SerializerMethodField()
    PPOList = serializers.SerializerMethodField()

    def get_RequestTimestamp(self, obj):
        return self.context["RequestTimestamp"]
    def get_PeriodFrom(self, obj):
        dt = self.context["From"]
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    def get_PeriodTo(self, obj):
        dt = self.context["To"]
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    def get_PPOList(self, obj):
        #all_companies fetches every TollCompany object except the one calling it
        all_companies = TollCompany.objects.exclude(name__exact=obj.name)
        #companies_list is a list of the companies names
        companies_list = []

        for comp in all_companies:
            companies_list.append(comp.abbr)

        #The thought proccess is for each station of our company,
        #we fetch the passes of the rest of the companies and save them as a whole
        #into full_passes_list
        all_stations = obj.StationsList.all()
        full_passes_list = []

        for station in all_stations:
            for comp in companies_list:
                passes_of_station = PassAnalysisCharges(Pass.from_to(
                    self.context["From"], self.context["To"],
                    station.PassesList, of=comp, no=0),many=True)
                full_passes_list += passes_of_station.data
        #Make a list of the companies that had ID's pass from us in the given timeframe


        passed_companies = []
        for p in full_passes_list:
            if p["TagProvider"] in passed_companies:
                pass
            else:
                passed_companies.append(p["TagProvider"])

        #Initialize a List containing Lists for each return item
        Specs_List=[]
        for i in range(len(passed_companies)):
            Specs_List.append([])

        #Each list inside our list contains the name of the Company that passed
        for i, comp in enumerate(passed_companies):
            Specs_List[i].append(comp)

        getcontext().Emin = -2
        for i in range(len(passed_companies)):
            #Initialize the NumberOfPasses and the charges for each company
            count = 0
            charge = Decimal("0.00")
            for o in range(len(full_passes_list)):
                #Scan through all the passes and increase count and charges
                #when a pass matches the company
                if full_passes_list[o]["TagProvider"] in Specs_List[i]:
                    count += 1
                    charge += Decimal(full_passes_list[o]["PassCharge"])
                else:
                    pass

            Specs_List[i].append(count)
            Specs_List[i].append(float(round(charge, 2)))

        #Call a serializer to Format our list according to specifications
        Formated_data = ChargeSerializer(Specs_List,many=True).data
        return Formated_data


    class Meta:
        model = TollCompany
        fields = ["op_ID",
            "RequestTimestamp", "PeriodFrom",
            "PeriodTo",
            "PPOList",]

class SettlementsSerializer(serializers.Serializer):
    Operator = serializers.CharField()
    Status  = serializers.CharField()
    Amount = serializers.FloatField()
