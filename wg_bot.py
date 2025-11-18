import subprocess
import telebot
print("Bot started! Waiting for commands...")

BOT_TOKEN = "8255873011:AAG3-i0NBFgLVyNe6En1SJQrGGzZuJuJpOA"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=["gen"])
def gen_wg(message):
    priv = subprocess.check_output(["wg", "genkey"]).decode().strip()
    pub = subprocess.check_output(["wg", "pubkey"], input=priv.encode()).decode().strip()

    text = f"PrivateKey: `{priv}`\nPublicKey: `{pub}`"
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

bot.polling()
