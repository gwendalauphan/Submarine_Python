"""Demonstrate processes that each start a small group of threads."""

from multiprocessing import Process, current_process
from threading import Thread, current_thread


def thread_worker(process_index, thread_index):
    process_name = current_process().name
    thread_name = current_thread().name
    print(f"process {process_index} ({process_name}) / thread {thread_index} ({thread_name})")


def process_worker(process_index, thread_count):
    threads = []
    for thread_index in range(thread_count):
        thread = Thread(
            target=thread_worker,
            args=(process_index, thread_index),
            name=f"worker-thread-{thread_index}",
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


def main(process_count=2, thread_count=3):
    processes = []
    for process_index in range(process_count):
        process = Process(
            target=process_worker,
            args=(process_index, thread_count),
            name=f"worker-process-{process_index}",
        )
        processes.append(process)
        process.start()

    for process in processes:
        process.join()


if __name__ == "__main__":
    main()

