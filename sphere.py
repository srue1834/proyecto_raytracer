
from lib import *


class Sphere(object):  # una esfera se puede carcaterizar como radio y su centoir en el universo
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material
        

    # se quiere saber si el rayo intersecta la esfera
    def ray_intersect(self, origin, direction):
        
        L = sub(self.center, origin)  # vector que va del origin de donde salio el rayo al centro de la esfera
        tca = dot(L, direction)  # tca es el otro vector que es el producto punto de L y la direccion. Se quiere la magnitud que multiplicada la doireccion de L
        l = length(L)
        d2 = l**2 - tca**2 # tca**2 + d**2 = l**2 
        # se ve si d2 es mayor al radio al cuadrado, eso quiere decir que el rayo paso afuera de la esfera
        if d2 > self.radius**2:
            return None

        # es la mitad de distancia que hay del radio a la esfera, thc se puede utilizar para ver si el rayo toca la esfera
        thc = (self.radius**2 - d2)**(1/2) # self.radius**2 = thc**2 + d2
        t0 = tca - thc
        t1 = tca + thc
        # cast ray puede revisar con todas las esferas de la escena

        if t0 < 0:
            t0 = t1  # se quiere que en t0 se quede el intercepto menor 
        if t0 < 0:
            return None # no pego
    
        hit = sum(origin, mul(direction, t0)) # magnitud en la direccion de la luz
        normal = norm(sub(hit, self.center))
        return Intersect(
            distance=t0,
            # normal
            normal =normal,
            # posicion del punto 
            point =hit
        ) # si pego


        # como se hace para saber si hay algo detras del objeto?
        # se tienen que saber si el mismo radio ya le pego a algo
        # si se sabe que tan lejos impacto el rayo, se podria usar la tecnica de zbuffer

            

