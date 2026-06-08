from tkinter import Canvas
import numpy as np
from math import cos, sin, pi

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

        self.tick_items = []
        self.label_items = []
        for a,i in (enumerate(self.liste_angles)):
            if a%5==0 and a%9!=0:
                self.l = 5
            elif a%9 ==0:
                self.l = 10
                text_id = self.boussole.create_text((1/8)*self.win_width + (3/16)*self.win_height*cos(i) + cos(i)*self.l, (1/4)*self.win_height + (3/16)*sin(i)*self.win_height +sin(i)*self.l, text = self.liste_orientation[int(a/9)], fill ='red')
                self.label_items.append((text_id, int(a/9), i))
            else:
                self.l = 3
            line_id = self.boussole.create_line((1/8)*self.win_width + (3/16)*self.win_height*cos(i),(1/4)*self.win_height - (3/16)*sin(i)*self.win_height,(1/8)*self.win_width + (3/16)*self.win_height*cos(i) - cos(i)*self.l, (1/4)*self.win_height - (3/16)*sin(i)*self.win_height +sin(i)*self.l, fill ="red")
            self.tick_items.append((line_id, i, self.l))

        self.direction_line = self.boussole.create_line((1/8)*self.win_width, y2, (1/8)*self.win_width -sin(self.parent.angle_boussole_2)*(1/45)*self.win_width, y2+ cos(self.parent.angle_boussole_2)*(1/45)*self.win_width, fill ="yellow")

    def rotate_boussole(self):
        x1, y1 = (1/8)*self.win_width + (1/180)*self.win_width, (1/4)*self.win_height + (8/(16*4))*self.win_height
        x2, y2 = (1/8)*self.win_width - (1/180)*self.win_width, (1/4)*self.win_height + (8/(16*4))*self.win_height

        for line_id, angle, tick_len in self.tick_items:
            a = angle - self.parent.angle_boussole
            self.boussole.coords(
                line_id,
                (1/8)*self.win_width + (3/16)*self.win_height*cos(a),
                (1/4)*self.win_height - (3/16)*sin(a)*self.win_height,
                (1/8)*self.win_width + (3/16)*self.win_height*cos(a) - cos(a)*tick_len,
                (1/4)*self.win_height - (3/16)*sin(a)*self.win_height + sin(a)*tick_len,
            )

        for text_id, orientation_idx, angle in self.label_items:
            a = angle + self.parent.angle_boussole
            self.boussole.coords(
                text_id,
                (1/8)*self.win_width + (3/16)*self.win_height*cos(a) + cos(a)*10,
                (1/4)*self.win_height + (3/16)*sin(a)*self.win_height + sin(a)*10,
            )
            self.boussole.itemconfig(text_id, text=self.liste_orientation[orientation_idx])

        self.boussole.coords(
            self.direction_line,
            (1/8)*self.win_width,
            y2,
            (1/8)*self.win_width - sin(self.parent.angle_boussole_2)*(1/45)*self.win_width,
            y2 + cos(self.parent.angle_boussole_2)*(1/45)*self.win_width,
        )
