from plot_3d.perlin import*
import math
import numpy as np


class create_map:
    def __init__(self):
        ############ Land size

        width = 50 # map width
        length = 40 # map length

        ############ Noise variables

        n1div = 20 # landmass distribution
        n2div = 2 # boulder distribution
        n3div = 10 # rock distribution

        n1scale = 20 # landmass height
        n2scale = 2 # boulder scale
        n3scale = 5 # rock scale

        noise1 = noise(width / n1div, length / n1div) # landmass / mountains
        noise2 = noise(width / n2div, length / n2div) # boulders
        noise3 = noise(width / n3div, length / n3div) # rocks


        zroot = 2
        zpower = 2.5

        ############ 3D shapes

        points = []

        for x in range(-int(width/2), int(width/2)):
            for y in range(-int(length/2), int(length/2)):
                x1 = x + width/2
                y1 = y + length/2
                z = noise1.perlin(x1 / n1div, y1 / n1div) * n1scale # add landmass
                z += noise2.perlin(x1 / n2div, y1 / n2div) * n2scale # add boulders
                z += noise3.perlin(x1 / n3div, y1 / n3div) * n3scale # add rocks
                if z >= 0:
                    z = -math.sqrt(z)
                else:
                    z = ((-z) ** (1 / zroot)) ** zpower
                points.append([x, y, z])

        self.points_bis = np.array(points)


    def array_points(self):
        return self.points_bis

        #print(points_bis.shape)
