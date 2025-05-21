# views.py
from rest_framework import status, generics, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import login
from .models import Utente, Gruppo, Partecipazione, Spesa
from .serializers import *
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Utente

@api_view(['POST'])
@permission_classes([AllowAny])
def registrazione(request):
    serializer = RegistrazioneSerializer(data=request.data)
    if serializer.is_valid():
        print("VALIDATED DATA:", serializer.validated_data)
        utente = serializer.save()
        return Response({
            "success": True,
            "id": utente.id,
            "nomeUtente": utente.nome_utente,
            "email": utente.email
        })
    else:
        print("ERRORI VALIDAZIONE:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.contrib.auth import authenticate


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get('email').lower().strip()  # Normalizza l'email
    password = request.data.get('password')

    user = authenticate(request, email=email, password=password)

    if user is not None:
        return Response({
            "id": user.id,
            "nomeUtente": user.nome_utente,
            "email": user.email
        })
    else:
        # Debug avanzato
        from .models import Utente
        if Utente.objects.filter(email=email).exists():
            return Response({"error": "Password errata"}, status=401)
        else:
            return Response({"error": "Email non registrata"}, status=401)


@api_view(['POST'])
@permission_classes([AllowAny])
def crea_gruppo(request):
    nome = request.data.get('nome')
    id_utente = request.data.get('id_utente')
    creatore = Utente.objects.get(id=id_utente)
    gruppo = Gruppo.objects.create(nome=nome, creatore=creatore)
    Partecipazione.objects.create(gruppo=gruppo, utente=creatore)
    return Response({"id": gruppo.id, "nome": gruppo.nome, "membri": [id_utente]})

@api_view(['GET'])
@permission_classes([AllowAny])
def gruppi_utente(request):
    id_utente = request.GET.get('utente')
    gruppi = Gruppo.objects.filter(partecipazione__utente=id_utente).distinct()
    return Response(GruppoDettaglioSerializer(gruppi, many=True).data)

@api_view(['GET'])
@permission_classes([AllowAny])
def dettaglio_gruppo(request, id):
    gruppo = Gruppo.objects.get(id=id)
    return Response(GruppoDettaglioSerializer(gruppo).data)

@api_view(['GET'])
@permission_classes([AllowAny])
def membri_gruppo(request, id):
    membri = Utente.objects.filter(partecipazione__gruppo=id)
    return Response(UtenteSerializer(membri, many=True).data)

@api_view(['POST'])
@permission_classes([AllowAny])
def uscita_gruppo(request):
    id_gruppo = request.data.get('id_gruppo')
    id_utente = request.data.get('id_utente')
    Partecipazione.objects.filter(gruppo_id=id_gruppo, utente_id=id_utente).delete()
    return Response({"success": True})

@api_view(['POST'])
@permission_classes([AllowAny])
def aggiungi_spesa(request):
    serializer = SpesaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([AllowAny])
def spese_gruppo(request, id):
    spese = Spesa.objects.filter(gruppo_id=id)
    return Response(SpesaSerializer(spese, many=True).data)

@api_view(['DELETE'])
@permission_classes([AllowAny])
def elimina_spesa(request, id):
    try:
        spesa = Spesa.objects.get(id=id)
        spesa.delete()
        return Response({"success": True})
    except Spesa.DoesNotExist:
        return Response(status=404)