from tkinter import Canvas, LEFT, RIGHT, BOTTOM
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

class plot_four:
    def __init__(self,win, parent,win_width, win_height ,Frame ):
        self.win = win
        self.parent = parent
        self.win_width = win_width
        self.win_height = win_height
        self.Frame = Frame
        self.verite = 1
        self.current_mode = 1

        self.v = tk.IntVar()
        self.v.set(1)  # initializing the choice, i.e. Python

        self.choix = [("vitesse",1), ("accélération",2), ("v at acc relatives", 3)]
        self.menu_graph = Canvas(self.Frame, width = self.win_width/2, highlightthickness = 0)
        self.menu_graph.pack()

        tk.Label(self.menu_graph,text="Choisis les informations à afficher:").pack(side = LEFT)
        for val, choice in enumerate(self.choix):
            tk.Radiobutton(self.menu_graph,text=choice,variable=self.v,command=self.ShowChoice,value=val).pack(side =LEFT)

        tk.Button(self.menu_graph, text = "Reset", command = self.reset).pack(side = RIGHT)

        self.graph_can = Canvas(self.Frame, height = self.win_height/2, width = self.win_width/2, highlightthickness = 0, bg = 'black')
        self.graph_can.pack(side = BOTTOM, fill=tk.BOTH, expand= True)

        self.fig, self.ax = plt.subplots(figsize=(5, 10), dpi= 100)
        self.graph = FigureCanvasTkAgg(self.fig, self.graph_can)
        toolbar = NavigationToolbar2Tk(self.graph, self.graph_can)
        toolbar.update()
        self.graph.get_tk_widget().pack( fill=tk.BOTH, expand= True)


        self.line1, = self.ax.plot([], [], c = "blue")
        self.line2, = self.ax.plot([], [], c = "red")
        self.line3, = self.ax.plot([], [], c = "yellow")

        self.ax.set_ylim(-1,1)
        self.ax.set_yscale('symlog', linthresh=0.01)
        self.ax.set_title("Accélérations en fonction du temps", weight = 'bold')
        self.ax.legend((self.line1, self.line2, self.line3), ('acc_x', 'acc_y', 'acc_z'))
        self.fig.canvas.draw()

        self.ax.grid(alpha =0.5)

    def update_graph(self):

        if self.v.get() == 0 and len(self.parent.liste_v_x)>0:
            self.line1.set_data(self.parent.liste_time, self.parent.liste_v_x)
            self.line2.set_data(self.parent.liste_time, self.parent.liste_v_y)
            self.line3.set_data(self.parent.liste_time, self.parent.liste_v_z)

        elif self.v.get() == 1 and len(self.parent.liste_acc_x)>0:
            self.line1.set_data(self.parent.liste_time, self.parent.liste_acc_x)
            self.line2.set_data(self.parent.liste_time, self.parent.liste_acc_y)
            self.line3.set_data(self.parent.liste_time, self.parent.liste_acc_z)

        elif self.v.get() == 2 and len(self.parent.liste_acc_relatif)>0:
            self.line1.set_data(self.parent.liste_time, self.parent.liste_acc_relatif)
            self.line2.set_data(self.parent.liste_time, self.parent.liste_v_relatif)
            self.line3.set_data([], [])

        left = max(0, self.parent.t2 - 10)
        right = self.parent.t2
        if right <= left:
            right = left + 1e-6
        self.ax.set_xlim(left=left, right=right)

        self.fig.canvas.draw_idle()

    def _clear_series(self, data):
        if hasattr(data, 'clear'):
            data.clear()
        else:
            del data[:]

    def reset(self):
        #self.graph_can.destroy()
        self._clear_series(self.parent.liste_time)
        self._clear_series(self.parent.liste_acc_x)
        self._clear_series(self.parent.liste_acc_y)
        self._clear_series(self.parent.liste_acc_z)
        self._clear_series(self.parent.liste_v_x)
        self._clear_series(self.parent.liste_v_y)
        self._clear_series(self.parent.liste_v_z)
        self._clear_series(self.parent.liste_acc_relatif)
        self._clear_series(self.parent.liste_v_relatif)
        #self.graph_can = Canvas(self.Frame, height = self.win_height/2, width = self.win_width/2, highlightthickness = 0, bg = 'black')
        #self.graph_can.pack(side = BOTTOM, fill=tk.BOTH, expand= True)


        self.ShowChoice()

    def ShowChoice(self):
        if self.v.get() != self.verite:
            self._clear_series(self.parent.liste_time)

        if self.v.get() != 0 and self.verite == 0:
            self._clear_series(self.parent.liste_v_x)
            self._clear_series(self.parent.liste_v_y)
            self._clear_series(self.parent.liste_v_z)

        elif self.v.get() != 1 and self.verite == 1:
            self._clear_series(self.parent.liste_acc_x)
            self._clear_series(self.parent.liste_acc_y)
            self._clear_series(self.parent.liste_acc_z)


        elif self.v.get() != 2 and self.verite == 2:
            self._clear_series(self.parent.liste_acc_relatif)
            self._clear_series(self.parent.liste_v_relatif)


        if self.v.get() == 0:
            self.ax.set_ylim(-5,5)
            self.ax.set_title("Vitesses en fonction du temps", weight = 'bold')
            self.ax.legend((self.line1, self.line2, self.line3), ('v_x', 'v_y', 'v_z'),loc = 'upper right')
            self.ax.set_yscale('symlog', linthresh=0.01)
            self.current_mode = 0

        elif self.v.get() == 1:
            self.ax.set_ylim(-1,1)
            self.ax.set_title("Accélérations en fonction du temps", weight = 'bold')
            self.ax.legend((self.line1, self.line2, self.line3), ('acc_x', 'acc_y', 'acc_z'),loc = 'upper right')
            self.ax.set_yscale('symlog', linthresh=0.01)
            self.current_mode = 1
        else:
            self.ax.set_ylim(-5,5)
            self.ax.set_title("V et Acc relatives en fonction du temps", weight = 'bold')
            self.ax.legend((self.line1, self.line2), ('acc', 'v'),loc = 'upper right')
            self.ax.set_yscale('symlog', linthresh=0.01)
            self.current_mode = 2

        self.verite = self.v.get()
        self.fig.canvas.draw_idle()
