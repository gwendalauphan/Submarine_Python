from tkinter import*
import tkinter as tk
from math import*
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.pyplot import figure
import matplotlib.tri as mtri
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D,proj3d  # noqa: F401 unused import
from matplotlib import cm
from plot_3d.map import*

from matplotlib.patches import FancyArrowPatch

import concurrent.futures
import time

class plot_four:
    def __init__(self,win):
        self.win = win
        self.graph_can = Canvas(self.win, highlightthickness = 0, bg = 'black')
        self.graph_can.pack(side = BOTTOM, fill=tk.BOTH, expand= True)

        self.fig_1, self.ax_1 = plt.subplots(figsize=(5, 10), dpi= 100)
        self.graph = FigureCanvasTkAgg(self.fig_1, self.graph_can)
        toolbar = NavigationToolbar2Tk(self.graph, self.graph_can)
        toolbar.update()
        self.graph.get_tk_widget().pack( fill=tk.BOTH, expand= True)

        self.i = 0
        self.x = np.arange(0,100,0.1)
        self.y = np.arange(0,100,0.1)
        self.data1 = []
        self.data2 = []
        self.update()

    def update(self):

        print(self.i)
        self.i+=1

        self.data1.append(self.x[self.i])
        self.data2.append(self.y[self.i])
        self.line = self.ax_1.scatter(self.data1,self.data2, c = 'b')
        self.fig_1.canvas.draw()
        self.win.after(5, self.update)


def do_something(secs):
    if secs ==1:
        win1 = Tk()
        a = plot_four(win1)
        win1.mainloop()
    if secs ==2:
        win2 = Tk()
        b = plot_four(win2)
        win2.mainloop()
    if secs ==3:
        win3 = Tk()
        c = plot_four(win3)
        win3.mainloop()
    if secs ==4:
        win4 = Tk()
        d = plot_four(win4)
        win4.mainloop()

    print(f'Sleeping {seconds} second(s)...')
    time.sleep(seconds)
    return f'Done Sleeping...{seconds}'

if __name__ == '__main__':
    with concurrent.futures.ProcessPoolExecutor() as executor:
        secs = [1,2,3,4]
        #secs = [1]
        results = executor.map(do_something, secs)

        # for result in results:
        #     print(result)
