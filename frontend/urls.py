from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="home"),

    path("PassesPerForm", views.PassesPerForm, name="PassesPerForm"),
    path("PassesAnalysisForm", views.PassesAnalysisForm, name="PassesAnalysisForm"),
    path("PassesCostForm", views.PassesCostForm, name="PassesCostForm"),
    path("ChargesByForm", views.ChargesByForm, name="ChargesByForm"),
    path("SettlementsForm", views.SettlementsForm, name="SettlementsForm"),

    path("PassesPerForm/fetch", views.PassesPerFetch, name="PassesPerFetch"),
    path("PassesAnalysisForm/fetch", views.PassesAnalysisFetch, name="PassesAnalysisFetch"),
    path("PassesCostForm/fetch", views.PassesCostFetch, name="PassesCostFetch"),
    path("ChargesByForm/fetch", views.ChargesByFetch, name="ChargesByFetch"),
    path("SettlementsForm/fetch", views.SettlementsFetch, name="SettlementsFetch"),
]
