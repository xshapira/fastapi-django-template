from django.contrib import admin

from cities.models import City, Company, Language, Programmer

admin.site.register(City)
admin.site.register(Company)
admin.site.register(Language)
admin.site.register(Programmer)
