import os
import threading
import base64
from http.server import BaseHTTPRequestHandler, HTTPServer

import telebot
from nacl import bindings


BOT_TOKEN = "8255873011:AAG3-i0NBFgLVyNe6En1SJQrGGzZuJuJpOA"
bot = telebot.TeleBot(BOT_TOKEN)


def wg_generate_keys():
    private_key = bindings.crypto_box_keypair()[0]
    private_key_b64 = base64.b64encode(private_key).decode()

    public_key = bindings.crypto_scalarmult_base(private_key)
    public_key_b64 = base64.b64encode(public_key).decode()

    return private_key_b64, public_key_b64


@bot.message_handler(commands=['gen'])
def cmd_gen(message):
    priv, pub = wg_generate_keys()
    bot.send_message(
        message.chat.id,
        f"PrivateKey: `{priv}`\nPublicKey: `{pub}`",
        parse_mode="Markdown"
    )


# ---- HTTP сервер, чтобы Render видел порт ----
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"OK")


def run_server():
    port = int(os.environ.get("PORT", "10000"))
    httpd = HTTPServer(("0.0.0.0", port), HealthHandler)
    print(f"HTTP server running on port {port}")
    httpd.serve_forever()


if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    print("Bot polling started...")
    bot.polling()
