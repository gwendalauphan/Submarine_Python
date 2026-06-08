# Concurrency Playground

This folder contains small research scripts for multiprocessing, process pools,
threading, and Tkinter feasibility checks. They are intentionally separate from
the submarine simulator folders so the application code stays focused on the
runnable simulator.

Run commands from the repository root.

## Setup

Install the simulator dependencies if you also want to run the Tkinter and
Matplotlib-based parts of the project:

```bash
python3 -m pip install -r submarine_merge/requirements.txt
```

Tkinter usually comes with Python. On Debian/Ubuntu, install it with:

```bash
sudo apt-get install python3-tk
```

## Scripts

### Shared Memory Demo

```bash
python3 playground/concurrency/shared_memory_demo.py
```

Expected behavior:

- Starts one child process.
- The child process writes `3.1415927` into a shared `Value`.
- The child process negates every value in a shared `Array`.
- The parent process prints the modified shared values.

### Process Pool Demo

```bash
python3 playground/concurrency/process_pool_demo.py
```

Expected behavior:

- Starts a `ProcessPoolExecutor`.
- Submits a few short jobs.
- Prints each result as the jobs finish.
- Prints total elapsed time.

### Process With Threads Demo

```bash
python3 playground/concurrency/process_with_threads_demo.py
```

Expected behavior:

- Starts multiple processes.
- Each process starts multiple threads.
- Each thread prints its process id and thread name.
- The script exits after all processes and threads have joined.

### Tkinter Threading Demo

```bash
python3 playground/concurrency/thread_vs_tkinter_demo.py
```

Expected behavior:

- Opens a small Tkinter window in a graphical environment.
- Runs worker threads for background work.
- Sends worker progress back to the Tkinter main thread through a queue.
- Updates the UI from the Tkinter main loop only.

Tkinter widgets should be created and updated on the main thread. Worker threads
can do background work, but they should communicate results back to the UI with a
thread-safe queue and `after()` polling.

