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


class myArrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        FancyArrowPatch.draw(self, renderer)

class plot_five:
    def __init__(self,win, parent,win_width, win_height ,Frame ):
        self.win = win
        self.win.protocol("WM_DELETE_WINDOW", self.close)
        self.parent = parent
        self.win_width = win_width
        self.win_height = win_height
        self.Frame = Frame
        self.angle_hor = 0
        self.angle_ver = 0
        self.angle_roulis = 0
        self.n = 0
        self.scale = 1
        self.vect_view = np.array([1,0,0]).reshape(1,3).dot(self.matrice(self.angle_roulis,self.angle_ver,self.angle_hor))
        self.coor_view = np.array([0.0,0.0,0.0]).reshape(1,3)
        self.map = create_map()

        #Import des photos
        self.run = PhotoImage(file = "E:/submarine/ressources/run.png")
        self.back = PhotoImage(file = "E:/submarine/ressources/back.png")
        self.arrow_top = PhotoImage(file = "E:/submarine/ressources/arrow_top.png")
        self.arrow_right = PhotoImage(file = "E:/submarine/ressources/arrow_right.png")
        self.arrow_down = PhotoImage(file = "E:/submarine/ressources/arrow_down.png")
        self.arrow_left = PhotoImage(file = "E:/submarine/ressources/arrow_left.png")

        #Canvas Principale
        self.canvas_3d = Canvas(self.Frame, height = self.win_height/2, width = 7*self.win_height/16, highlightthickness = 0)
        self.canvas_3d.pack(fill=tk.BOTH, expand= True)

        #Canvas droite DEP
        self.canvas_bis_bis = Canvas(self.canvas_3d, height = self.win_height/2, width = 100, highlightthickness = 0)
        self.canvas_bis_bis.pack(side = RIGHT,fill=tk.BOTH, expand= True)
        self.canvas_bis_bis.create_text(50,8, anchor = CENTER, text = "Déplacement")
        self.canvas_bis_bis.create_text(50,21, anchor = CENTER, text = "de la carte 3d")

        #Canvas droite ROT
        self.canvas_bis = Canvas(self.canvas_3d, height = self.win_height/2, width = 100, highlightthickness = 0)
        self.canvas_bis.pack(side = RIGHT,fill=tk.BOTH, expand= True)
        self.canvas_bis.create_text(50,8, anchor = CENTER, text = "Rotation")
        self.canvas_bis.create_text(50,21, anchor = CENTER, text = "de la carte 3d")

        #Création des boutons de rotation et de déplacement
        self.canvas_bis.create_rectangle(-1,29,100,181, outline = 'black')
        self.button_arrow_top = Button(self.canvas_bis,image = self.arrow_top, highlightthickness=0, borderwidth = 0 ,cursor ='hand2', command = lambda: self.update_graph_rot_ver(0)).place(x = 25, y = 30)
        self.button_arrow_right = Button(self.canvas_bis,image = self.arrow_right, highlightthickness=0, borderwidth = 0 ,cursor ='hand2',command = lambda: self.update_graph_rot_hor(0)).place(x = 49, y = 80)
        self.button_arrow_down = Button(self.canvas_bis,image = self.arrow_down, highlightthickness=0, borderwidth = 0 ,cursor ='hand2', command = lambda: self.update_graph_rot_ver(1)).place(x = 25, y = 130)
        self.button_arrow_left = Button(self.canvas_bis,image = self.arrow_left, highlightthickness=0, borderwidth = 0 ,cursor ='hand2', command = lambda: self.update_graph_rot_hor(1)).place(x = 1, y = 80)

        self.canvas_bis_bis.create_rectangle(0,29,100,181, outline = 'black')
        self.button_arrow_top_bis = Button(self.canvas_bis_bis,image = self.run, highlightthickness=0, borderwidth = 0 ,cursor ='hand2', command = lambda: self.update_graph_dep(0)).place(x = 1, y = 30)
        self.button_arrow_down_bis = Button(self.canvas_bis_bis,image = self.back, highlightthickness=0, borderwidth = 0 ,cursor ='hand2', command = lambda: self.update_graph_dep(1)).place(x = 49, y = 30)
        self.button_arrow_right_bis = Button(self.canvas_bis_bis,image = self.arrow_right, highlightthickness=0, borderwidth = 0 ,cursor ='hand2',command = lambda: self.update_graph_dep(2)).place(x = 49, y = 80)
        self.button_arrow_left_bis = Button(self.canvas_bis_bis,image = self.arrow_left, highlightthickness=0, borderwidth = 0 ,cursor ='hand2', command = lambda: self.update_graph_dep(3)).place(x = 1, y = 80)
        self.button_arrow_run_bis = Button(self.canvas_bis_bis,image = self.arrow_top, highlightthickness=0, borderwidth = 0 ,cursor ='hand2', command = lambda: self.update_graph_dep(4)).place(x = 1, y = 130)
        self.button_arrow_back_bis = Button(self.canvas_bis_bis,image = self.arrow_down, highlightthickness=0, borderwidth = 0 ,cursor ='hand2', command = lambda: self.update_graph_dep(5)).place(x = 49, y = 130)

        #Echelles de la sensi
        self.sensi = Scale(self.canvas_bis, orient='horizontal', from_=0, to=20,resolution=1, tickinterval=10, length=100, label='Sensibilité ROT', cursor ='hand2')
        self.sensi.place(x = 50, y =225, anchor = CENTER)
        self.sensi.set(5)
        self.sensi_bis = Scale(self.canvas_bis_bis, orient='horizontal', from_=0, to=20,resolution=1, tickinterval=10, length=100, label='Sensibilité DEP', cursor ='hand2')
        self.sensi_bis.place(x = 50, y =225, anchor = CENTER)
        self.sensi_bis.set(5)

        #Boutons du choix de centrage
        self.v = tk.IntVar()
        self.v.set(1)
        self.choix = [("Centré sur sous-marin",1), ("Mode libre",2)]
        self.canvas_bis.create_rectangle(-1,268,100,320, outline = 'black')
        self.canvas_bis_bis.create_rectangle(0,268,100,320, outline = 'black')
        self.canvas_bis.create_text(50,275, text = "Centré sur", anchor = CENTER)
        self.canvas_bis.create_text(50,285, text = "sous-marin", anchor = CENTER)
        self.canvas_bis_bis.create_text(50,275, text = "Mode", anchor = CENTER)
        self.canvas_bis_bis.create_text(50,285, text = "libre", anchor = CENTER)
        tk.Radiobutton(self.canvas_bis,variable=self.v,command= self.centre_map,value=self.choix[0][1], cursor ='hand2').place(x = 50, y = 305, anchor = CENTER)
        tk.Radiobutton(self.canvas_bis_bis,variable=self.v,command=self.centre_map,value=self.choix[1][1], cursor ='hand2').place(x = 50, y = 305, anchor = CENTER)

        #Boutons ZOOM et DEZOOM
        self.zoom = Button(self.canvas_bis, text = "AGRANDIRE", command = lambda: self.ZOOM(1), cursor ='hand2').place(x = 48, y = 338, anchor = CENTER)
        self.dezoom = Button(self.canvas_bis_bis, text = "RETRECIRE", command = lambda: self.ZOOM(0), cursor ='hand2').place(x = 52, y = 338, anchor = CENTER)
        self.label1 = Label(self.canvas_bis, text = "X").place(x = 90, y = 330)
        self.label2 = Label(self.canvas_bis_bis, text = "1")
        self.label2.place(x = 0, y = 330)
        self.canvas_bis.create_line(0,355,100,355, fill = 'black')
        self.canvas_bis_bis.create_line(0,355,100,355, fill = 'black')

        #Boutons de l'affichage du plot
        self.CheckVar1 = IntVar()
        self.CheckVar2 = IntVar()
        self.CheckVar1.set(0)
        self.CheckVar2.set(1)
        self.C1 = Checkbutton(self.canvas_bis, text = "Plan", variable = self.CheckVar1, onvalue = 1, offvalue = 0,command = self.state_1, cursor ='hand2')
        self.C2 = Checkbutton(self.canvas_bis_bis, text = "Lignes", variable = self.CheckVar2, onvalue = 1, offvalue = 0,command = self.state_2, cursor ='hand2')
        self.C1.place(x = 50, y = 370, anchor = CENTER)
        self.C2.place(x = 50, y = 370, anchor = CENTER)

        #Début de plot
        plt.style.use('dark_background')
        self.fig_1 = figure(num=None, figsize=(10, 3), dpi=80)
        self.ax_1 = self.fig_1.gca(projection='3d')
        self.ax_1.set_title("Vision 3D du sous-marin dans l'eau", weight = 'bold')

        self.graph_3d = FigureCanvasTkAgg(self.fig_1, self.canvas_3d)
        self.graph_3d.get_tk_widget().pack(side = LEFT,  fill=tk.BOTH)

        #Data
        self.points = self.map.array_points()
        self.points[:,2] -= np.max(self.points[:,2])
        self.max = np.array([np.max(self.points[:,0]), np.max(self.points[:,1]), np.max(self.points[:,2])]).reshape(1,3)
        self.min = np.array([np.min(self.points[:,0]), np.min(self.points[:,1]), np.min(self.points[:,2])]).reshape(1,3)

        self.triang = mtri.Triangulation(self.points[:,0], self.points[:,1])
        #self.ax_1.scatter(self.points[:,0], self.points[:,1], self.points[:,2] )
        self.surf = self.ax_1.plot_trisurf(self.triang, self.points[:,2], cmap='jet', alpha = 0.5)


        #Couleur et transparence des panneaux plot
        self.ax_1.xaxis.set_pane_color((0.93, 0.93, 0.93, 0.0))
        self.ax_1.yaxis.set_pane_color((0.93, 0.93, 0.93, 0.0))
        self.ax_1.zaxis.set_pane_color((0.93, 0.93, 0.93, 0.0))

        # make the grid lines transparent
        self.ax_1.xaxis._axinfo["grid"]['color'] =  (0.93, 0.93, 0.93,0.2)
        self.ax_1.yaxis._axinfo["grid"]['color'] =  (0.93, 0.93, 0.93,0.2)
        self.ax_1.zaxis._axinfo["grid"]['color'] =  (0.93, 0.93, 0.93,0.2)

        self.ax_1.zaxis.set_major_locator(LinearLocator(10))
        self.ax_1.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
        self.ax_1.view_init(elev = self.angle_ver, azim = self.angle_hor)

        #Définition des axes
        self.ax_1.set_xlabel('X')
        self.ax_1.set_ylabel('Y')
        self.ax_1.set_zlabel('Z')

        #Colorbar
        cax = self.fig_1.add_axes([0.2, 0.05, 0.6, 0.04])
        self.fig_1.colorbar(self.surf,cax=cax,  orientation='horizontal', extend='both',shrink=0.5, aspect=5)

        self.ax_1.set_zlim(self.min[0][2],self.max[0][2])

        #Création du sous-marin
        self.sub = self.ax_1.scatter3D(self.parent.coor[0][0],self.parent.coor[0][1],self.parent.coor[0][2],  s = 40, c = 'white', alpha = 1)

        self.arrow_sub = myArrow3D([self.parent.coor[0][0] - self.parent.vect[0][0]*self.scale*3,self.parent.coor[0][0]] + self.parent.vect[0][0]*self.scale*3\
                                  ,[self.parent.coor[0][1] - self.parent.vect[0][1]*self.scale*3,self.parent.coor[0][1]] + self.parent.vect[0][1]*self.scale*3\
                                  ,[self.parent.coor[0][2] - self.parent.vect[0][2]*self.scale*3,self.parent.coor[0][2]] + self.parent.vect[0][2]*self.scale*3\
                                  , mutation_scale=10, lw=4, arrowstyle="fancy", color="white", alpha = 1)
        self.ax_1.add_artist(self.arrow_sub)
        self.fig_1.canvas.draw()

    def state_1(self): #Transparence du plan
        transparence = 0
        if self.CheckVar1.get() == 1:
            transparence = 0.2
        self.ax_1.xaxis.set_pane_color((0.93, 0.93, 0.93, transparence))
        self.ax_1.yaxis.set_pane_color((0.93, 0.93, 0.93, transparence))
        self.ax_1.zaxis.set_pane_color((0.93, 0.93, 0.93, transparence))

    def state_2(self): #Transparence des lignes
        transparence = 0
        if self.CheckVar2.get() == 1:
            transparence = 0.2
        self.ax_1.xaxis._axinfo["grid"]['color'] =  (0.93, 0.93, 0.93,transparence)
        self.ax_1.yaxis._axinfo["grid"]['color'] =  (0.93, 0.93, 0.93,transparence)
        self.ax_1.zaxis._axinfo["grid"]['color'] =  (0.93, 0.93, 0.93,transparence)

    def close(self): #Ferme les graphs et la fenetre
        plt.close()
        plt.close()

    def matrice(self,x,y,z): #Matrice de rotation
        return np.array([cos(z)*cos(y), -sin(z)*cos(x) + sin(x)*cos(z)*sin(y),  sin(x)*sin(z) + sin(y)*cos(z)*cos(x),
                                          cos(y)*sin(z),       cos(z)*cos(x) + sin(y)*sin(z)*sin(x),       -cos(z)*sin(x) + cos(x)*sin(y)*sin(z),
                                         -sin(y),                           cos(y)*sin(x),                  cos(y)*cos(x)]).reshape(3,3)

    def update_graph_rot_hor(self, a): #ROT de la view
        if a == 0:
            self.angle_hor +=self.sensi.get()
            self.vect_view = self.vect_view.dot(self.matrice(0,0, (self.sensi.get()*pi)/180))
        else:
            self.angle_hor -=self.sensi.get()
            self.vect_view = self.vect_view.dot(self.matrice(0, 0, -(self.sensi.get()*pi)/180))

        self.ax_1.view_init(elev = self.angle_ver, azim = self.angle_hor)
        print(self.angle_ver, self.angle_hor)
        #print(self.vect_view)

        self.fig_1.canvas.draw()

    def update_graph_rot_ver(self,a): #ROT de la view
        if a == 0:
            self.angle_ver +=self.sensi.get()
            if self.angle_ver > 90:
                self.angle_ver = 90
            else:
                self.vect_view = self.vect_view.dot(self.matrice(0, (self.sensi.get()*pi)/180, 0))
        else:
            self.angle_ver -=self.sensi.get()
            if self.angle_ver < -40:
                self.angle_ver = -40
            else:
                self.vect_view = self.vect_view.dot(self.matrice(0, -(self.sensi.get()*pi)/180, 0))
        self.ax_1.view_init(elev = self.angle_ver, azim = self.angle_hor)
        self.fig_1.canvas.draw()

    def ZOOM(self, a):
        if a ==1:
            self.n+=1
        else:
            self.n-=1
        self.scale = 2**self.n
        self.label2["text"] = str(self.scale)
        if self.v.get() == 2:
            self.ax_1.set_xlim(self.min[0][0]/self.scale,self.max[0][0]/self.scale)
            self.ax_1.set_ylim(self.max[0][1]/self.scale,self.min[0][1]/self.scale)

    def update_graph_dep(self, a): #DEP
        if self.v.get() == 2:
            self.coor_view = np.array([0.0,0.0,0.0]).reshape(1,3)
            if a == 0: #Déplacement en avant
                self.coor_view[0][0] = -cos(self.angle_hor*pi/180)
                self.coor_view[0][1] = -sin(self.angle_hor*pi/180)
            elif a == 1: #Déplacement en arrière
                self.coor_view[0][0] = cos(self.angle_hor*pi/180)
                self.coor_view[0][1] = sin(self.angle_hor*pi/180)

            elif a == 2: #Déplacement sur la gauche
                self.coor_view[0][0] = cos(self.angle_hor*pi/180+ pi/2)
                self.coor_view[0][1] = sin(self.angle_hor*pi/180+ pi/2)

            elif a == 3: #Déplacement sur la droite
                self.coor_view[0][0] = -cos(self.angle_hor*pi/180+ pi/2)
                self.coor_view[0][1] = -sin(self.angle_hor*pi/180+ pi/2)

            elif a == 4: #Déplacement vers le haut
                self.coor_view[0][0] = cos(self.angle_hor*pi/180)*cos(self.angle_ver*pi/180 + pi/2)
                self.coor_view[0][1] = sin(self.angle_hor*pi/180)*cos(self.angle_ver*pi/180 + pi/2)
                self.coor_view[0][2] =  cos(self.angle_ver*pi/180)

            elif a == 5: #Déplacement vers le bas
                self.coor_view[0][0] = -cos(self.angle_hor*pi/180)*cos(self.angle_ver*pi/180 + pi/2)
                self.coor_view[0][1] = -sin(self.angle_hor*pi/180)*cos(self.angle_ver*pi/180 + pi/2)
                self.coor_view[0][2] =  -cos(self.angle_ver*pi/180)


            self.min,self.max = self.min + self.coor_view*self.sensi_bis.get(),self.max + self.coor_view*self.sensi_bis.get()
            self.ax_1.set_xlim(self.min[0][0]/self.scale,self.max[0][0]/self.scale)
            self.ax_1.set_ylim(self.max[0][1]/self.scale,self.min[0][1]/self.scale)
            self.ax_1.set_zlim(self.min[0][2],self.max[0][2])

    def centre_map(self):
        self.n = 0
        #Recentrage de la carte en 0,0,0
        if self.v.get() == 2:
            self.min[0][0],self.max[0][0] = np.min(self.points[:,0])/self.scale, np.max(self.points[:,0])/self.scale
            self.min[0][1],self.max[0][1] = np.min(self.points[:,1])/self.scale, np.max(self.points[:,1])/self.scale
            self.min[0][2],self.max[0][2] = np.min(self.points[:,2])/self.scale, np.max(self.points[:,2])/self.scale
            self.ax_1.set_xlim(self.min[0][0],self.max[0][0])
            self.ax_1.set_ylim(self.max[0][1],self.min[0][1])
            self.ax_1.set_zlim(self.min[0][2],self.max[0][2])

    def update_sub(self):
        #Calcul des limites si centré sur sous-marin
        if self.v.get() == 1:
            self.min[0][0],self.max[0][0] = self.parent.coor[0][0]-20/self.scale , self.parent.coor[0][0]+20/self.scale
            self.min[0][1],self.max[0][1] = self.parent.coor[0][1]-20/self.scale , self.parent.coor[0][1]+20/self.scale
            self.min[0][2],self.max[0][2] = self.parent.coor[0][2]-20/self.scale , self.parent.coor[0][2]+20/self.scale
            self.ax_1.set_xlim(self.min[0][0], self.max[0][0])
            self.ax_1.set_ylim(self.max[0][1],self.min[0][1])
            #self.ax_1.set_zlim(self.min[0][2], self.max[0][2])
        self.sub.remove()
        self.arrow_sub.remove()
        print(self.parent.coor[0][0] - self.parent.vect[0][0]*self.scale*3)
        self.arrow_sub = myArrow3D([self.parent.coor[0][0] - self.parent.vect[0][0]*self.scale*3,self.parent.coor[0][0]] + self.parent.vect[0][0]*self.scale*3\
                                  ,[self.parent.coor[0][1] - self.parent.vect[0][1]*self.scale*3,self.parent.coor[0][1]] + self.parent.vect[0][1]*self.scale*3\
                                  ,[self.parent.coor[0][2] - self.parent.vect[0][2]*self.scale*3,self.parent.coor[0][2]] + self.parent.vect[0][2]*self.scale*3\
                                  , mutation_scale=10, lw=2, arrowstyle="fancy", color="white", alpha = 1)
        self.ax_1.add_artist(self.arrow_sub)
        self.sub = self.ax_1.scatter3D(self.parent.coor[0][0],self.parent.coor[0][1],self.parent.coor[0][2], s = 40, c = 'white', alpha = 1)
        self.fig_1.canvas.draw()
