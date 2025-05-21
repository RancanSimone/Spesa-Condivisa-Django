# serializers.py
from rest_framework import serializers
from .models import Utente, Gruppo, Partecipazione, Spesa
from django.contrib.auth import authenticate

class UtenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utente
        fields = ['id', 'nome_utente', 'email']

class RegistrazioneSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Utente
        fields = ['nome_utente', 'email', 'password']
        extra_kwargs = {
            'email': {'required': True},
            'nome_utente': {'required': True},
        }

    def create(self, validated_data):
        utente = Utente(
            nome_utente=validated_data['nome_utente'],
            email=validated_data['email']
        )
        utente.set_password(validated_data['password'])
        utente.save()
        return utente

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(
            request=self.context.get('request'),
            email=data['email'],
            password=data['password']
        )
        if not user:
            raise serializers.ValidationError("Credenziali non valide")
        return user

class GruppoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gruppo
        fields = ['id', 'nome', 'creatore']

class GruppoDettaglioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gruppo
        fields = ['id', 'nome']

class PartecipazioneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partecipazione
        fields = ['id', 'utente', 'gruppo']

class SpesaSerializer(serializers.ModelSerializer):
    nomeUtente = serializers.CharField(source='utente_pagante.nome_utente', read_only=True)

    class Meta:
        model = Spesa
        fields = ['id', 'gruppo', 'utente_pagante', 'causale', 'importo', 'data', 'nomeUtente']