"""Demonstrate multiprocessing shared Value and Array objects."""

from multiprocessing import Array, Process, Value


def update_shared_state(number, values):
    number.value = 3.1415927
    for index in range(len(values)):
        values[index] = -values[index]


def main():
    number = Value("d", 0.0)
    values = Array("i", range(10))

    process = Process(target=update_shared_state, args=(number, values))
    process.start()
    process.join()

    print(f"shared number: {number.value}")
    print(f"shared array: {list(values)}")


if __name__ == "__main__":
    main()

