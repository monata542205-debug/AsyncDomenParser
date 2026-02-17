import threading

import threading


def func(numbers, thread_id):
    filename = f"thread_{thread_id}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        for num in numbers:
            if num < 5:
                f.write(f"{num}\n")


def streams(function, sublists):
    threads = []

    for i, chunk in enumerate(sublists, 1):
        if not chunk:
            continue

        t = threading.Thread(
            target=function,  # ← сразу твоя функция
            args=(chunk, i),  # ← передаём два аргумента
            daemon=True
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

if __name__ == "__main__":
    # тестовые данные — 10 одинаковых списков
    links = [[1, 2, 3, 4, 5, 6, 7]] * 10
    streams(func, links)      #