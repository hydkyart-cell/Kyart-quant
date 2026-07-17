from notifications import TelegramNotifier

bot = TelegramNotifier()

response = bot.send("🟢 Kyart Quant Telegram test successful")

print(response)
