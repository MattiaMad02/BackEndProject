# 🗳️ Polling App – Crea, Vota e Visualizza Sondaggi

Benvenuto nella **Polling App**, una web app interattiva per creare sondaggi, votare e visualizzare risultati in tempo reale. Basata su **Django REST Framework** per il backend e **HTML + JavaScript** per il frontend.

---

## 📌 Funzionalità principali

### 👥 Utenti anonimi
- ✅ Visualizzano i sondaggi
- ✅ Visualizzano i risultati

### 🔐 Utenti registrati
- ✅ Tutte le funzionalità degli anonimi
- ✅ Registrazione/Login
- ✅ Creano sondaggi
- ✅ Modificano o eliminano i propri sondaggi
- ✅ Aggiungono scelte personalizzate
- Elenco utenti già registrati: user1(password:1234),user2(password:WA@GY@8shmQEt9p),user3(password:qwertyuiop),user4(password:zxcvbnm),user5(password:1234567890)
---

## 🧱 Struttura del progetto

### 📦 Backend (Django)
- **App `accounts`** – gestione utenti, token auth, profili con bio
- **App `polls`** – modelli `Poll`, `Choice`, `Vote`, API REST
- **Permessi** – Solo i creatori e il superuser(fondatore)possono modificare/eliminare

### 🌐 Frontend (HTML + JS)
- Interfaccia minimale per:
  - Registrazione e login
  - Creazione sondaggi
  - Votazione
  - Visualizzazione risultati (pubblica)
  - Modifica/eliminazione sondaggi (solo autore)
---

## ▶️ Come si usa

### 1. Registrazione
Compila il form con username, email e password. Ricevi un token di autenticazione.

### 2. Login
Inserisci le credenziali. Il token viene salvato e utilizzato per le richieste protette(dopo aver fatto il logout si refreshi la pagina).

### 3. Crea un sondaggio
Dopo il login, puoi inserire una domanda e almeno due scelte.(Gli id con i sondaggi sono:2,6,16,22,23,24. Dopo il 24 si possono creare nuovi sondaggi, i numeri nel mezzo sono sondaggi cancellati)

### 4. Vota
Inserisci l'ID di un sondaggio e seleziona una delle scelte.

### 5. Visualizza risultati
Chiunque può cliccare su "Mostra risultati" per vedere i voti aggiornati in tempo reale.

### 6. Modifica sondaggio
Il creatore può aggiornare la domanda e le scelte. I voti vengono azzerati.

### 7. Elimina sondaggio
Il creatore può cancellare completamente il sondaggio.
---

## 🔐 API principali

| Metodo | Endpoint                             | Descrizione                                 |
|--------|--------------------------------------|---------------------------------------------|
| POST   | `/api/register/`                     | Registrazione utente                        |
| POST   | `/api/login/`                        | Login utente (restituisce token)            |
| GET    | `/api/polls/`                        | Elenco di tutti i sondaggi                  |
| POST   | `/api/polls/`                        | Crea un nuovo sondaggio                     |
| PUT    | `/api/polls/<id>/`                   | Modifica un sondaggio esistente             |
| DELETE | `/api/polls/<id>/`                   | Elimina un sondaggio                        |
| POST   | `/api/choices/`                      | Aggiunge una nuova scelta a un sondaggio    |
| POST   | `/api/vote/`                         | Registra un voto per una scelta             |
| GET    | `/api/polls/<id>/results/`           | Mostra i risultati di un sondaggio          |

---
Link dashboard railway: https://railway.com/project/590ead3b-0a81-4e84-b1bb-d190f6bb8388/service/94ea2651-916a-4640-a1cb-2afc30e751ae?environmentId=f0f35f8f-024c-4d5f-aa1b-da927197d980
Link progetto railway: https://backendproject-production-637c.up.railway.app
