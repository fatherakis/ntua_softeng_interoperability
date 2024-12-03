from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django import forms
from json2html import *
import requests
from .forms import Operators, Operator, Station

def index(request):
    """View function for home page of site."""
    # Render the HTML template index.html
    return render(request, 'index.html')

def PassesPerForm(request):
    station = Station().as_p()
    return render(request, 'passes_per_form.html',
        context={"station": station})

def PassesAnalysisForm(request):
    operators = Operators().as_p()
    return render(request, "passes_analysis_form.html",
        context={"operators": operators})

def PassesCostForm(request):
    operators = Operators().as_p()
    return render(request, "passes_cost_form.html",
        context={"operators": operators})

def ChargesByForm(request):
    operator = Operator().as_p()
    return render(request, "charges_by_form.html",
        context={"operator": operator})

def SettlementsForm(request):
    operator = Operator().as_p()
    return render(request, "settlements_form.html",
        context={"operator": operator})



def PassesPerFetch(request):
    if request.method == 'POST':
        get = (
            request.POST.get("station"),
            request.POST.get("from").replace("-", ""),
            request.POST.get("to").replace("-", "")
        )

        json = requests.get("https://localhost:9103"
        + "/interoperability/api/PassesPerStation/" + "/".join(get),
        verify=False).json()


        html_table = json2html.convert(json=json)
        return render(request, "base_detail.html", context={"table": html_table})

    else:
        return HttpResponseBadRequest("This is wrong")


def PassesAnalysisFetch(request):
    if request.method == 'POST':
        get = (
            request.POST.get("op1"),
            request.POST.get("op2"),
            request.POST.get("from").replace("-", ""),
            request.POST.get("to").replace("-", "")
        )

        json = requests.get("https://localhost:9103"
        + "/interoperability/api/PassesAnalysis/" + "/".join(get),
        verify=False).json()

        html_table = json2html.convert(json=json)
        return render(request, "base_detail.html", context={"table": html_table})

    else:
        return HttpResponseBadRequest("This is wrong")

def PassesCostFetch(request):
    if request.method == 'POST':
        get = (
            request.POST.get("op1"),
            request.POST.get("op2"),
            request.POST.get("from").replace("-", ""),
            request.POST.get("to").replace("-", "")
        )

        json = requests.get("https://localhost:9103"
        + "/interoperability/api/PassesCost/" + "/".join(get),
        verify=False).json()

        html_table = json2html.convert(json=json)
        return render(request, "base_detail.html", context={"table": html_table})

    else:
        return HttpResponseBadRequest("This is wrong")

def ChargesByFetch(request):
    print("Post data: " + str(request.POST))
    if request.method == 'POST':
        get = (
            request.POST.get("op"),
            request.POST.get("from").replace("-", ""),
            request.POST.get("to").replace("-", "")
        )

        json = requests.get("https://localhost:9103"
        + "/interoperability/api/ChargesBy/" + "/".join(get),
        verify=False).json()

        html_table = json2html.convert(json=json)
        return render(request, "base_detail.html", context={"table": html_table})

    else:
        return HttpResponseBadRequest("This is wrong")


def SettlementsFetch(request):
    if request.method == 'POST':
        operator = request.POST.get("op")

        json = requests.get("https://localhost:9103"
        + "/interoperability/api/Settlements/" + operator,
        verify=False).json()

        html_table = json2html.convert(json=json)
        return render(request, "base_detail.html", context={"table": html_table})

    else:
        return HttpResponseBadRequest("This is wrong")
