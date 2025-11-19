import nacl.public
import nacl.utils
import base64
import qrcode

from io import BytesIO

def generate_qr_code(config_text):
    img = qrcode.make(config_text)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

def generate_keypair():
    private = nacl.public.PrivateKey.generate()
    private_b64 = base64.b64encode(bytes(private)).decode()
    public_b64 = base64.b64encode(bytes(private.public_key)).decode()
    return private_b64, public_b64


def parse_used_ips(output):
    used = []
    for line in output.split("\n"):
        if "allowed-address" in line:
            try:
                ip = line.split("allowed-address=")[1]
                ip = ip.split("/")[0]
                used.append(ip)
            except:
                pass
    return used


def get_free_ip(used_ips, base="10.10.10."):
    for i in range(2, 255):
        ip = f"{base}{i}"
        if ip not in used_ips:
            return ip
    return None


def build_client_config(private_key, client_ip, server_pub, endpoint, dns):
    return f"""[Interface]
PrivateKey = {private_key}
Address = {client_ip}/32
DNS = {dns}

[Peer]
PublicKey = {server_pub}
AllowedIPs = 0.0.0.0/0
Endpoint = {endpoint}
PersistentKeepalive = 25
"""
