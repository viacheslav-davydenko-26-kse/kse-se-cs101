import hashlib
import base64

def get_hex_sha256(pin, salt="", iterations=100_000):
    return hashlib.pbkdf2_hmac("sha256", pin.encode(),
                               salt.encode(), iterations).hex()

weak_password = "password123"

db1_pass = get_hex_sha256(weak_password)
db2_pass = get_hex_sha256(weak_password)
print("db1_pass:", db1_pass)
print("db2_pass:", db2_pass)
print("Однакові?:", db1_pass == db2_pass)

print()

db3_secret_salt = "salt"
db3_pass = get_hex_sha256(weak_password, salt=db3_secret_salt)
db4_secret_salt = "salt"
db4_pass = get_hex_sha256(weak_password, salt=db4_secret_salt)
print("db3_pass:", db3_pass)
print("db4_pass:", db4_pass)
print("Однакові хеші?:", db3_pass == db4_pass)
print("Однакові солі?:", db3_secret_salt == db4_secret_salt)

print()

db5_secret_salt = "salt for 5"
db5_pass = get_hex_sha256(weak_password, salt=db5_secret_salt)
db6_secret_salt = "salt for 6"
db6_pass = get_hex_sha256(weak_password, salt=db6_secret_salt)
print("db5_pass:", db5_pass)
print("db6_pass:", db6_pass)
print("Однакові хеші?:", db5_pass == db6_pass)
print("Однакові солі?:", db5_secret_salt == db6_secret_salt)
