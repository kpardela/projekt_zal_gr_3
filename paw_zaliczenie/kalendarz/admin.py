from django.contrib import admin
from .models import Kategoria, Miejsce, Wydarzenie, Przypomnienie

admin.site.register(Kategoria)
admin.site.register(Miejsce)
admin.site.register(Wydarzenie)
admin.site.register(Przypomnienie)
