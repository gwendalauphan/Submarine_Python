from tkinter import*

class plot_six_central:
    def __init__(self,win, parent,win_width, win_height ,Frame ):
        self.win = win
        self.parent = parent
        self.win_width = win_width
        self.win_height = win_height
        self.Frame = Frame

        self.canvas_aff = Canvas(self.Frame, height = self.win_height/2, width = self.win_width/8, highlightthickness = 0, bg="black")
        self.canvas_aff.pack(fill = BOTH, expand =True)

        cut = 20
        height = win_height/2
        i1 = 20
        Label(self.canvas_aff, text = "Acc générale:", fg = "white", bg="black").place(x = 10, y = i1)
        self.LabelAcc = Label(self.canvas_aff, text = "0", fg = "white", bg="black")
        self.LabelAcc.place(x = 10, y = i1 + height/cut)

        i2 = height/5 + 20
        Label(self.canvas_aff, text = "Vit générale:", fg = "white", bg="black").place(x = 10, y = i2)
        self.LabelVitG = Label(self.canvas_aff, text = "0", fg = "white", bg="black")
        self.LabelVitG.place(x = 10, y = i2 + height/cut)

        i3 = 2*height/5 + 20
        Label(self.canvas_aff, text = "Vit suivant axe:", fg="white", bg="black").place(x = 10, y = i3)
        self.LabelVitX = Label(self.canvas_aff, text = "Vx = ", fg = "white", bg = "black")
        self.LabelVitX.place(x = 10, y = i3+height/cut)
        self.LabelVitY = Label(self.canvas_aff, text = "Vy = ", fg = "white", bg = "black")
        self.LabelVitY.place(x = 10, y = i3+2*height/cut)
        self.LabelVitZ = Label(self.canvas_aff, text = "Vz = ", fg = "white", bg = "black")
        self.LabelVitZ.place(x = 10, y = i3+3*height/cut)

        i4 = 3*height/5 + 20
        Label(self.canvas_aff, text = "Position suivant axe:", fg="white", bg="black").place(x = 10, y = i4)
        self.LabelX = Label(self.canvas_aff, text = "x = ", fg = "white", bg = "black")
        self.LabelX.place(x = 10, y = i4+height/cut)
        self.LabelY = Label(self.canvas_aff, text = "y = ", fg = "white", bg = "black")
        self.LabelY.place(x = 10, y = i4+2*height/cut)
        self.LabelZ = Label(self.canvas_aff, text = "z = ", fg = "white", bg = "black")
        self.LabelZ.place(x = 10, y = i4+3*height/cut)


    def output_var(self):
        f = lambda x:str(round(x, 3))
        self.LabelAcc["text"] = f(self.parent.a_re) + " m/s²"
        self.LabelVitG["text"] = f(self.parent.speed_re) + " m/s"

        self.LabelVitX["text"] = "Vx = " + f(self.parent.speed_x) + " m/s"
        self.LabelVitY["text"] = "Vy = " + f(self.parent.speed_y) + " m/s"
        self.LabelVitZ["text"] = "Vz = " + f(self.parent.speed_z) + " m/s"

        self.LabelX["text"] = "x = " + f(self.parent.coor[0][0]) + " m"
        self.LabelY["text"] = "y = " + f(self.parent.coor[0][1]) + " m"
        self.LabelZ["text"] = "z = " + f(self.parent.coor[0][2]) + " m"

        #print(np.matrix(self.parent.coor))
