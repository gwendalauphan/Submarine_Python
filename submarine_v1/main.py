from tkinter import*
import tkinter as tk
import numpy as np
import time 
from time import sleep
from math import *
from plot_1 import*
from plot_2 import*
from plot_3 import*
from plot_4 import*
from plot_3d.plot_5 import*
from plot_6 import*
from multi_process import*


win = Tk()
win.title("Projet")
win.focus_force()
win.wm_state(newstate="zoomed")	# Affiche la fenetre principale en plein écran
win_height=win.winfo_screenheight()
win_width=win.winfo_screenwidth()
print(win_height, win_width)


"""
rotation à partir de l'axe z


matrice_par_z = np.array([[cos(teta), -sin(teta), 0]
                          [sin(teta),  cos(teta), 0]
                          [0,          0,         1]])

matrice_par_y = np.array([[cos(teta),  0, sin(teta)]
                          [0,          1,         0]
                          [-sin(teta), 0, cos(teta)]])

matrice_par_x = np.array([[1,          0,         0]
                          [0, cos(teta), -sin(teta)]
                          [0, sin(teta),  cos(teta)]])


"""

class submarine:
    def __init__(self, win, height, width, length, weight, power,  x,y,z, temp):

        self.win = win
        self.win.bind("<Key>", self.rotate)
        self.multiprocess_1 = multiprocess(self)


        self.liste_acc_relatif, self.liste_v_relatif = [], []
        self.liste_acc_x, self.liste_acc_y, self.liste_acc_z = [],[],[]
        self.liste_v_x, self.liste_v_y, self.liste_v_z = [],[],[]
        self.liste_time = []

        #Caractéristiques du SOUS MARIN
        self.height = height
        self.width = width
        self.length = length
        self.weight = weight
        self.power = power
        self.temp = temp
        self.tr_min = 0
        self.radius_helice = 0.05
        self.var =0
        self.gouvernail = 0
        self.angle_boussole = 0
        self.angle_boussole_2 = 0

        #Variables importantes
        self.g = 9.80665 #m/s2 : accélération de pesanteur
        self.ρ_eau = 1000.00 #kg/m−3 : masse volumique de l'eau sous 10°
        self.μ_eau = 0.001 #(Pa.s) ou (N.s / m²) : viscosité dynamique de l'eau
        self.volume = pi*((self.width/2)**2)*self.length #m3
        self.ratio_l_d = self.length/(self.width)
        self.liste_weight_water= np.linspace(0,1,100)
        self.i = 0
        self.weight_water = self.liste_weight_water[self.i]

        self.Cxlin_y = self.Cxlin_z = (4*pi)/(log(2*self.ratio_l_d)+0.193)
        self.Cxlin_x = (4*pi*(self.ratio_l_d**2 - 1))/(((2*self.ratio_l_d**2 - 1)*log(self.ratio_l_d + sqrt(self.ratio_l_d**2 - 1)))/sqrt(self.ratio_l_d**2 - 1) - self.ratio_l_d)
        self.speed_re = 0
        self.speed_z,self.speed_y,self.speed_x = 0,0,0

        #Formules importantes
        self.Pa = self.ρ_eau*self.volume*self.g #Poussée d'Archimède: Pa = ρ.V.g
        self.Pm = self.g*(self.weight+self.weight_water) #Force éxercée par le sous marin #VARIABLE

        self.force_frot_fluides_z = self.μ_eau*self.speed_z*self.length*(self.Cxlin_y)*10
        self.force_frot_fluides_y = self.μ_eau*self.speed_re*self.length*(self.Cxlin_z)*10
        self.force_frot_fluides_x = self.μ_eau*self.speed_re*self.length*(self.Cxlin_x)*1000
        self.force_elice = self.ρ_eau*((self.tr_min/60)**3)*((self.radius_helice*2)**4)
        print(self.force_frot_fluides_y,self.force_frot_fluides_x,self.force_frot_fluides_z)

        #Différentes accélérations
        self.a_z = (self.Pm - self.Pa - self.force_frot_fluides_y)/self.weight
        self.a_re = (self.force_elice - self.force_frot_fluides_x)/self.weight
        self.a_x, self.a_y = 0,0

        #Initialisation des angles
        self.angle_rotate_par_x, self.angle_rotate_par_y,self.angle_rotate_par_z = pi/60,pi/60,pi/60
        self.angle_par_z, self.angle_par_y, self.angle_par_x  = 0,0,0



        #Initialisation des Coordonnées et Vecteurs
        self.x = x
        self.y = y
        self.z = z
        self.vect = np.array([1.00,0.00,0.00]).reshape(1,3)

        self.coor = np.array([x,y,z]).reshape(1,3)


        win_height=self.win.winfo_screenheight()
        win_width=self.win.winfo_screenwidth()

        self.Frame_main = Frame(self.win)
        self.Frame_main.pack(fill = "both", expand = True)
        self.Frame_top = Frame(self.Frame_main, height = win_height/2, width = win_width )
        self.Frame_top.pack(side = TOP,fill = "both")
        self.Frame_bottom = Frame(self.Frame_main, height = win_height/2, width = win_width)
        self.Frame_bottom.pack(side = BOTTOM,fill = "both")

        self.Frame_top_right = Frame(self.Frame_top, height = win_height/2, width = 6*win_width/16 ,bg ='black')
        self.Frame_top_right.pack( side = RIGHT ,fill = "both")
        self.Frame_top_center =Frame(self.Frame_top, height = win_height/2, width = win_width/8 ,bg ='pink')
        self.Frame_top_center.pack( side = RIGHT ,fill = "both")
        self.Frame_top_left = Frame(self.Frame_top,height = win_height/2, width = win_width/2,bg ='green')
        self.Frame_top_left.pack( side = LEFT ,fill = "both")

        self.Frame_bottom_right = Frame(self.Frame_bottom,height = win_height/2, width = win_width/2)
        self.Frame_bottom_right.pack(side = RIGHT,fill = "both")

        self.Frame_bottom_left = Frame(self.Frame_bottom,height = win_height/2, width = win_width/2, bg ="white")
        self.Frame_bottom_left.pack(side = LEFT,fill = "both", expand =True)

        self.Frame_bottom_right_right = Frame(self.Frame_bottom_right,height = win_height/2, width = win_width/4)
        self.Frame_bottom_right_right.pack(side = RIGHT,fill = "both")

        self.Frame_bottom_right_left = Frame(self.Frame_bottom_right,height = win_height/2, width = win_width/4)
        self.Frame_bottom_right_left.pack(side = LEFT,fill = "both")

        self.matrice_par_z = np.array([cos(self.angle_par_z), -sin(self.angle_par_z), 0,
                                       sin(self.angle_par_z),  cos(self.angle_par_z), 0,
                                       0,                0,             1]).reshape(3,3)

        self.matrice_par_y = np.array([cos(self.angle_par_y),  0, sin(self.angle_par_y),
                                   0,                     1,                    0,
                                  -sin(self.angle_par_y), 0, cos(self.angle_par_y)]).reshape(3,3)

        self.matrice_par_x = np.array([1,                     0,                     0,
                                  0, cos(self.angle_par_x), -sin(self.angle_par_x),
                                  0, sin(self.angle_par_x),  cos(self.angle_par_x)]).reshape(3,3)


        self.plot_1 = plot_one(self, win_width, win_height, self.height, self.width ,self.Frame_bottom_right_left)
        self.plot_2 = plot_two(self, win_width, win_height, self.height, self.width ,self.Frame_top_right) #Frame_top_right
        self.plot_3 = plot_three(self, win_width, win_height, self.height, self.width, self.Frame_bottom_right_right)
        self.plot_5 = plot_five(self.win,self, win_width,win_height, self.Frame_top_left)
        self.plot_4 = plot_four(self.win, self, win_width,win_height, self.Frame_bottom_left)
        self.plot_6 = plot_six_central(self.win, self, win_width, win_height, self.Frame_top_center)


        self.t1 = time.time()
        self.t2 = 0
        self.t3 = 0.01
        self.update()

    def rotate(self, event = None): #fonction appelée par appuis d'une touche
        symb = event.keysym

        if symb == "Right": #selon l'axe x
            if self.gouvernail > -pi/4:
                self.gouvernail -= self.angle_rotate_par_z
        elif symb == "Left": #selon l'axe x φ
            if self.gouvernail < pi/4:
                self.gouvernail += self.angle_rotate_par_z
        elif symb == "Down": #
            if self.i <99:
                self.i +=1
        elif symb == "Up":
            if self.i >0:
                self.i -=1
        elif symb == "z": #selon l'axe z ψ
            if self.tr_min <200:
                self.tr_min +=10

        elif symb == "s": #selon l'axe z
            if self.tr_min > -200:
                self.tr_min -=10


        self.plot_1.rotate_plot()

    def update(self):
        if self.var == 0:
            self.depart = time.time()

        #Calcul pour les coord de y
        self.weight_water = self.liste_weight_water[self.i]
        if self.weight_water > 1:
            self.weight_water = 1
        self.Pm = self.g*(self.weight+self.weight_water)
        self.force_frot_fluides_y = self.μ_eau*(self.speed_z)*self.length*(self.Cxlin_y)*10
        self.a_z = ((self.Pm - self.Pa + self.force_frot_fluides_y)/(self.weight+self.weight_water))
        self.speed_z -= self.a_z*self.t3
        if self.z <= 0 and self.speed_z >= 0:
            self.z = 0
            self.speed_z = 0
            self.a_z = 0

        #Calcul pour les coord de x (relatif)
        self.force_frot_fluides_x = self.μ_eau*self.speed_re*self.length*(self.Cxlin_x)*100 + self.force_frot_fluides_z*abs(self.angle_rotate_par_z)*100
        self.force_elice = self.ρ_eau*((self.tr_min/60)**3)*((self.radius_helice*2)**4)
        self.a_re = (self.force_elice - self.force_frot_fluides_x)/(self.weight+self.weight_water)
        self.speed_re += self.a_re*self.t3


        #calcul pour virage selon z
        self.z-=self.speed_z*self.t3

        if self.speed_re !=0:
            self.angle_par_z += self.gouvernail/10
            self.angle_par_z = self.angle_par_z/(10*(((self.speed_re-1)**2)/(2*self.speed_re)+1.5))



        self.matrice_rotation = np.array([cos(self.angle_par_z)*cos(self.angle_par_y), -sin(self.angle_par_z)*cos(self.angle_par_x) + sin(self.angle_par_x)*cos(self.angle_par_z)*sin(self.angle_par_y),  sin(self.angle_par_x)*sin(self.angle_par_z) + sin(self.angle_par_y)*cos(self.angle_par_z)*cos(self.angle_par_x),
                                          cos(self.angle_par_y)*sin(self.angle_par_z),       cos(self.angle_par_z)*cos(self.angle_par_x) + sin(self.angle_par_y)*sin(self.angle_par_z)*sin(self.angle_par_x),       -cos(self.angle_par_z)*sin(self.angle_par_x) + cos(self.angle_par_x)*sin(self.angle_par_y)*sin(self.angle_par_z),
                                         -sin(self.angle_par_y),                           cos(self.angle_par_y)*sin(self.angle_par_x),                                                                          cos(self.angle_par_y)*cos(self.angle_par_x)]).reshape(3,3)

        self.vect = self.vect.dot(self.matrice_rotation)
        self.coor += self.speed_re*(self.vect)*self.t3
        self.coor[0][2] = -self.z

        self.speed_x, self.speed_y = self.speed_re*self.vect[0][0], self.speed_re*self.vect[0][1]
        self.a_x, self.a_y = self.a_re*self.vect[0][0], self.a_re*self.vect[0][1]

        if self.var%50==0:
            self.plot_4.update_graph()
            self.plot_6.output_var()
            self.plot_5.update_sub()

        if self.var%10==0:
            #self.multiprocess_1.start(self.var)
            self.plot_2.update()
            self.plot_3.rotate_boussole()
            self.angle_boussole_2 -= self.angle_boussole_2*self.t3

            #print(self.x, self.a_re, self.speed_re,self.force_frot_fluides_x, self.tr_min)
            #print(self.z,self.a_z, self.speed_z, self.force_frot_fluides_y, self.liste_weight_water[self.i])
            #print(self.x,self.y,self.z)
            #print(self.speed_re,self.coor,self.gouvernail,self.speed_z, self.tr_min)
            #print(self.vect.dot(self.matrice_rotation))
            #print(self.speed_re,self.vect,self.angle_par_z, self.gouvernail,self.coor)
            #print(self.angle_boussole,self.gouvernail, self.angle_par_z)
            #print(self.liste_acc_relatif)
            #print(self.liste_time)

        if self.plot_4.v.get() == 1:
            self.liste_acc_x.append(self.a_x)
            self.liste_acc_y.append(self.a_y)
            self.liste_acc_z.append(self.a_z)
        elif self.plot_4.v.get() == 0:
            self.liste_v_x.append(self.speed_x)
            self.liste_v_y.append(self.speed_y)
            self.liste_v_z.append(self.speed_z)

        elif self.plot_4.v.get() == 2:
            self.liste_acc_relatif.append(self.a_re)
            self.liste_v_relatif.append(self.speed_re)

        self.liste_time.append(self.t2)

        if len(self.liste_time)>1000:
            del self.liste_time[0]

        if len(self.liste_v_x)>1000:
            del self.liste_v_x[0]
            del self.liste_v_y[0]
            del self.liste_v_z[0]

        if len(self.liste_acc_x)>1000:
            del self.liste_acc_x[0]
            del self.liste_acc_y[0]
            del self.liste_acc_z[0]

        if len(self.liste_acc_relatif)>1000:
            del self.liste_acc_relatif[0]
            del self.liste_v_relatif[0]


        if self.angle_boussole_2 > -pi/4 and self.angle_boussole_2 < pi/4:
            self.angle_boussole_2 +=self.gouvernail/5

        self.angle_boussole += self.angle_par_z
        #Code pour le gouvernail se remettre droit
        if 0.05 > self.gouvernail > -0.05:
            self.gouvernail = 0
            self.angle_par_z = 0
        else:
            self.gouvernail -= self.gouvernail/10
            self.angle_par_z -= self.angle_par_z/10

        self.var+=1

        self.t2 = time.time() - self.depart
        self.t3 = time.time() - self.t1
        self.t1 = time.time()
        self.win.after(10, self.update)


if __name__ == '__main__':
    sub1 = submarine(win,0.15,0.15,0.6,10,0,0.00,0.00,5.00,0)


win.mainloop()
