import requests

TOKEN = "8802692834:AAEeOZTnbrNXhtPOz6l_Ja1Z_w4MoVYwEc8"
CHAT_ID = "8543592519"
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

data = {
    "chat_id": CHAT_ID,
    "text": "Kyart Quant is online 🚀"
}

r = requests.post(url, data=data)
print(r.text)
