import os
import random

from part1_model import tokenize, build_model, predict_next, generate

def read_words(path):
    """Читає файл і повертає список слів. Якщо файлу немає — порожній список."""
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return tokenize(f.read())

def test_inconsistent_start(corpus):
    print("-" * 10, "test_inconsistent_start", "-" * 10)
    n = 3
    model = build_model(corpus, n)

    start = ("рахували", "сусідню", "бо") 
    produced = generate(model, start, 40)
    print(produced)

    start = ("швидше", "але", "а") 
    produced = generate(model, start, 40)
    print(produced)

    start = ("і", "тому", "на") 
    produced = generate(model, start, 40)
    print(produced)


    print("with random:")
    seed = 389
    start = ("рахували", "сусідню", "бо") 
    produced = generate(model, start, 40, random.Random(seed))
    print(produced)

    start = ("швидше", "але", "а") 
    produced = generate(model, start, 40, random.Random(seed))
    print(produced)

    start = ("і", "тому", "на") 
    produced = generate(model, start, 40, random.Random(seed))
    print(produced)

def test_full_copy(corpus):
    print("-" * 10, "test_full_copy", "-" * 10)
    for n in range(1, 20):
        model = build_model(corpus, n)
        start = tuple(corpus[:n])
        produced = generate(model, start, len(corpus))

        is_copied = (list(start) + produced) == corpus
        print("n:", n, "is full copied?:", is_copied)


def main():
    corpus = read_words("corpus.txt")
    test_inconsistent_start(corpus)
    test_full_copy(corpus)

if __name__ == "__main__":
    main()
