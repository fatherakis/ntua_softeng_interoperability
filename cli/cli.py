#!/usr/bin/env python3

"""Interoperability cli app"""
import click
import requests
base = "https://localhost:9103/interoperability/api/"
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def format():
    return click.option(
        "--format",
        required=True,
        help="The format to be returned: json, csv"
)


@click.group()
def cli():
    pass


@cli.command()
def healthcheck():
    r = requests.get(base + "admin/healthcheck", verify=False)
    click.echo(r.content)
@cli.command()
def resetpasses():
    r = requests.post(base + "admin/resetpasses", verify=False)
    click.echo(r.content)
@cli.command()
def resetvehicles():
    r = requests.post(base + "admin/resetvehicles", verify=False)
    click.echo(r.content)
@cli.command()
def resetstations():
    r = requests.post(base + "admin/resetstations", verify=False)
    click.echo(r.content)




@cli.command()
@click.option(
    "--station",
    required=True,
    help="The station in question (format: XXYY)."
)
@click.option(
    "--datefrom",
    required=True,
    help="The initial date (format: YYYYMMDD)."
)
@click.option(
    "--dateto",
    required=True,
    help="The end date (format: YYYYMMDD)."
)
@format()
def passesperstation(station, datefrom, dateto, format):
    params = {"format": format}
    r = requests.get(
        base + "PassesPerStation/"
             + station + "/"
             + datefrom + "/"
             + dateto,
        params=params,
        verify=False
    )

    if r.status_code == 200:
        if format == "csv":
            click.echo(r.content)
        else:
            click.echo(r.json())

    else:
        click.echo(r)

@cli.command()
@click.option(
    "--op1",
    required=True,
    help="The company we are interested in."
)
@click.option(
    "--op2",
    required=True,
    help="The company from which tags come from."
)
@click.option(
    "--datefrom",
    required=True,
    help="The initial date (format: YYYYMMDD)."
)
@click.option(
    "--dateto",
    required=True,
    help="The end date (format: YYYYMMDD)."
)
@format()
def passesanalysis(op1, op2, datefrom, dateto, format):
    params = {"format": format}
    r = requests.get(
        base + "PassesAnalysis/"
             + op1 + "/" + op2 + "/"
             + datefrom + "/" + dateto,
        params = params,
        verify=False
    )

    if r.status_code == 200:
        if format == "csv":
            click.echo(r.content)
        else:
            click.echo(r.json())

    else:
        click.echo(r)


@cli.command()
@click.option(
    "--op1",
    required=True,
    help="The company we are interested in."
)
@click.option(
    "--op2",
    required=True,
    help="The company from which tags come from."
)
@click.option(
    "--datefrom",
    required=True,
    help="The initial date (format: YYYYMMDD)."
)
@click.option(
    "--dateto",
    required=True,
    help="The end date (format: YYYYMMDD)."
)
@format()
def passescost(op1, op2, datefrom, dateto, format):
    params = {"format": format}
    r = requests.get(
        base + "PassesCost/"
             + op1 + "/" + op2 + "/"
             + datefrom + "/" + dateto,
        params = params,
        verify=False
    )

    if r.status_code == 200:
        if format == "csv":
            click.echo(r.content)
        else:
            click.echo(r.json())

    else:
        click.echo(r)






@cli.command()
@click.option(
    "--op1",
    required=True,
    help="The company we are interested in."
)
@click.option(
    "--datefrom",
    required=True,
    help="The initial date (format: YYYYMMDD)."
)
@click.option(
    "--dateto",
    required=True,
    help="The end date (format: YYYYMMDD)."
)
@format()
def chargesby(op1, datefrom, dateto, format):
    params = {"format": format}
    r = requests.get(
        base + "ChargesBy/"
             + op1 + "/"
             + datefrom + "/" + dateto,
        params = params,
        verify=False
    )

    if r.status_code == 200:
        if format == "csv":
            click.echo(r.content)
        else:
            click.echo(r.json())

    else:
        click.echo(r)


@cli.command()
@click.option(
    "--op",
    required=True,
    help="The operator to compute the settlements for (format: XX)."
)
@format()
def settlements(op, format):
    params = {"format": format}
    r = requests.get(
        base + "Settlements/"
             + op + "/",
        params=params,
        verify=False
    )

    if r.status_code == 200:
        if format == "csv":
            click.echo(r.content)
        else:
            click.echo(r.json())

    else:
        click.echo(r)


@cli.command()
@click.option(
    "--passesupd",
    help="The end date (format: YYYYMMDD).",
    is_flag=True
)
@click.option(
    "--source",
    help="The end date (format: YYYYMMDD)."
)
def admin(passesupd, source):
    add_passes(source)


def add_passes(source):
    from os.path import dirname, abspath
    d = dirname(dirname(abspath(__file__))) 
    import sys
    sys.path.append(d)
    import os 
    os.chdir(d)
    print(os.getcwd())
    os.environ['DJANGO_SETTINGS_MODULE'] = 'interoperability.settings'
    import django
    django.setup()
    from backend.db_control import get_starting_passes

    try:
        get_starting_passes(source)
    except:
        return click.echo("Error")
    click.echo("Done")
