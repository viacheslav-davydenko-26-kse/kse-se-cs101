# Частина 2. Досліди над власною мовною моделлю.
#
# Цей скрипт майже повністю готовий. Він бере вашу модель із частини 1 і
# ставить над нею чотири досліди. Запустіть його, уважно подивіться на вивід
# і поясніть побачене у report.md. Наприкінці є одна вправа.
#
# Перед запуском покладіть поруч файл my_text.txt зі СВОЇМ текстом
# (не менше 200 слів). Про те, який текст брати, написано в методичці.

import os
import random

from part1_model import tokenize, build_model, predict_next, generate

# --- службовий блок, його чіпати не треба ---------------------------------
lines = []


def show(*args):
    text = " ".join(str(a) for a in args)
    print(text)
    lines.append(text)


def read_words(path):
    """Читає файл і повертає список слів. Якщо файлу немає — порожній список."""
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return tokenize(f.read())


def copied_fraction(generated, source, k=6):
    """Яка частка породженого тексту дослівно зустрічається в джерелі.

    Ріжемо і породжений текст, і джерело на ланцюжки по k слів і дивимося,
    скільки ланцюжків породженого знайшлося в джерелі. Сто відсотків означає,
    що модель не склала нічого свого, а переписала навчальний текст.
    """
    if len(generated) < k:
        return 0.0
    source_grams = set()
    for i in range(len(source) - k + 1):
        source_grams.add(tuple(source[i:i + k]))
    total = 0
    copied = 0
    for i in range(len(generated) - k + 1):
        total = total + 1
        if tuple(generated[i:i + k]) in source_grams:
            copied = copied + 1
    return copied / total


def unique_share(words):
    """Частка різних слів серед породжених. Низька — модель ходить по колу."""
    if not words:
        return 0.0
    return len(set(words)) / len(words)


def cycle_length(words, tail=24):
    """Довжина циклу в кінці тексту, або 0, якщо циклу немає."""
    t = words[-tail:]
    for period in range(1, len(t) // 2 + 1):
        if all(t[i] == t[i - period] for i in range(period, len(t))):
            return period
    return 0


def counts(words):
    c = {}
    for w in words:
        c[w] = c.get(w, 0) + 1
    return c
# --------------------------------------------------------------------------


corpus = read_words("corpus.txt")
show("Слів у корпусі:", len(corpus), "| різних слів:", len(set(corpus)))
show("")


show("=== Дослід 1. Що дає довжина контексту ===")
show("Скрізь однаковий початок і однаковий жадібний вибір слова —")
show("змінюється лише те, скільки слів модель пам'ятає.")
show("")
for n in (1, 2, 3):
    model = build_model(corpus, n)
    start = tuple(corpus[:n])
    produced = generate(model, start, 40)
    show("--- n =", n, "---")
    show(" ".join(start) + " " + " ".join(produced))
    show("дослівно з корпусу: %.0f%%" % (100 * copied_fraction(produced, corpus)),
         "| різних слів: %.0f%%" % (100 * unique_share(produced)),
         "| довжина циклу:", cycle_length(produced) or "немає")
    show("")


show("=== Дослід 2. Контекст, якого модель не бачила ===")
model2 = build_model(corpus, 2)
for ctx in (tuple(corpus[:2]), ("кіт", "з'їв"), ("квантовий", "процесор")):
    show("контекст", ctx, "-> наступне слово:", predict_next(model2, ctx))
show("")


show("=== Дослід 3. Жадібний вибір проти випадкового ===")
model1 = build_model(corpus, 1)
start1 = tuple(corpus[:1])
greedy = generate(model1, start1, 40)
show("--- жадібно (завжди найімовірніше слово) ---")
show(" ".join(greedy))
show("різних слів: %.0f%%" % (100 * unique_share(greedy)),
     "| довжина циклу:", cycle_length(greedy) or "немає")
show("")
for seed in (1, 2):
    sampled = generate(model1, start1, 40, random.Random(seed))
    show("--- випадково, seed =", seed, "---")
    show(" ".join(sampled))
    show("різних слів: %.0f%%" % (100 * unique_share(sampled)),
         "| довжина циклу:", cycle_length(sampled) or "немає")
    show("")


show("=== Дослід 4. Коли даних про одне більше, ніж про інше ===")
my_words = read_words("my_text.txt")
if len(my_words) < 200:
    show("Файл my_text.txt відсутній або в ньому менше 200 слів",
         "(знайдено %d)." % len(my_words))
    show("Без нього цей дослід не виконується.")
else:
    only_corpus = set(corpus) - set(my_words)
    only_mine = set(my_words) - set(corpus)
    shared = set(corpus) & set(my_words)
    if len(shared) < 5:
        show("Спільних слів із корпусом:", len(shared), "— цього замало.")
        show("Найімовірніша причина: ваш текст іншою мовою. Модель може перейти")
        show("з одного тексту в інший лише через слова, які є в обох, тож")
        show("візьміть український текст — і дослід запрацює.")
    else:
        cc, cm = counts(corpus), counts(my_words)
        start = max(sorted(shared), key=lambda w: cc[w] + cm[w])
        show("Слів у вашому тексті:", len(my_words),
             "| спільних слів із корпусом:", len(shared))
        show("Стартуємо зі слова", repr(start),
             "— воно є в обох текстах, тож модель може піти в будь-який бік.")
        show("")
        show("УВАГА: тут модель пам'ятає лише ОДНЕ слово, тому породжений текст")
        show("буде беззмістовним — так і має бути. Ми дивимося не на зв'язність,")
        show("а на те, СЛОВА З ЯКОГО тексту модель тягне. Саме це й показує,")
        show("куди її хилять дані.")
        show("")
        samples = {}
        show("%-22s %-16s %-16s" % ("частка вашого тексту",
                                    "слова з корпусу", "слова з вашого"))
        for share in (0.0, 0.1, 0.3, 0.5, 0.7, 0.9):
            if share == 0.0:
                mixed = corpus
            else:
                repeats = max(1, round(share * len(corpus) /
                                       ((1 - share) * len(my_words))))
                mixed = corpus + my_words * repeats
            produced = generate(build_model(mixed, 1), (start,), 200,
                                random.Random(7))
            from_corpus = sum(1 for w in produced if w in only_corpus)
            from_mine = sum(1 for w in produced if w in only_mine)
            total = max(1, len(produced))
            show("%-22s %-16s %-16s" % ("%.0f%%" % (100 * share),
                                        "%.0f%%" % (100 * from_corpus / total),
                                        "%.0f%%" % (100 * from_mine / total)))
            if share in (0.0, 0.9):
                samples[share] = produced[:25]
        show("")
        show("Тут пораховано лише ті слова, які є ВИКЛЮЧНО в одному з текстів —")
        show("спільні слова на кшталт «і» чи «в» не зараховані жодній стороні.")
        show("")
        show("А ось як це виглядає словами — два крайні рядки таблиці:")
        for share in (0.0, 0.9):
            if share in samples:
                show("--- вашого тексту %.0f%% ---" % (100 * share))
                show(" ".join(samples[share]))
show("")


# === ВПРАВА ===============================================================
# Виберіть власний початок — два слова, які точно йдуть поспіль десь у
# corpus.txt, — і подивіться, що модель скаже з нього.
#
# Зробіть три речі:
#   1) присвойте змінній MY_START кортеж із двох слів, наприклад ("не", "має");
#      назва MY_START обов'язкова — за нею перевіряється вправа;
#   2) породьте від нього 40 слів по моделі model2 з випадковим вибором
#      (третій аргумент — довжина, четвертий — random.Random із вашим seed);
#   3) виведіть результат через show, щоб він потрапив у файл.
#
# Зразок виклику:
#     produced = generate(model2, MY_START, 40, random.Random(3))
#     show(" ".join(MY_START), " ".join(produced))
#
# Ваш код:
MY_START = ("інженери", "навчилися")

produced = generate(model2, MY_START, 40, random.Random(69))
show(" ".join(MY_START), " ".join(produced))


# --- збереження результату, чіпати не треба -------------------------------
with open("part2_output.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

print()
print("Готово. Результат збережено у файл part2_output.txt")
