@echo off
REM Avvia ngrok in una finestra separata
start "" ngrok http --url=admittedly-darling-stallion.ngrok-free.app 8000

REM Avvia Django
python manage.py runserver 0.0.0.0:8000
