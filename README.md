# 💸 Gestione Spese Condivise

Un'applicazione web per la gestione di gruppi, spese e debiti tra più utenti. Ogni utente può creare gruppi, aggiungere partecipanti, registrare spese, e tenere traccia di chi deve cosa.

---

## 🛠️ Tecnologie Utilizzate

### Backend
- Python 3.10+
- Django 4.x
- Django REST Framework
- MySQL (gestito tramite XAMPP)
- Ngrok (per esporre l'API in pubblico)

### API
- /api/registrazione/	POST	Registrazione utente
- /api/login/	POST	Login utente
- /api/gruppi/	POST	Crea un gruppo
- /api/gruppi/?utente=<id>	GET	Gruppi di un utente
- /api/gruppi/<id>/	GET	Info su un gruppo
- /api/gruppi/<id>/membri/	GET	Membri di un gruppo
- /api/uscita-gruppo/	POST	Uscita di un utente da gruppo
- /api/spese/	POST	Aggiunge una spesa
- /api/gruppi/<id>/spese/	GET	Spese di un gruppo
- /api/spese/<id>/	DELETE	Elimina una spesa

 # NGROK
 Per usare l'app anche da smartphone o da frontend remoto, esponi il backend con ngrok.

## Scarica ed installa ngrok
Vai su https://ngrok.com/download e scaricalo per il tuo sistema operativo.

- Estrai l’eseguibile ed esegui:
 " ngrok config add-authtoken 2xBfjVfgoEN8cxPH6s5ZqHhopFH_M6eXi2hS1eUxPmhkUzd "


- Avvia ngrok sulla porta 8000: 
  " ngrok http 8000 "
