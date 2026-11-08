import hashlib
import base64

def get_hex_sha256(pin, salt="", iterations=100_000):
    return hashlib.pbkdf2_hmac("sha256", pin.encode(),
                               salt.encode(), iterations).hex()

weak_password = "password123"
print(get_hex_sha256(weak_password))
print(get_hex_sha256(weak_password, salt="1"))
print(get_hex_sha256(weak_password, salt="2"))
print(get_hex_sha256(weak_password, salt="3"))
