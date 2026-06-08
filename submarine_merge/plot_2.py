from tkinter import*


class plot_two:
    def __init__(self, parent,win_width, win_height, height,width, Frame):
        self.parent = parent
        self.height = height
        self.width = width
        self.win_width = win_width
        self.win_height = win_height
        self.Frame = Frame
        self.carte = Canvas(self.Frame, height = self.win_height/2, width = 6*self.win_width/16, highlightthickness = 0, bg = 'black')
        self.carte.pack()
        self.point = self.carte.create_oval(-5,self.win_height/2-5,5,self.win_height/2+5, fill = 'red')

    def update(self):
        x = round(self.parent.coor[0][0] * 10, 3)
        y = round(self.parent.coor[0][1] * 10, 3)
        self.carte.coords(
            self.point,
            x - 5,
            self.win_height / 2 + y - 5,
            x + 5,
            self.win_height / 2 + y + 5,
        )
