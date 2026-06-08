"""Open several Tkinter windows, each refreshed by its own process."""

from argparse import ArgumentParser
from math import sin
from multiprocessing import Process
from time import perf_counter
from tkinter import Canvas, Label, Tk


def run_window(window_index, total_windows, refresh_ms, duration_s):
    root = Tk()
    root.title(f"Parallel refresh window {window_index}")
    root.geometry(f"360x180+{80 + window_index * 48}+{80 + window_index * 48}")

    title = Label(root, text=f"Window {window_index + 1}/{total_windows}")
    title.pack(pady=(12, 4))

    status = Label(root, text="Starting...")
    status.pack(pady=(0, 8))

    canvas = Canvas(root, width=320, height=80, bg="white", highlightthickness=1)
    canvas.pack(padx=16, pady=(0, 16))
    bar = canvas.create_rectangle(10, 28, 70, 52, fill="#2f80ed", outline="")
    marker = canvas.create_line(160, 10, 160, 70, fill="#27ae60", width=2)

    start = perf_counter()
    frame = 0

    def refresh():
        nonlocal frame
        elapsed = perf_counter() - start
        if elapsed >= duration_s:
            root.destroy()
            return

        frame += 1
        progress = (sin(elapsed * 4 + window_index) + 1) / 2
        x = 10 + progress * 240
        marker_x = 160 + sin(elapsed * 2) * 80
        canvas.coords(bar, x, 28, x + 60, 52)
        canvas.coords(marker, marker_x, 10, marker_x, 70)
        status.config(text=f"frames: {frame} | elapsed: {elapsed:.2f}s")
        root.after(refresh_ms, refresh)

    root.after(refresh_ms, refresh)
    root.mainloop()


def main():
    parser = ArgumentParser(description="Open several independently refreshed Tkinter windows.")
    parser.add_argument("--windows", type=int, default=3, help="Number of windows/processes to start.")
    parser.add_argument("--refresh-ms", type=int, default=50, help="Refresh delay for each window.")
    parser.add_argument("--duration-s", type=float, default=8.0, help="Seconds before windows close.")
    args = parser.parse_args()

    if args.windows < 1:
        raise ValueError("--windows must be at least 1")
    if args.refresh_ms < 1:
        raise ValueError("--refresh-ms must be at least 1")
    if args.duration_s <= 0:
        raise ValueError("--duration-s must be positive")

    processes = []
    for window_index in range(args.windows):
        process = Process(
            target=run_window,
            args=(window_index, args.windows, args.refresh_ms, args.duration_s),
            name=f"tk-window-{window_index}",
        )
        processes.append(process)
        process.start()

    for process in processes:
        process.join()


if __name__ == "__main__":
    main()

