from dataclasses import fields
from .models import Kategoria, Miejsce, Wydarzenie, Przypomnienie
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


class KategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kategoria
        fields = ["id", "nazwa", "opis", "kolor", "owner"]
        read_only_fields = ["id"]

        validators = [
            UniqueTogetherValidator(
                queryset=Kategoria.objects.all(),
                fields=["owner", "nazwa"]
            )
        ]

    def validate_nazwa(self, value):
        if not value:
            raise serializers.ValidationError("Nazwa nie może być pusta.")
        if not value[0].isupper():
            raise serializers.ValidationError("Nazwa kategorii powinna zaczynać się wielką literą.")
        return value

class MiejsceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Miejsce
        fields = ["id", "nazwa", "adres", "notatki", "owner"]
        read_only_fields = ["id"]

        validators = [
            UniqueTogetherValidator(
                queryset=Miejsce.objects.all(),
                fields=["owner", "nazwa"]
            )
        ]

    def validate_nazwa(self, value):
        if not value:
            raise serializers.ValidationError("Nazwa nie może być pusta.")
        if not value[0].isupper():
            raise serializers.ValidationError("Nazwa miejsca powinna zaczynać się wielką literą.")
        return value

class WydarzenieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wydarzenie
        fields = [
            "id",
            "tytul",
            "opis",
            "start",
            "koniec",
            "caly_dzien",
            "status",
            "priorytet",
            "kategoria",
            "miejsce",
            "owner",
            "data_utworzenia",
        ]
        read_only_fields = ["id", "data_utworzenia"]

    def validate_tytul(self, value):
        if not value:
            raise serializers.ValidationError("Tytuł nie może być pusty.")
        if not value[0].isupper():
            raise serializers.ValidationError("Tytuł powinien zaczynać się wielką literą.")
        return value

    def validate(self, data):
        start = data.get("start")
        koniec = data.get("koniec")

        if start and koniec and koniec < start:
            raise serializers.ValidationError(
                {"koniec": "Data zakończenia nie może być wcześniejsza niż data rozpoczęcia."}
            )

        return data


class PrzypomnienieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Przypomnienie
        fields = ["id", "wydarzenie", "kiedy", "wiadomosc", "wyslane"]
        read_only_fields = ["id"]

    def validate(self, data):
        wydarzenie = data.get("wydarzenie")
        kiedy = data.get("kiedy")

        if wydarzenie and kiedy and wydarzenie.koniec and kiedy > wydarzenie.koniec:
            raise serializers.ValidationError(
                {"kiedy": "Przypomnienie nie może być ustawione po zakończeniu wydarzenia."}
            )

        return data
