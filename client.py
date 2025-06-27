import requests

BASE_URL = "http://127.0.0.1:8000"

# Inserisci le tue credenziali superuser
USERNAME = "user1"
PASSWORD = "1234"

# 🔐 1. Ottieni il token
auth_response = requests.post(f"{BASE_URL}/api-token-auth/", data={
    "username": USERNAME,
    "password": PASSWORD
})
token = auth_response.json().get("token")
headers = {"Authorization": f"Token {token}"}
print("✅ Token:", token)

# 📊 2. Crea un sondaggio
poll = {"question": "Qual è il tuo colore preferito?"}
poll_resp = requests.post(f"{BASE_URL}/api/polls/", json=poll, headers=headers)
print("✅ Sondaggio creato:", poll_resp.json())

# 🔢 3. Aggiungi scelte
poll_id = poll_resp.json().get("id")
choice1 = {"poll": poll_id, "choice_text": "Blu"}
choice2 = {"poll": poll_id, "choice_text": "Rosso"}

requests.post(f"{BASE_URL}/api/choices/", json=choice1, headers=headers)
requests.post(f"{BASE_URL}/api/choices/", json=choice2, headers=headers)
print("✅ Scelte aggiunte")

# ✅ 4. Vota (supponendo che la choice con id 1 esista)
vote_data = {"poll": poll_id, "choice": 1}
vote_resp = requests.post(f"{BASE_URL}/api/vote/", json=vote_data, headers=headers)
print("✅ Voto registrato:", vote_resp.status_code)

# 📥 5. Recupera tutti i sondaggi (anche anonimo)
polls = requests.get(f"{BASE_URL}/api/polls/")
print("📋 Tutti i sondaggi:", polls.json())
