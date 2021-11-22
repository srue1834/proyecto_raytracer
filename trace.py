
from lib import * 
from math import pi, tan
from random import random
from sphere import *
from cube import *
from plane import *
from triangle import *
from envmap import *

BLACK = color(0, 0, 0)
MAX_RECURSION_DEPTH = 3 # se rebota 3 veces

class Raytracer(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.envmap = None
        self.background_color =  BLACK
        self.color2 = color(26,158,207)
        self.light  = None
        self.clear()
        
        
    def clear(self):
        self.framebuffer = [
            [BLACK for _ in range(self.width)]
            for _ in range(self.height)
        ]
        # array v2
    def write(self, filename):
        writeBMP(filename, self.width, self.height, self.framebuffer)

    def point(self, x, y, col):
        self.framebuffer[y][x] = col

    def cast_ray(self, origin, direction, recursion = 0):
        # if sphere.ray_intersect(origin, direction):
        #     return color(255, 0, 0)
        # else:
        #     return color(0, 0, 255)
        material, intersect = self.scene_intersect(origin, direction)

        if material is None or recursion >= MAX_RECURSION_DEPTH:
            if self.envmap:
                return self.envmap.get_color(direction)

            return self.color2

        light_dir = norm(sub(self.light.position, intersect.point))
        light_distance = length(sub(self.light.position, intersect.point))
        # shadow bias
        offset_normal = mul(intersect.normal, 0.1) # se agarra la normal y se multiplica por un valor pequeño
        shadow_orig = sum(intersect.point, offset_normal) if dot(light_dir, intersect.normal) > 0 else sub(intersect.point, offset_normal) # se mueve el punto de inicio en direccion del rayo normal
        shadow_material, shadow_intersect = self.scene_intersect(shadow_orig, light_dir)
        
        if shadow_material is None or length(sub(shadow_intersect.point, shadow_orig)) > light_distance:
            shadow_intensity = 0 # cuando se llame al scene intersect va a chocar contra si mismo
        else:
            shadow_intensity = 0.9 # se puede calcular el numero de varias maneras

        if material.albedo[2] > 0 :  # si es una superficie reflectiva
            revert_dir = mul(direction, -1)# revertir la direccion
            reflect_dir = reflect(revert_dir, intersect.normal) # direccion reflejada
            reflect_origin = sum(intersect.point, offset_normal) if dot(reflect_dir, intersect.normal) > 0 else sub(intersect.point, offset_normal)# se hace un offset moviendo el punto de origen de la refleccion
            reflect_color = self.cast_ray(reflect_origin, reflect_dir, recursion  +1)
            
        else:
            reflect_color = color(0, 0, 0)

        # luz que atraviesa 
        if material.albedo[3] > 0 : 
            refract_dir =  refract(direction, intersect.normal, material.refractive_index)
            
            if refract_dir is None:
                refract_color = color(255, 0, 0)
            else:
                refract_origin = sum(intersect.point, offset_normal) if dot(refract_dir, intersect.normal) > 0 else sub(intersect.point, offset_normal)
            
                refract_color = self.cast_ray(refract_origin, refract_dir, recursion  +1)
            
        else:
            refract_color = color(0, 0, 0)


        diffuse_intensity = self.light.intensity * max(0, dot(light_dir, intersect.normal)) * (1 - shadow_intensity) # intesidad de luz difusa


        if shadow_intensity > 0:
            specular_intensity = 0
        else:

            s_reflection = reflect(light_dir, intersect.normal) # para calcular reflexion
            specular_intensity = self.light.intensity * (
            max(0, dot(s_reflection, direction)) ** material.spec)  # intesidad de reflexion, producto punto entre la reflexion y la direccion del rayo

        diffuse = material.diffuse * diffuse_intensity * material.albedo[0] # dependende del marterial pp intensidad

        specular = self.light.color * specular_intensity * material.albedo[1] # albedo para el color especular

        reflection = reflect_color * material.albedo[2] 
        refraction = refract_color * material.albedo[3]


        c =  diffuse + specular + reflection + refraction # color que viene por la refleccion
        return c
            

    def scene_intersect(self, origin, direction):
        zbuffer = float('inf') # valor negativo mas grande
        material = None
        intersect = None
        
        # se componen de varios objetos
        for obj in self.scene:
            r_intersect = obj.ray_intersect(origin, direction)

            if r_intersect and r_intersect.distance < zbuffer: # distancia es magnitud del vector que siempre es positiva
                zbuffer = r_intersect.distance  # donde golpeo rayo
                material = obj.material
                intersect = r_intersect
        return material, intersect

    def render(self):
        fov = pi/2
        aspect_ratio = self.width/self.height # aspect ratio
        for y in range(self.height):
            for x in range(self.width):
                # para saber si el rayo toca algo, se trabaja con intersectar
                if random() > 0: # asi es mas rapido, se deberia renderizar 10% de los rayos
                    
                    """X y Y son las coordenadas en el espacio del raster
                    se encuentra el I y J son coordenadas del rayo que se esta lanzando en el espacio del mundo"""
                    i = (2 *((x + 0.5)/ self.width) - 1) * aspect_ratio * tan(fov/2) # si la apertura es de 45 grados, eso es constante
                    j = 1 - 2 * ((y + 0.5)/ self.height) * tan(fov/2) # se voltea
                    
                    """se tiene una camara con una apertura que pega a un plano
                    los rayos infinitos se normalizan """
                    direction = norm(V3(i, j, -1)) # la direcicon es una funcion con algun valor que corresponda a X y Y
                    # z es siempre -1 
                    col = self.cast_ray(V3(0, 0, 0), direction) # se tiene varios objetos volando y se quiere ver a cual objeto
                    self.point(x,y, col)

                
        

r = Raytracer(200, 100)
r.envmap = Envmap("./textures/background.bmp")
r.light = Light(
    position= V3(35, -70, 90),
    intensity=1.6,
    color = color(255,255,255)
)

dark_green =  Material(diffuse=color(30,77,24), albedo=[0.9, 0.1, 0.0, 0], spec=10)
green =  Material(diffuse=color(95,197,89), albedo=[0.9, 0.1, 0.0, 0], spec=10)
beige =  Material(diffuse=color(193,172,119), albedo=[0.6, 0.3, 0.1, 0], spec=50)
black = Material(diffuse=color(7,19,6), albedo=[0.9, 0.1, 0.0, 0], spec=10)

ivory = Material(diffuse=color(100, 100, 80), albedo=[0.6, 0.3, 0.1, 0], spec=50)
water = Material(diffuse=color(80, 80, 120), albedo=[0, 0.5, 0.1, 0.8], spec=125, refractive_index=1.5)


r.scene = [

    Cube(V3(0, 7, -20), V3(60, 15, 10), water),
    Cube(V3(6, 3.5, -15), V3(10, 15, 10), green),

    Cube(V3(3.5, 0, -9.8), V3(2.6, 2.6, 0), dark_green),
    Cube(V3(3.8, 0.5, -9.6), V3(1.5, 1.5, 0), black),

    Cube(V3(8, 0, -9.8), V3(2.6, 2.6, 0), dark_green),
    Cube(V3(7.5, 0.5, -9.6), V3(1.5, 1.5, 0), black),

    Cube(V3(5.7, 2, -9.8), V3(2.6, 1, 0), dark_green),
    Cube(V3(4, 3.5, -9.8), V3(1.2, 2.6, 0), dark_green),
    Cube(V3(7.5, 3.5, -9.8), V3(1.2, 2.6, 0), dark_green),

    Cube(V3(5.7, 3, -9.8), V3(2.6, 0.8, 0), black),
    Cube(V3(5.6, 3.7, -9.6), V3(4, 1.2, 0), black),



    Cube(V3(-7, 4.5, -10.3), V3(7, 5, 5), green),

    Cube(V3(0, 9, -8), V3(26, 10, 1), beige),
    Cube(V3(14.5, 0, -8), V3(3, 16, 1), beige),
    Cube(V3(-14.5, 0, -8), V3(3, 16, 1), beige),



    Triangle(V3(1, 0, 1), V3(1, 1, 1), V3(1, 0, 1), ivory),
    
]

r.render()
r.write('r.bmp')

# r = int((x / self.width) * 255)
# g = int((y / self.height) * 255)
# b = 0  






        











