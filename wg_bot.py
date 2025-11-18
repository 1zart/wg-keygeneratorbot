import telebot
import base64
from nacl import bindings

BOT_TOKEN = "8255873011:AAG3-i0NBFgLVyNe6En1SJQrGGzZuJuJpOA"
bot = telebot.TeleBot(BOT_TOKEN)


def wg_generate_keys():
    # Private key 32 bytes
    private_key = bindings.crypto_box_keypair()[0]
    private_key_b64 = base64.b64encode(private_key).decode()

    # Public key = scalar multiplication
    public_key = bindings.crypto_scalarmult_base(private_key)
    public_key_b64 = base64.b64encode(public_key).decode()

    return private_key_b64, public_key_b64


@bot.message_handler(commands=['gen'])
def gen_handler(message):
    priv, pub = wg_generate_keys()

    bot.send_message(
        message.chat.id,
        f"PrivateKey: `{priv}`\nPublicKey: `{pub}`",
        parse_mode="Markdown"
    )


bot.polling()

