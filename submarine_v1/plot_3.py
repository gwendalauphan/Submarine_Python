from tkinter import*
import numpy as np
from math import cos,sin,pi

class plot_three:
    def __init__(self, parent,win_width, win_height, height,width, Frame):
        self.parent = parent
        self.height = height
        self.width = width
        self.win_width = win_width
        self.win_height = win_height
        self.Frame = Frame
        self.l = 3

        self.liste_orientation = ["E","SE","S","SO","O","NO","N","NE"]
        self.boussole = Canvas(self.Frame, height = self.win_height/2, width = self.win_width/4, highlightthickness = 0, bg = 'black')
        self.boussole.pack()
        self.boussole.create_line(0,self.win_height/4, self.win_width/4, self.win_height/4,  dash=(3, 3), fill ='green')
        self.boussole.create_line(self.win_width/8, 0, self.win_width/8, self.win_height/2,  dash=(3, 3), fill ='green')

        self.boussole.create_arc((1/8)*self.win_width - (1/64)*self.win_width,(1/4)*self.win_height - (10/(16*4))*self.win_height,(1/8)*self.win_width + (1/64)*self.win_width , (1/4)*self.win_height ,start = 180 ,extent=-90, outline="white")
        self.boussole.create_arc((1/8)*self.win_width - (1/64)*self.win_width,(1/4)*self.win_height - (10/(16*4))*self.win_height,(1/8)*self.win_width + (1/64)*self.win_width , (1/4)*self.win_height ,start = 90 ,extent=-90, outline="white")
        self.boussole.create_rectangle((1/8)*self.win_width - (1/64)*self.win_width,(1/4)*self.win_height - (5/(16*4))*self.win_height,(1/8)*self.win_width + (1/64)*self.win_width,(1/4)*self.win_height + (7/(16*4))*self.win_height, outline ='white')
        self.boussole.create_rectangle((1/8)*self.win_width - (1/160)*self.win_width,(1/4)*self.win_height - (5/(16*4))*self.win_height,(1/8)*self.win_width + (1/160)*self.win_width,(1/4)*self.win_height + (7/(16*4))*self.win_height, outline ='white')
        x0, y0 = (1/8)*self.win_width + (1/64)*self.win_width,(1/4)*self.win_height + (7/(16*4))*self.win_height
        x1, y1 = (1/8)*self.win_width + (1/180)*self.win_width, (1/4)*self.win_height + (8/(16*4))*self.win_height
        x2, y2 = (1/8)*self.win_width - (1/180)*self.win_width, (1/4)*self.win_height + (8/(16*4))*self.win_height
        x3, y3 = (1/8)*self.win_width - (1/64)*self.win_width, (1/4)*self.win_height + (7/(16*4))*self.win_height
        self.boussole.create_polygon(x0, y0,x1, y1,x2, y2,x3, y3, outline ="white" )
        self.boussole.create_rectangle(x2, y2, x1,  (1/4)*self.win_height + (9/(16*4))*self.win_height, outline ="white")
        self.boussole.create_line(x3, (1/4)*self.win_height + (9/(16*4))*self.win_height, x0, (1/4)*self.win_height + (9/(16*4))*self.win_height, fill ="white" )
        self.boussole.create_line((1/8)*self.win_width, y2, (1/8)*self.win_width -sin(self.parent.angle_boussole_2)*(1/45)*self.win_width, y2+ cos(self.parent.angle_boussole_2)*(1/45)*self.win_width, fill ="yellow")

        self.liste_angles =[]
        self.liste_angles_0 = np.linspace(0, 2*pi, 360)
        for a in range(len(self.liste_angles_0)):
            if a%5 == 0:
                self.liste_angles.append(self.liste_angles_0[a])

        for a,i in (enumerate(self.liste_angles)):
            if a%5==0 and a%9!=0:
                self.l = 5
            elif a%9 ==0:
                self.l = 10
                self.boussole.create_text((1/8)*self.win_width + (3/16)*self.win_height*cos(i) + cos(i)*self.l, (1/4)*self.win_height + (3/16)*sin(i)*self.win_height +sin(i)*self.l, text = self.liste_orientation[int(a/9)], fill ='red')
            else:
                self.l = 3
            liset = self.boussole.create_line((1/8)*self.win_width + (3/16)*self.win_height*cos(i),(1/4)*self.win_height - (3/16)*sin(i)*self.win_height,(1/8)*self.win_width + (3/16)*self.win_height*cos(i) - cos(i)*self.l, (1/4)*self.win_height - (3/16)*sin(i)*self.win_height +sin(i)*self.l, fill ="red")

    def rotate_boussole(self):
        x0, y0 = (1/8)*self.win_width + (1/64)*self.win_width,(1/4)*self.win_height + (7/(16*4))*self.win_height
        x1, y1 = (1/8)*self.win_width + (1/180)*self.win_width, (1/4)*self.win_height + (8/(16*4))*self.win_height
        x2, y2 = (1/8)*self.win_width - (1/180)*self.win_width, (1/4)*self.win_height + (8/(16*4))*self.win_height
        x3, y3 = (1/8)*self.win_width - (1/64)*self.win_width, (1/4)*self.win_height + (7/(16*4))*self.win_height
        for i in (self.boussole.find_all()):
            if i>len(self.boussole.find_all())-81:
                self.boussole.delete(self.parent.win, i)

        for a,i in (enumerate(self.liste_angles)):
            if a%5==0 and a%9!=0:
                self.l = 5
            elif a%9 ==0:
                self.l = 10
                self.boussole.create_text((1/8)*self.win_width + (3/16)*self.win_height*cos(i+self.parent.angle_boussole) + cos(i+self.parent.angle_boussole)*self.l, (1/4)*self.win_height + (3/16)*sin(i+self.parent.angle_boussole)*self.win_height +sin(i+self.parent.angle_boussole)*self.l, text = self.liste_orientation[int(a/9)], fill ='red')
            else:
                self.l = 3
            self.boussole.create_line((1/8)*self.win_width + (3/16)*self.win_height*cos(i-self.parent.angle_boussole),(1/4)*self.win_height - (3/16)*sin(i-self.parent.angle_boussole)*self.win_height,(1/8)*self.win_width + (3/16)*self.win_height*cos(i-self.parent.angle_boussole) - cos(i-self.parent.angle_boussole)*self.l, (1/4)*self.win_height - (3/16)*sin(i-self.parent.angle_boussole)*self.win_height +sin(i-self.parent.angle_boussole)*self.l, fill ="red")

        self.boussole.create_line((1/8)*self.win_width, y2, (1/8)*self.win_width -sin(self.parent.angle_boussole_2)*(1/45)*self.win_width, y2+ cos(self.parent.angle_boussole_2)*(1/45)*self.win_width, fill ="yellow")
