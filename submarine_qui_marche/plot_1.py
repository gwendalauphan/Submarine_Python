from tkinter import*
from math import cos,sin



class plot_one:
    def __init__(self, parent,win_width, win_height, height,width,  Frame):
        self.parent = parent
        self.height = height
        self.width = width
        self.win_width = win_width
        self.win_height = win_height
        self.Frame = Frame

        self.position_back = Canvas(self.Frame, height = self.win_height/2, width = self.win_width/4, highlightthickness = 0, bg = 'white')
        self.position_back.pack()
        self.position_back.create_line(0,self.win_height/4, self.win_width/4, self.win_height/4,  dash=(3, 3), fill ='green')
        self.position_back.create_line(self.win_width/8, 0, self.win_width/8, self.win_height/2,  dash=(3, 3), fill ='green')

        self.position_back.create_oval(self.win_width/8 - self.win_width/16, self.win_height/4 -self.win_width/16, self.win_width/8 + self.win_width/16, self.win_height/4 + self.win_width/16, dash=(3, 3), outline = 'red')
        self.rot_x_1 = self.position_back.create_line(self.win_width/8 ,  self.win_height/4 , self.win_width/8- cos(self.parent.angle_par_x)*self.win_width/16,self.win_height/4 + sin(self.parent.angle_par_x)*self.win_width/16 , fill ='red')
        self.rot_x_2 = self.position_back.create_line(self.win_width/8 ,  self.win_height/4 , self.win_width/8+ cos(self.parent.angle_par_x)*self.win_width/16,self.win_height/4 - sin(self.parent.angle_par_x)*self.win_width/16 , fill ='red')
    def rotate_plot(self):
        self.position_back.delete(self.parent.win, self.rot_x_1)
        self.position_back.delete(self.parent.win, self.rot_x_2)
        self.rot_x_1 = self.position_back.create_line(self.win_width/8 ,  self.win_height/4 , self.win_width/8- cos(self.parent.angle_par_x)*self.win_width/16,self.win_height/4 + sin(self.parent.angle_par_x)*self.win_width/16 , fill ='red')
        self.rot_x_2 = self.position_back.create_line(self.win_width/8 ,  self.win_height/4 , self.win_width/8+ cos(self.parent.angle_par_x)*self.win_width/16,self.win_height/4 - sin(self.parent.angle_par_x)*self.win_width/16 , fill ='red')
