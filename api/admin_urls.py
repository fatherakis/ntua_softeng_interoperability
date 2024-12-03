from django.urls import path
from . import admin_views

urlpatterns = [
    path("healthcheck", admin_views.healthcheck, name="healthcheck"),
    path("resetpasses", admin_views.resetpasses, name="reset passes"),
    path("resetstations", admin_views.resetstations, name="reset stations"),
    path("resetvehicles", admin_views.resetvehicles, name="reset vehicles"),
]