from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import ValidationError



STATUS_WYDARZENIA = (
    ("PLAN", "Planowane"),
    ("DONE", "Zrobione"),
    ("CANC", "Odwołane"),
)


PRIORYTET = (
    ("LOW", "Niski"),
    ("MED", "Średni"),
    ("HIGH", "Wysoki"),
)


class Kategoria(models.Model):
    """Model reprezentujący kategorię wydarzeń (np. Uczelnia, Praca, Prywatne)."""
    nazwa = models.CharField(max_length=50, help_text="Nazwa kategorii, np. Uczelnia.")
    opis = models.TextField(blank=True, help_text="Opis kategorii (opcjonalnie).")
    kolor = models.CharField(max_length=7, default="#000000", help_text="Kolor.")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, help_text="Użytkownik, do którego należy kategoria.")

    def __str__(self):
        return self.nazwa

    class Meta:
        ordering = ["nazwa"]
        verbose_name = "Kategoria"
        verbose_name_plural = "Kategorie"

    

class Miejsce(models.Model):
    """Model reprezentujący miejsce wydarzenia (opcjonalnie)."""
    nazwa = models.CharField(max_length=120, help_text="Nazwa miejsca, np. Dom, Uczelnia.")
    adres = models.CharField(max_length=255, blank=True, help_text="Adres (opcjonalnie).")
    notatki = models.TextField(blank=True, help_text="Dodatkowe informacje (opcjonalnie).")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, help_text="Użytkownik, do którego należy miejsce.")

    def __str__(self):
        return self.nazwa

    class Meta:
        ordering = ["nazwa"]
        verbose_name = "Miejsce"
        verbose_name_plural = "Miejsca"


class Wydarzenie(models.Model):
    """Model reprezentujący wydarzenie w kalendarzu."""
    tytul = models.CharField(max_length=120, help_text="Krótki tytuł, np. Kolokwium.")
    opis = models.TextField(blank=True, help_text="Opis wydarzenia (opcjonalnie).")

    start = models.DateTimeField(help_text="Data i godzina rozpoczęcia.")
    koniec = models.DateTimeField(help_text="Data i godzina zakończenia.")
    caly_dzien = models.BooleanField(default=False, help_text="Zaznacz, jeśli wydarzenie trwa cały dzień.")

    status = models.CharField(max_length=4, choices=STATUS_WYDARZENIA, default="PLAN", help_text="Status wydarzenia.")
    priorytet = models.CharField(max_length=4, choices=PRIORYTET, default="MED", help_text="Priorytet wydarzenia.")

    kategoria = models.ForeignKey(
        Kategoria, null=True, blank=True, on_delete=models.SET_NULL,
        help_text="Kategoria wydarzenia (opcjonalnie)."
    )
    miejsce = models.ForeignKey(
        Miejsce, null=True, blank=True, on_delete=models.SET_NULL,
        help_text="Miejsce wydarzenia (opcjonalnie)."
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE, help_text="Użytkownik, do którego należy wydarzenie.")
    data_utworzenia = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.tytul

    def save(self, *args, **kwargs):
        if self.start > self.koniec:
            raise ValidationError("Data rozpoczęcia nie moze byc po dacie zakończenia")
        super().save(*args, **kwargs)


    class Meta:
        ordering = ["start"] 
        verbose_name = "Wydarzenie"
        verbose_name_plural = "Wydarzenia"


class Przypomnienie(models.Model):
    """Model reprezentujący przypomnienie o wydarzeniu."""
    wydarzenie = models.ForeignKey(Wydarzenie, on_delete=models.CASCADE, help_text="Do jakiego wydarzenia.")
    kiedy = models.DateTimeField(help_text="Kiedy wysłać przypomnienie (data i godzina).")
    wiadomosc = models.CharField(max_length=200, blank=True, help_text="Treść przypomnienia (opcjonalnie).")
    wyslane = models.BooleanField(default=False, help_text="Czy przypomnienie zostało już wysłane.")

    def __str__(self):
        return f"Przypomnienie: {self.wydarzenie.tytul}"

    class Meta:
        ordering = ["kiedy"] 
        verbose_name = "Przypomnienie"
        verbose_name_plural = "Przypomnienia"
