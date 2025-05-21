from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group


# Se vuoi personalizzare il modello utente:
class Utente(AbstractUser):
    # Campi obbligatori per sostituire username
    nome_utente = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)

    # Disabilita completamente il campo username
    username = None

    # Mantieni questi campi per evitare errori di clausole di autorizzazione
    groups = models.ManyToManyField(
        Group,
        related_name='utenti_gruppi',
        blank=True,
        help_text='I gruppi a cui appartiene questo utente.',
        verbose_name='gruppi',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='utenti_permessi',
        blank=True,
        help_text='I permessi specifici per questo utente.',
        verbose_name='permessi utente',
    )

    # Campi per l'autenticazione
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome_utente']

    # Aggiungi questi metodi per risolvere i conflitti
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field('email')._unique = True

    def natural_key(self):
        return (self.email,)

    def __str__(self):
        return self.nome_utente

class Gruppo(models.Model):
    nome = models.CharField(max_length=100)
    creatore = models.ForeignKey(Utente, on_delete=models.CASCADE, related_name='gruppi_creati')
    data_creazione = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class Partecipazione(models.Model):
    utente = models.ForeignKey(Utente, on_delete=models.CASCADE, related_name='partecipazioni')
    gruppo = models.ForeignKey(Gruppo, on_delete=models.CASCADE, related_name='partecipazioni')

    def __str__(self):
        return f"{self.utente.nome_utente} in {self.gruppo.nome}"


class Spesa(models.Model):
    gruppo = models.ForeignKey(Gruppo, on_delete=models.CASCADE, related_name='spese')
    utente_pagante = models.ForeignKey(Utente, on_delete=models.CASCADE, related_name='spese_pagante')
    causale = models.CharField(max_length=255)
    importo = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.causale} - {self.importo}€"


class Debito(models.Model):
    spesa = models.ForeignKey(Spesa, on_delete=models.CASCADE, related_name='debiti')
    utente_debitore = models.ForeignKey(Utente, on_delete=models.CASCADE, related_name='debiti')
    importo = models.DecimalField(max_digits=10, decimal_places=2)
    descrizione = models.TextField(blank=True)

    def __str__(self):
        return f"{self.utente_debitore.nome_utente} deve {self.importo}€ per {self.spesa.causale}"
