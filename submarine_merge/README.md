# Submarine Merge - Simulator

## Description
This folder contains a merged, runnable version of the submarine simulation project.

The app is a Tkinter desktop interface with several visual modules:
- 2D top/side views of the submarine
- Compass/orientation display
- A 3D terrain/water view
- Live graph panel for speed/acceleration signals
- Numeric telemetry panel (speed, acceleration, position)

The simulation updates submarine dynamics in real time (buoyancy, drag, propeller thrust, heading), then refreshes views and graphs on a schedule.

## How To Run
### 1) Requirements
Use Python 3.9+ (3.10+ recommended) and install:
- numpy
- matplotlib
- tkinter (usually already included with system Python on Linux)

If needed:

```bash
python3 -m pip install numpy matplotlib
```

On Debian/Ubuntu, if Tk is missing:

```bash
sudo apt-get install python3-tk
```

### 2) Launch
From this folder:

```bash
cd submarine_merge
python3 main.py
```

The window starts maximized.

### 3) Controls
- Right arrow: turn right (rudder)
- Left arrow: turn left (rudder)
- Up arrow: decrease ballast water index
- Down arrow: increase ballast water index
- z: increase propeller RPM
- s: decrease propeller RPM

In the graph panel:
- Select display mode: speed / acceleration / relative speed+acceleration
- Use "Reset" to clear graph histories

## How It Works
### Main Loop
The core loop is in `main.py` inside `submarine.update()`.
It is scheduled with:

```python
self.win.after(10, self.update)
```

At each cycle the code:
1. Updates forces and accelerations (buoyancy, weight, drag, thrust)
2. Integrates velocities and position using the elapsed time step (`self.t3`)
3. Updates heading/rudder behavior
4. Stores telemetry history for plotting
5. Refreshes UI modules at different frequencies

### Refresh Rates
Different panels are updated at different intervals to keep the UI responsive:
- Every 10 ticks: compass + orientation updates
- Every 50 ticks: graph panel + numeric telemetry
- Every 250 ticks: 3D submarine/scene update

### Data Flow
- `main.py` computes physics and stores live values in attributes/lists
- Plot classes (`plot_1.py`, `plot_2.py`, `plot_3.py`, `plot_4.py`, `plot_6.py`) read from the shared `submarine` object
- 3D rendering is handled by `plot_3d/plot_5.py`, using `plot_3d/map.py` and `plot_3d/perlin.py`

### Entry Point
Startup is protected by:

```python
if __name__ == '__main__':
    sub1 = submarine(...)
```

This keeps imports safer if you later add tests or tools around the project.
