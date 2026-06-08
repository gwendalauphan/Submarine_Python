"""External process runner for the 3D submarine view."""

from dataclasses import dataclass
from multiprocessing import get_context
from queue import Empty, Full
from tkinter import Frame, Tk

import numpy as np

from plot_3d.plot_5 import plot_five


@dataclass(frozen=True)
class SubmarineSnapshot:
    coor: tuple[float, float, float]
    vect: tuple[float, float, float]
    elapsed: float


class SnapshotParent:
    def __init__(self, win, snapshot):
        self.win = win
        self.running = True
        self.apply_snapshot(snapshot)

    def apply_snapshot(self, snapshot):
        self.coor = np.array(snapshot.coor).reshape(1, 3)
        self.vect = np.array(snapshot.vect).reshape(1, 3)
        self.t2 = snapshot.elapsed

    def on_close(self):
        self.running = False
        self.win.destroy()


def put_latest_snapshot(snapshot_queue, snapshot):
    if snapshot_queue is None:
        return

    while True:
        try:
            snapshot_queue.put_nowait(snapshot)
            return
        except Full:
            try:
                snapshot_queue.get_nowait()
            except Empty:
                return
        except (BrokenPipeError, EOFError, OSError):
            return


def close_snapshot_queue(snapshot_queue):
    if snapshot_queue is None:
        return

    try:
        snapshot_queue.cancel_join_thread()
    except (AttributeError, OSError, ValueError):
        pass

    try:
        snapshot_queue.close()
    except (AttributeError, OSError, ValueError):
        pass


def run_3d_window(snapshot_queue, stop_event, initial_snapshot, win_width, win_height):
    root = Tk()
    root.title("Submarine 3D View")
    frame = Frame(root)
    frame.pack(fill="both", expand=True)

    parent = SnapshotParent(root, initial_snapshot)
    plot = plot_five(root, parent, win_width, win_height, frame)
    closing = False

    def close_window():
        nonlocal closing
        if closing:
            return

        closing = True
        parent.running = False
        stop_event.set()
        plot.close()
        try:
            root.quit()
        except Exception:
            pass
        try:
            root.destroy()
        except Exception:
            pass

    def poll_snapshots():
        if stop_event.is_set() or not parent.running:
            close_window()
            return

        latest_snapshot = None
        while True:
            try:
                latest_snapshot = snapshot_queue.get_nowait()
            except Empty:
                break

        if latest_snapshot is not None:
            parent.apply_snapshot(latest_snapshot)
            plot.update_sub()

        root.after(100, poll_snapshots)

    root.protocol("WM_DELETE_WINDOW", close_window)
    root.after(100, poll_snapshots)
    try:
        root.mainloop()
    finally:
        close_window()
        close_snapshot_queue(snapshot_queue)


def start_3d_process(initial_snapshot, win_width, win_height):
    context = get_context("spawn")
    snapshot_queue = context.Queue(maxsize=2)
    stop_event = context.Event()
    process = context.Process(
        target=run_3d_window,
        args=(snapshot_queue, stop_event, initial_snapshot, win_width, win_height),
        name="submarine-3d-view",
    )
    process.daemon = True
    process.start()
    return process, snapshot_queue, stop_event


def stop_3d_process(process, stop_event, timeout=1.0):
    if process is None or stop_event is None:
        return

    stop_event.set()
    process.join(timeout)
    if process.is_alive():
        process.terminate()
        process.join(timeout)
    if process.is_alive():
        process.kill()
        process.join(timeout)
    try:
        process.close()
    except (AttributeError, OSError, ValueError):
        pass
