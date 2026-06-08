"""Demonstrate a simple ProcessPoolExecutor workflow."""

from concurrent.futures import ProcessPoolExecutor, as_completed
from time import perf_counter, sleep


def slow_message(message, delay):
    sleep(delay)
    return f"{message} finished after {delay:.1f}s"


def main():
    jobs = [
        ("first job", 0.4),
        ("second job", 0.2),
        ("third job", 0.3),
    ]

    start = perf_counter()
    with ProcessPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(slow_message, message, delay) for message, delay in jobs]

        for future in as_completed(futures):
            print(future.result())

    elapsed = perf_counter() - start
    print(f"all jobs finished in {elapsed:.2f}s")


if __name__ == "__main__":
    main()

