# Частина 3. Скільки коштує ОДНА спроба підбору.
#
# Ця частина працює на стандартній бібліотеці — жодних встановлень.
# Тут ви побачите, чому в частині 2 перебір пройшов за секунди, і що саме
# зробило б його безнадійним.

import hashlib
import time

# --- службовий блок, його чіпати не треба ---------------------------------
lines = []


def show(*args):
    text = " ".join(str(a) for a in args)
    print(text)
    lines.append(text)


def measure(make_key, attempts):
    """Скільки спроб за секунду встигає перебір із такою функцією ключа.

    make_key — функція, що з PIN робить ключ. attempts — скільки спроб
    зробити для заміру. Повертає кількість спроб за секунду.
    """
    start = time.perf_counter()
    for i in range(attempts):
        make_key("%06d" % i)
    spent = time.perf_counter() - start
    return attempts / spent


def naive_key(pin):
    """Те саме, що weak_key у частині 2: просто хеш, один прохід."""
    return hashlib.sha256(pin.encode()).digest()


def slow_key(pin, iterations):
    """PBKDF2: той самий SHA-256, але прогнаний тисячі разів поспіль."""
    return hashlib.pbkdf2_hmac("sha256", pin.encode(),
                               b"kse-cs101-practical-5", iterations)
# --------------------------------------------------------------------------


def sweep_seconds(rate, digits):
    """ВПРАВА 1. Скільки секунд триватиме перебір УСІХ PIN із digits цифр.

    Наприклад, шестизначних PIN існує 10 у шостому степені, тобто мільйон.
    Якщо перебір робить rate спроб за секунду, весь простір займе
    стільки-то секунд.

    Підказка: у Python степінь пишеться 10 ** digits.
    """
    # Приберіть рядок нижче і напишіть свій код.
    return 0.0


def human(seconds):
    """ВПРАВА 2. Переводить секунди в зручний для читання рядок.

    Правила такі:
      менше 60          -> "12 с"
      менше 3600        -> "5 хв"
      менше 86400       -> "7 год"
      інакше            -> "3 діб"

    Число округлюйте до цілого через round(). Зберіть рядок так, щоб у ньому
    були і число, і одиниця, розділені пробілом.
    """
    # Приберіть рядок нижче і напишіть свій код.
    return str(seconds)


if __name__ == "__main__":
    show("=== Вартість однієї спроби на ВАШІЙ машині ===")
    show("")
    show("%-20s %12s %14s %16s" % ("спосіб ключа", "спроб/с",
                                    "перебір 10^6", "один вхід у вас"))

    rate_naive = measure(naive_key, 20000)
    show("%-20s %12.0f %14s %16s"
         % ("просто sha256", rate_naive, human(sweep_seconds(rate_naive, 6)),
            "%.4f с" % (1 / rate_naive)))

    for iterations in (1000, 10000, 100000):
        rate = measure(lambda p: slow_key(p, iterations),
                       max(20, int(2000000 / iterations)))
        show("%-20s %12.0f %14s %16s"
             % ("PBKDF2 %d" % iterations, rate,
                human(sweep_seconds(rate, 6)), "%.4f с" % (1 / rate)))

    show("")
    show("=== Що дає довший PIN при НАЇВНОМУ ключі ===")
    for digits in (6, 8, 10, 12):
        show("  %2d цифр: %s" % (digits,
                                 human(sweep_seconds(rate_naive, digits))))

    show("")
    show("Тепер найважливіше. Подивіться на останню колонку першої таблиці:")
    show("скільки триває ОДИН чесний вхід із паролем. Порівняйте це з тим,")
    show("скільки коштує перебір. Потім подивіться на другу таблицю й")
    show("спитайте себе: чи погодяться люди запам'ятовувати PIN такої довжини?")
    show("Саме про це питання 5 і 6 у звіті.")

    with open("part3_output.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print()
    print("Готово. Результат збережено у файл part3_output.txt")
