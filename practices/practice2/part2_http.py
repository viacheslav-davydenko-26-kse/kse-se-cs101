# Частина 2. HTTP власноруч: розмова з сайтом звичайним текстом.
#
# Браузер, відкриваючи сторінку, надсилає серверу простий текстовий запит і
# отримує таку саму текстову відповідь. Тут ви зробите це самі: складете
# запит із рядків, відправите його в сокет і розберете відповідь на частини.
#
# Правило цієї частини: усередині своїх функцій розбору НЕ можна користуватися
# готовими бібліотеками http/urllib. Ми саме й дивимося, з чого протокол
# складається насправді.

# --- службовий блок, його чіпати не треба ---------------------------------
lines = []


def show(*args):
    text = " ".join(str(a) for a in args)
    print(text)
    lines.append(text)


# Збережена справжня відповідь сервера — щоб функції розбору можна було
# перевірити навіть без інтернету. Зверніть увагу: рядки протоколу
# розділяються послідовністю \r\n, а порожній рядок (\r\n\r\n) відділяє
# заголовки від тіла відповіді.
SAMPLE_RESPONSE = (
    b"HTTP/1.1 200 OK\r\n"
    b"Content-Type: text/html; charset=UTF-8\r\n"
    b"Content-Length: 25\r\n"
    b"Server: ExampleServer\r\n"
    b"\r\n"
    b"<html>Hello, world!</html>"
)
# --------------------------------------------------------------------------


def parse_status_code(raw):
    """Повертає числовий код відповіді (наприклад, 200) з сирої відповіді.

    Ця функція вже написана — вона ваш зразок. Розберіть її в методичці.

    Перший рядок відповіді має вигляд "HTTP/1.1 200 OK". Ми беремо все до
    першого \r\n, розбиваємо за пробілами і беремо другий шматок — це й є код.
    """
    first_line = raw.split(b"\r\n")[0]
    parts = first_line.split(b" ")
    return int(parts[1])


def parse_headers(raw):
    """Повертає заголовки відповіді як словник {назва: значення}.

    ВПРАВА 1. Тут уже написано найскладніше — робота з байтами. Вам лишається
    один цикл. Розберіть готові рядки нижче, а тоді допишіть цикл за зразком.

    Має вийти, зокрема: результат["Content-Type"] == "text/html; charset=UTF-8".
    """
    # Крок А (вже зроблено). Відділяємо заголовки від тіла за порожнім рядком
    # b"\r\n\r\n" і беремо рядки заголовків БЕЗ першого (той — рядок статусу).
    head = raw.split(b"\r\n\r\n", 1)[0]
    header_lines = head.split(b"\r\n")[1:]

    # Крок Б (зразок). Ось як обробити ОДИН рядок-заголовок. Наприклад, якщо
    #   line = b"Content-Type: text/html"
    # то розділяємо його рівно один раз за b": " і переводимо байти в рядки:
    #   name, value = line.split(b": ", 1)      # b"Content-Type", b"text/html"
    #   result[name.decode()] = value.decode()  # "Content-Type" -> "text/html"

    result = {}
    # ВАШ КОД. Пройдіть циклом кожен line у header_lines і зробіть із ним те
    # саме, що показано у зразку вище, складаючи все у словник result.
    # Початок циклу: for line in header_lines:
    for line in header_lines:
        name, value = line.split(b": ", 1)
        result[name.decode()] = value.decode()

    return result


def get_body(raw):
    """Повертає тіло відповіді (те, що йде після заголовків) як рядок.

    ВПРАВА 2. Напишіть тіло цієї функції.

    Тіло — це все, що стоїть ПІСЛЯ порожнього рядка b"\r\n\r\n".
    Розбийте raw цією послідовністю (split(b"\r\n\r\n", 1)), візьміть другу
    частину і переведіть її в рядок через .decode(errors="replace").
    Для SAMPLE_RESPONSE має вийти "<html>Hello, world!</html>".
    """
    # Приберіть рядок нижче і напишіть свій код.
    return raw.split(b"\r\n\r\n", 1)[1].decode(errors="replace")


def http_get(host, path="/"):
    """Надсилає серверу справжній HTTP-запит і повертає сиру відповідь.

    Ця функція вже написана. Вона складає текст запиту рівно за правилами
    протоколу і відправляє його в сокет — так само, як це робить браузер.
    """
    import socket
    request = (
        "GET " + path + " HTTP/1.1\r\n"
        "Host: " + host + "\r\n"
        "Connection: close\r\n"
        "User-Agent: KSE-lab2\r\n"
        "\r\n"
    )
    with socket.create_connection((host, 80), timeout=10) as sock:
        sock.sendall(request.encode())
        chunks = []
        while True:
            data = sock.recv(4096)
            if not data:
                break
            chunks.append(data)
    return b"".join(chunks)


# Увесь код нижче виконується лише коли ви запускаєте цей файл напряму
# (python part2_http.py). Так автоперевірка може імпортувати ваші функції,
# не виходячи при цьому в мережу. Вашого коду вправ це не стосується — ви
# пишете тіла функцій вище.
if __name__ == "__main__":
    # === Самоперевірка розбору (працює без інтернету) =====================
    show("=== Розбір збереженої відповіді ===")
    show("Код відповіді:", parse_status_code(SAMPLE_RESPONSE))
    show("Заголовок Content-Type:",
         parse_headers(SAMPLE_RESPONSE).get("Content-Type", "(не знайдено)"))
    show("Тіло:", get_body(SAMPLE_RESPONSE))

    ok = (parse_status_code(SAMPLE_RESPONSE) == 200
          and parse_headers(SAMPLE_RESPONSE).get("Content-Type") == "text/html; charset=UTF-8"
          and get_body(SAMPLE_RESPONSE) == "<html>Hello, world!</html>")
    show("Усі три функції розбору працюють правильно:" if ok
         else "Розбір ще не працює — доробіть вправи 1 і 2.", ok)

    # === Справжній запит (потрібен інтернет) =============================
    # Беремо example.com, бо він відповідає на звичайний запит кодом 200 і
    # віддає сторінку. Якщо підставити великий сайт (напр. google.com), сервер
    # найпевніше поверне код 301/302 і майже порожнє тіло — це не помилка, а
    # вимога перейти на захищену версію (HTTPS). Можете спробувати заради
    # цікавості.
    show("")
    show("=== Справжній запит до example.com ===")
    try:
        raw = http_get("example.com", "/")
        show("Код відповіді сервера:", parse_status_code(raw))
        headers = parse_headers(raw)
        show("Сервер повідомив тип вмісту:", headers.get("Content-Type", "(немає)"))
        show("Довжина отриманого тіла, байтів:", len(get_body(raw)))
    except OSError as e:
        show("мережа недоступна:", e.__class__.__name__,
             "- частину з розбором це не скасовує")

    # --- збереження результату, чіпати не треба ---------------------------
    with open("part2_output.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print()
    print("Готово. Результат збережено у файл part2_output.txt")
