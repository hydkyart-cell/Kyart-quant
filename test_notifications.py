from notifications import TelegramNotifier

TOKEN = "8802692834:AAEeOZTnbrNXhtPOz6l_Ja1Z_w4MoVYwEc8"
CHAT_ID = 8543592519

bot = TelegramNotifier(TOKEN, CHAT_ID)

bot.send("🚀 Kyart Quant notification system is operational.")
