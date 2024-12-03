from django.urls import path
from . import views


urlpatterns = [
    #path("", views.index, name="index"),

    #path("login/", views.login, name="login"),
    #path("logout/", views.logout, name="logout"),

    path("PassesPerStation/<str:stationID>"\
    "/<int:date_from>/<int:date_to>/", views.passes_per_station,
    name="passes per station"),

    path("PassesAnalysis/<str:op1_ID>/<str:op2_ID>/<str:date_from>/"\
    "<str:date_to>/", views.passes_analysis, name="passes from "\
    "stations of op1 by cars with tag of op2"),

    path("PassesCost/<str:op1_ID>/<str:op2_ID>/<str:date_from>"\
    "/<str:date_to>/", views.passes_cost, name="how many passes "\
    "from stations of op1 by cars with tag of op2 & the total cost"),

    path("ChargesBy/<str:op_ID>/<str:date_from>/<str:date_to>/",
    views.charges_by, name="how many passes in op stations "\
    "from cars with other tags, and the amount owed from each prov"),

    path("Settlements/<str:op_ID>/",
    views.settlements, name="settlements"),
]
