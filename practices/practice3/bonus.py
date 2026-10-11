import os

from part1_model import tokenize, build_model, predict_next, generate

def read_words(path):
    """Читає файл і повертає список слів. Якщо файлу немає — порожній список."""
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return tokenize(f.read())

def test_inconsistent_start():
    print("-" * 10, "test_inconsistent_start", "-" * 10)
    n = 3
    corpus = read_words("corpus.txt")
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


def main():
    test_inconsistent_start()

if __name__ == "__main__":
    main()
