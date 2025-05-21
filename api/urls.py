# urls.py (dentro api/urls.py)
from django.urls import path
from . import views

urlpatterns = [
    path('registrazione/', views.registrazione),
    path('login/', views.login_view),
    path('gruppi/', views.crea_gruppo),
    path('gruppi/', views.gruppi_utente),
    path('gruppi/<int:id>/', views.dettaglio_gruppo),
    path('gruppi/<int:id>/membri/', views.membri_gruppo),
    path('uscita-gruppo/', views.uscita_gruppo),
    path('spese/', views.aggiungi_spesa),
    path('gruppi/<int:id>/spese/', views.spese_gruppo),
    path('spese/<int:id>/', views.elimina_spesa),
]

# settings.py
AUTH_USER_MODEL = 'api.Utente'