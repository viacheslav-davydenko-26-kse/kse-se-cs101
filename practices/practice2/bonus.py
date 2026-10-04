import subprocess
import sys

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

def tracerout_command(host):
    if sys.platform.startswith("win"):
        return ["tracert", host]
    return ["traceroute", host]


# Перевіряємо різницю в часі ping між серверами
def test_time():
    def get_time_from_ping(output):
        lines = output.split("\n")
        time = "" 
        try:
            time = lines[1].split(" ")[-2]
            return float(time.split("=", 1)[-1]) 
        except:
            return -1 

    servers = [
        "kse.ua",
        "monobank.ua",
        "privatbank.ua",
        "github.com",
        "google.com",
        "cloudflare.com",
        "x.com",
    ]
    servers_pairs = []
    for i in range(len(servers)):
        for j in range(i + 1, len(servers)):
            server1 = servers[i]
            server2 = servers[j]
            servers_pairs.append((server1, server2))

    for server1, server2 in servers_pairs:
        code1, output1 = run(ping_command(server1, 1))
        code2, output2 = run(ping_command(server2, 1))
        time1 = get_time_from_ping(output1)
        time2 = get_time_from_ping(output2)
        
        output = "{} > {}, ({} ms > {} ms)"
        format_list = []
        if time1 > time2:
            format_list = [server1, server2, time1, time2]
        else:
            format_list = [server2, server1, time2, time1]

        output = output.format(*format_list)
        print(output)

def main():
    test_time()

if __name__ == "__main__":
    main()


