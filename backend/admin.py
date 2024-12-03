#for admin page (database management etc)

from django.contrib import admin
from django.apps import apps

for obj in apps.all_models['backend'].values():
    try:
        admin.site.register(apps.all_models['backend'].values())
    except admin.sites.AlreadyRegistered:
        pass


