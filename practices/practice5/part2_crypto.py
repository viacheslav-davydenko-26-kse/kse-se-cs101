# Частина 2. Справжнє шифрування AES — і чому воно не рятує саме по собі.
#
# ПОТРІБНА БІБЛІОТЕКА. Встановіть її один раз:
#     pip install cryptography
# Якщо команда дає помилку — прочитайте її й розберіться (див. методичку,
# Крок 0): це частина інженерної роботи, а не привід обійти.

import base64
import hashlib
import os
import re
import sys
import time

try:
    from cryptography.fernet import Fernet, InvalidToken
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
except ImportError:
    print("Немає бібліотеки cryptography.")
    print("Встановіть: pip install cryptography")
    print("Якщо команда дає помилку — розберіть її за підказками з методички "
          "(Крок 0), а не пропускайте частину.")
    sys.exit(0)

# --- службовий блок, його чіпати не треба ---------------------------------
lines = []


def show(*args):
    text = " ".join(str(a) for a in args)
    print(text)
    lines.append(text)


SALT = b"kse-cs101-practical-5"


def weak_key(pin):
    """НАЇВНИЙ спосіб: ключ — це просто хеш від PIN.

    Так робити не можна, і саме це ви зараз доведете власноруч.
    """
    return base64.urlsafe_b64encode(hashlib.sha256(pin.encode()).digest())


def strong_key(pin, iterations=100000):
    """ПРАВИЛЬНИЙ спосіб: ключ виводиться повільно, з сіллю.

    Той самий PIN, той самий AES — різниця лише в тому, скільки коштує
    ОДНА спроба підбору.
    """
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=SALT,
                     iterations=iterations)
    return base64.urlsafe_b64encode(kdf.derive(pin.encode()))


def my_pin():
    """PIN саме для вашої роботи — виводиться з вашого прізвища у report.md."""
    text = open("report.md", encoding="utf-8").read()
    m = re.search(r"Прізвище та ім'я[ \t]*:[ \t]*(.+)", text)
    name = (m.group(1).strip() if m else "")
    if not name:
        print("Спершу впишіть прізвище та ім'я у report.md")
        sys.exit(0)
    digest = hashlib.sha256(name.lower().encode("utf-8")).hexdigest()
    return "%06d" % (int(digest[:8], 16) % 1000000)


def make_secret():
    """Створює secret.bin, зашифрований НАЇВНИМ ключем від вашого PIN.

    Якщо файл уже є, але зашифрований іншим PIN (ви змінили прізвище після
    першого запуску), він перестворюється сам — щоб не лишалося чужого
    secret.bin, який потім не збігся б із вашим прізвищем.
    """
    message = ("Вітаю! Ви зламали шифр перебором. Це повідомлення було "
               "зашифроване справжнім AES — і це не допомогло.").encode("utf-8")
    if os.path.exists("secret.bin"):
        existing = open("secret.bin", "rb").read()
        try:
            Fernet(weak_key(my_pin())).decrypt(existing)
            return existing            # файл відповідає поточному прізвищу
        except InvalidToken:
            pass                       # чужий/застарілий — перестворюємо
    token = Fernet(weak_key(my_pin())).encrypt(message)
    with open("secret.bin", "wb") as f:
        f.write(token)
    return token
# --------------------------------------------------------------------------


def crack_naive(token):
    """ВПРАВА. Перебирає всі шестизначні PIN і повертає (pin, повідомлення).

    Якщо жоден не підійшов, поверніть (None, None).

    Як це робиться. Ідіть числом i від 0 до 999999. Перетворіть його на
    рядок рівно з шести цифр — це робить "%06d" % i. Для кожного такого PIN
    зберіть ключ через weak_key і спробуйте розшифрувати:

        Fernet(weak_key(pin)).decrypt(token)

    Якщо PIN не той, цей виклик кине виняток InvalidToken — його треба
    перехопити через try/except і просто йти далі. Якщо ж PIN правильний,
    ви отримаєте байти; переведіть їх у текст через .decode("utf-8") і
    поверніть разом із PIN.
    """
    # Приберіть рядок нижче і напишіть свій код.
    return None, None


if __name__ == "__main__":
    show("=== Дослід 1. Шифрування працює ===")
    secret_text = "Мій особистий рядок для перевірки шифрування."
    token = Fernet(strong_key("482913")).encrypt(secret_text.encode("utf-8"))
    show("Зашифровано, довжина токена:", len(token), "байтів")
    show("Розшифровано правильним PIN:",
         Fernet(strong_key("482913")).decrypt(token).decode("utf-8"))
    try:
        Fernet(strong_key("000000")).decrypt(token)
        show("ПОМИЛКА: розшифрувалося чужим PIN")
    except InvalidToken:
        show("Чужий PIN дав InvalidToken — саме так і має бути.")
    show("")

    show("=== Дослід 2. Ламаємо наївний ключ ===")
    token = make_secret()
    show("Файл secret.bin створено з вашого прізвища. PIN ви не знаєте.")
    start = time.perf_counter()
    pin, message = crack_naive(token)
    spent = time.perf_counter() - start
    if pin is None:
        show("Перебір нічого не знайшов — допишіть crack_naive.")
    else:
        show("PIN знайдено:", pin)
        show("Часу витрачено: %.1f с" % spent)
        show("Повідомлення:", message)
    show("")

    show("Чому це спрацювало так швидко — і що зупинило б перебір —")
    show("ви поміряєте власноруч у частині 3.")

    with open("part2_output.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print()
    print("Готово. Результат збережено у файл part2_output.txt")
