
from lib import *
from plane import *
import sys
from triangle import *

class Cube(object):
    def __init__(self, position, size, material):
        self.position = position
        self.size = size
        self.material = material

        self.planes = []
        self.b_min = [0, 0, 0]
        self.b_max = [0, 0, 0]
        
        halfSizeX = size[0] / 2
        halfSizeY = size[1] / 2
        halfSizeZ = size[2] / 2

        self.planes.append(Plane(sum(position, V3(halfSizeX, 0, 0)), V3(1, 0, 0), material))
        self.planes.append(Plane(sum(position, V3(-halfSizeX, 0, 0)), V3(-1, 0, 0), material))

        self.planes.append(Plane(sum(position, V3(0, halfSizeY, 0)), V3(0, 1, 0), material))
        self.planes.append(Plane(sum(position, V3(0, -halfSizeY, 0)), V3(0, -1, 0), material))
        
        self.planes.append(Plane(sum(position, V3(0, 0, halfSizeZ)), V3(0, 0, 1), material))
        self.planes.append(Plane(sum(position, V3(0, 0, -halfSizeZ)), V3(0, 0, -1), material))
        
        epsilon = 0.001

        
        for i in range(3):
            self.b_min[i] = self.position[i] - (epsilon + self.size[i] / 2)
            self.b_max[i] = self.position[i] + (epsilon + self.size[i] / 2)
        
    def ray_intersect(self, origin, direction):
        intersect = None
        t = sys.maxsize

        for plane in self.planes:
            plane_i = plane.ray_intersect(origin, direction)

            if plane_i is not None:
                if plane_i.point[0] >= self.b_min[0] and plane_i.point[0] <= self.b_max[0]:
                    if plane_i.point[1] >= self.b_min[1] and plane_i.point[1] <= self.b_max[1]:
                        if plane_i.point[2] >= self.b_min[2] and plane_i.point[2] <= self.b_max[2]:
                            if plane_i.distance < t:
                                t = plane_i.distance
                                intersect = plane_i

        if intersect is None: 
            return None
        return Intersect(
            distance = intersect.distance, 
            point = intersect.point, 
            normal = intersect.normal)

