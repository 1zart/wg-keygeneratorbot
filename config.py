try:   
    from config_local import *
except ImportError:
   
    TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
    SSH_HOST = "10.10.10.1"
    SSH_PORT = 22
    SSH_USERNAME = "bot"
    SSH_PASSWORD = "Password"

    WG_INTERFACE = "wireguard1"
    WG_SUBNET = "10.10.10."
    WG_SERVER_PUBLIC = "SERVER_PUB_KEY_HERE"
    WG_ENDPOINT = "Server_address_or_domain:port"
    DNS = "1.1.1.1"

    ALLOWED_USER_ID = 123456789
