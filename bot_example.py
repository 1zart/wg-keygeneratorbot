import telebot
from config import *
from ssh_mikrotik import ssh_run
from wg_utils import (
    generate_keypair,
    parse_used_ips,
    get_free_ip,
    build_client_config,
    generate_qr_code
)


ALLOWED_USER = 123456789

bot = telebot.TeleBot(TELEGRAM_TOKEN)


def check_access(msg):
    """Блокируем всех, кроме одного пользователя."""
    if msg.from_user.id != ALLOWED_USER:
        bot.send_message(msg.chat.id, "⛔ Доступ запрещён")
        return False
    return True


@bot.message_handler(commands=['start'])
def start(msg):
    if not check_access(msg):
        return

    bot.send_message(
        msg.chat.id,
        "Бот WireGuard готов.\nИспользуй команду:\n/new clientName"
    )


@bot.message_handler(commands=['new'])
def new_client(msg):
    if not check_access(msg):
        return

    parts = msg.text.split()
    if len(parts) != 2:
        bot.send_message(msg.chat.id, "Использование: /new clientName")
        return

    name = parts[1]

    #  peer list
    peers_out = ssh_run(
        SSH_HOST, SSH_PORT, SSH_USERNAME, SSH_PASSWORD,
        '/interface/wireguard/peers/print detail'
    )

    used_ips = parse_used_ips(peers_out)
    print("USED IPS:", used_ips)

    new_ip = get_free_ip(used_ips, WG_SUBNET)
    if not new_ip:
        bot.send_message(msg.chat.id, "❌ Нет свободных IP!")
        return

    
    private_key, public_key = generate_keypair()

    bot.send_message(msg.chat.id, f"🆕 Новый IP: {new_ip}\nГенерирую ключи…")

    # add peer
    cmd = (
        f'/interface/wireguard/peers/add interface={WG_INTERFACE} '
        f'public-key="{public_key}" allowed-address="{new_ip}/32" comment="{name}"'
    )

    bot.send_message(
        msg.chat.id,
        f"📡 Добавляю peer на MikroTik:\n\n<code>{cmd}</code>",
        parse_mode="HTML"
    )

    router_res = ssh_run(SSH_HOST, SSH_PORT, SSH_USERNAME, SSH_PASSWORD, cmd)

    # client config
    config_text = build_client_config(
        private_key=private_key,
        client_ip=new_ip,
        server_pub=WG_SERVER_PUBLIC,
        endpoint=WG_ENDPOINT,
        dns=DNS
    )

    bot.send_message(msg.chat.id, "<b>Готовый конфиг:</b>\n\n<pre>" +
                     config_text + "</pre>", parse_mode="HTML")

    # QR
    qr = generate_qr_code(config_text)
    bot.send_photo(msg.chat.id, qr, caption="QR-код WireGuard")


bot.polling(none_stop=True)
