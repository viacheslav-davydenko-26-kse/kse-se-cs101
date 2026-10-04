# Частина 4. Процеси й канали: як одна програма запускає іншу.
#
# ping і traceroute — це окремі програми, а не вбудовані можливості Python.
# Тут ви запустите їх зі свого коду й прочитаєте їхній вивід. Це рівно те, про
# що йшлося в лекції з ОС: один процес запускає інший, а спілкуються вони
# через канал (pipe) — ОС передає дочірньому процесу доступ до мережевої
# карти, а вам повертає його вивід.
#
# Це НЕ те, що робить браузер, коли відкриває сайт. ping і traceroute — це
# інструменти діагностики, які ви запускаєте самі, щоб роздивитися мережу.

import subprocess
import sys

# --- службовий блок, його чіпати не треба ---------------------------------
lines = []


def show(*args):
    text = " ".join(str(a) for a in args)
    print(text)
    lines.append(text)


def ping_command(host, count):
    """Складає команду ping під поточну операційну систему.

    Прапорці ping різні на Windows і на Unix, тому вибір роблено за
    sys.platform. Це вже написано — вам не треба цього чіпати.
      Windows:      ping -n <кількість> <хост>
      macOS/Linux:  ping -c <кількість> <хост>
    """
    if sys.platform.startswith("win"):
        return ["ping", "-n", str(count), host]
    return ["ping", "-c", str(count), host]


def run(command):
    """Запускає зовнішню програму й повертає (код_завершення, її_вивід).

    subprocess.run запускає ОКРЕМИЙ процес. capture_output=True під'єднує до
    нього канал і збирає весь його вивід; text=True віддає його як рядок.
    returncode 0 традиційно означає успіх (згадайте exit code з лекції).
    Помилку (програми немає, немає мережі) перехоплюємо, щоб скрипт не впав.
    """
    try:
        r = subprocess.run(command, capture_output=True, text=True,
                           timeout=30, encoding="utf-8", errors="replace")
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except FileNotFoundError:
        return None, "програму не знайдено: %s" % command[0]
    except subprocess.TimeoutExpired:
        return None, "перевищено час очікування"
    except OSError as e:
        return None, "помилка запуску: %s" % e.__class__.__name__
# --------------------------------------------------------------------------


import os
show("=== Хто я такий ===")
# Кожен процес має свій номер (PID). Це наш власний процес.
show("PID цього процесу:", os.getpid())


show("")
show("=== Запускаємо ping як окремий процес ===")
host = "example.com"
show("Команда:", " ".join(ping_command(host, 3)))
code, output = run(ping_command(host, 3))
show("Код завершення дочірнього процесу:", code)
show("--- вивід ping ---")
# Друкуємо лише перші кілька рядків виводу, щоб файл не роздувся.
for line in output.splitlines()[:8]:
    show(line)


# === ВПРАВА ==============================================================
# Запустіть traceroute до того самого хоста й покажіть код завершення та
# перші кілька рядків його виводу — так само, як зроблено для ping вище.
#
# Назва програми теж різна за системами, тому команду беріть таку:
#     Windows:      ["tracert", host]
#     macOS/Linux:  ["traceroute", host]
# Виберіть потрібний варіант через sys.platform.startswith("win"), як у
# функції ping_command. Далі викличте run(...) із цією командою і виведіть
# результат через show(). Кожен рядок виводу traceroute — це один вузол
# (маршрутизатор) на шляху пакета до сервера.
#
# Якщо traceroute на вашій системі не встановлено, run() поверне код None і
# повідомлення про це — цього достатньо, щоб показати, що ви спробували.
#
# Ваш код:


def tracerout_command(host):
    if sys.platform.startswith("win"):
        return ["tracert", host]
    return ["traceroute", host]

show("")
show("=== Запускаємо traceroute як окремий процес ===")
host = "example.com"
show("Команда:", " ".join(tracerout_command(host)))
code, output = run(tracerout_command(host))
show("Код завершення дочірнього процесу:", code)
show("--- вивід tracerout ---")
# Друкуємо лише перші кілька рядків виводу, щоб файл не роздувся.
for line in output.splitlines():
    show(line)


# --- збереження результату, чіпати не треба -------------------------------
with open("part4_output.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

print()
print("Готово. Результат збережено у файл part4_output.txt")
