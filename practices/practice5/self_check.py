# Самоперевірка ПЕРЕД здачею.
#
#     python self_check.py
#
# Скрипт не ставить оцінку. Він перевіряє те саме, що й перевірка викладача,
# і каже, чого ще бракує. Доки тут є хоч один рядок «НЕ ГОТОВО» — зарано.

import hashlib
import os
import re
import sys

problems = []
lines = []


def show(mark, text):
    row = "%s %s" % (mark, text)
    print(row)
    lines.append(row)
    if mark == "НЕ ГОТОВО":
        problems.append(text)


def save():
    """Пишеться ЗАВЖДИ, зокрема й при виході на півдорозі."""
    with open("self_check_output.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def finish(message):
    print()
    print(message)
    save()
    sys.exit(0)


def read(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return ""


print("=== Самоперевірка роботи ===")
print()

for name in ("hashes.sh", "document.sha256", "hash_check.txt",
             "part2_crypto.py", "part3_cost.py", "report.md"):
    if os.path.exists(name):
        show("гаразд", "файл %s на місці" % name)
    else:
        show("НЕ ГОТОВО", "немає файлу %s" % name)

report = read("report.md")
m = re.search(r"Прізвище та ім'я[ \t]*:[ \t]*(.+)", report)
name = m.group(1).strip() if m else ""
if not name:
    show("НЕ ГОТОВО", "у report.md не вписано прізвище та ім'я")
    finish("Без прізвища частина 2 не працює — саме з нього виводиться PIN.")
show("гаразд", "прізвище у звіті: %s" % name)

# --- частина 1
check = read("hash_check.txt")
if ": OK" in check and ": FAILED" in check:
    show("гаразд", "у hash_check.txt є і OK, і FAILED")
else:
    show("НЕ ГОТОВО", "у hash_check.txt має бути і рядок OK, і рядок FAILED "
                      "(до зміни файлу й після неї)")
hashes = re.findall(r"(?im)^([0-9a-f]{64})\s", check, re.M)
if len(hashes) >= 2:
    same = sum(1 for a, b in zip(hashes[0], hashes[1]) if a == b)
    show("гаразд", "два хеші паролів на місці, спільних символів %d з 64" % same)
else:
    show("НЕ ГОТОВО", "у hash_check.txt бракує двох хешів схожих паролів")

# --- частина 2
out2 = read("part2_output.txt")
if not out2:
    show("НЕ ГОТОВО", "немає part2_output.txt — частину 2 не запущено")
elif "Немає бібліотеки cryptography" in out2:
    show("НЕ ГОТОВО", "cryptography не встановлено: pip install cryptography")
else:
    expected = "%06d" % (int(hashlib.sha256(name.lower().encode("utf-8"))
                             .hexdigest()[:8], 16) % 1000000)
    found = re.search(r"PIN знайдено:\s*(\d{6})", out2)
    if not found:
        show("НЕ ГОТОВО", "перебір не знайшов PIN — допишіть crack_naive")
    elif found.group(1) != expected:
        show("НЕ ГОТОВО", "знайдений PIN не відповідає вашому прізвищу — "
                          "можливо, secret.bin чужий")
    else:
        show("гаразд", "PIN %s знайдено перебором" % found.group(1))
    if not os.path.exists("secret.bin"):
        show("НЕ ГОТОВО", "немає secret.bin")

# --- частина 3
out3 = read("part3_output.txt")
if not out3:
    show("НЕ ГОТОВО", "немає part3_output.txt — частину 3 не запущено")
else:
    if re.search(r"PBKDF2 100000\s+\d+", out3):
        show("гаразд", "таблицю вартості спроби побудовано")
    else:
        show("НЕ ГОТОВО", "у part3_output.txt немає рядка PBKDF2 100000")
    if re.search(r"\d+\s*(с|хв|год|діб)\b", out3):
        show("гаразд", "час перебору переведено в читабельний вигляд")
    else:
        show("НЕ ГОТОВО", "вправи sweep_seconds / human не дописані")

# --- звіт
answers = re.split(r"\*\*Відповідь:\*\*", report)[1:]
filled = sum(1 for a in answers if len(a.split("\n#")[0].strip()) > 40)
if filled == 7:
    show("гаразд", "у звіті відповіді на всі 7 питань")
else:
    show("НЕ ГОТОВО", "у звіті заповнено %d питань із 7" % filled)

numbers = ["PIN, який ви знайшли перебором", "Скільки секунд тривав перебір",
           "Спроб за секунду з наївним ключем", "Спроб за секунду з PBKDF2"]
missing = [k for k in numbers
           if not re.search(re.escape(k) + r"[^:\n]*:[ \t]*\S", report)]
if missing:
    show("НЕ ГОТОВО", "у розділі «Мої числа» не заповнено: %d з %d"
         % (len(missing), len(numbers)))
else:
    show("гаразд", "розділ «Мої числа» заповнено")

# --- справжні секрети
leaks = []
for root, dirs, files in os.walk("."):
    # віртуальне середовище (.venv тощо) — чужі бібліотеки, не ваша робота;
    # у cryptography, наприклад, є рядок-заголовок SSH-ключа
    dirs[:] = [d for d in dirs
               if d not in ("__pycache__", ".git", ".venv", "venv", "env",
                            "site-packages", "node_modules")
               and not os.path.exists(os.path.join(root, d, "pyvenv.cfg"))]
    for f in files:
        if f.endswith((".txt", ".md", ".py", ".sh")):
            path = os.path.join(root, f)
            t = read(path)
            for pat in (r"ghp_[A-Za-z0-9]{10,}", r"AKIA[0-9A-Z]{12,}",
                        r"-----BEGIN [A-Z ]*PRIVATE KEY-----"):
                if re.search(pat, t):
                    leaks.append(os.path.relpath(path))
                    break
if leaks:
    show("НЕ ГОТОВО", "УВАГА: схоже на справжній ключ у файлах %s — приберіть"
         % ", ".join(sorted(set(leaks))))
else:
    show("гаразд", "справжніх ключів у роботі не знайдено")

print()
if problems:
    print("Не готово до здачі. Залишилося виправити: %d" % len(problems))
    for p in problems:
        print("   -", p)
else:
    print("Усе гаразд. Можна пакувати в zip і здавати.")
save()
