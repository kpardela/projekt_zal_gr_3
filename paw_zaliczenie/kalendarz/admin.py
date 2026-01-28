from django.contrib import admin
from .models import Kategoria, Miejsce, Wydarzenie, Przypomnienie

class KategoriaAdmin(admin.ModelAdmin):
    list_display = ["nazwa", "kolor", "owner"]
    list_filter = ["owner"]
    search_fields = ["nazwa"]

class MiejsceAdmin(admin.ModelAdmin):
    list_display = ["nazwa", "adres", "owner"]
    list_filter = ["owner"]

class WydarzenieAdmin(admin.ModelAdmin):
    list_display = ["tytul", "start", "koniec", "status", "priorytet", "kategoria", "miejsce", "owner"]
    list_filter = ["status", "priorytet", "kategoria", "owner", "caly_dzien"]
    search_fields = ["tytul", "opis"]

    @admin.display(description="Kategoria (id)")
    def kategoria_z_id(self, obj):
        if obj.kategoria:
            return f"{obj.kategoria.nazwa} ({obj.kategoria.id})"
        return "-"

class PrzypomnienieAdmin(admin.ModelAdmin):
    list_display = ["wydarzenie", "kiedy", "wyslane"]
    list_filter = ["wyslane", "kiedy"]
    search_fields = ["wiadomosc", "wydarzenie__tytul"]

admin.site.register(Kategoria)
admin.site.register(Miejsce)
admin.site.register(Wydarzenie)
admin.site.register(Przypomnienie)
