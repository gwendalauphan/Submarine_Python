"""Demonstrate the safe pattern for mixing worker threads with Tkinter."""

from queue import Empty, Queue
from threading import Thread
from time import sleep
from tkinter import Button, Label, Tk


def worker(worker_id, messages):
    for step in range(1, 4):
        sleep(0.3)
        messages.put(f"worker {worker_id}: step {step}/3")
    messages.put(f"worker {worker_id}: done")


class ThreadedTkinterDemo:
    def __init__(self):
        self.root = Tk()
        self.root.title("Tkinter threading demo")
        self.messages = Queue()
        self.running_threads = []

        self.status = Label(self.root, text="Press Start to launch worker threads.", width=42)
        self.status.pack(padx=16, pady=(16, 8))

        self.start_button = Button(self.root, text="Start", command=self.start_workers)
        self.start_button.pack(padx=16, pady=(0, 16))

        self.root.after(100, self.poll_messages)

    def start_workers(self):
        self.start_button.config(state="disabled")
        self.status.config(text="Workers running...")

        for worker_id in range(2):
            thread = Thread(target=worker, args=(worker_id, self.messages), daemon=True)
            self.running_threads.append(thread)
            thread.start()

    def poll_messages(self):
        try:
            while True:
                message = self.messages.get_nowait()
                self.status.config(text=message)
        except Empty:
            pass

        if self.running_threads and all(not thread.is_alive() for thread in self.running_threads):
            self.start_button.config(state="normal")
            self.running_threads.clear()

        self.root.after(100, self.poll_messages)

    def run(self):
        self.root.mainloop()


def main():
    ThreadedTkinterDemo().run()


if __name__ == "__main__":
    main()

