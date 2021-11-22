import struct
import math

# clase vertice que se pueda sumar con el operador + 
class V3(object):   # hay que hacer overwrites
    def __init__(self, x, y, z = None):
        self.x = x
        self.y = y
        self.z = z
    
    def __getitem__(self, i):
        if i == 0:
            return self.x
        elif i == 1:
            return self.y
        elif i == 2:
            return self.z
    # metodo para imprimir algo 
    def __repr__(self):
        return "V3(%s, %s, %s)" %(self.x, self.y, self.z)

    
def clamp_color(v):
    return max(0, min(255, int(v)))

class color(object):
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
    # metodo para imprimir algo 
    def __repr__(self):
        b = clamp_color(self.b) # cual es el valor minimo entre 255 y self.b
        g = clamp_color(self.g)
        r = clamp_color(self.r)
        return "color(%s, %s, %s)" % (r, g, b)

    def toBytes(self):
        b = clamp_color(self.b) # cual es el valor minimo entre 255 y self.b
        g = clamp_color(self.g)
        r = clamp_color(self.r)

        return bytes([b, g, r])

    # suma de colores
    def __add__(self, other):
        r = clamp_color(self.r + other.r)
        g = clamp_color(self.g + other.g)
        b = clamp_color(self.b + other.b)
        return color(r, g, b)

    # multiplica de colores
    def __mul__(self, k):
        r = clamp_color(self.r * k)
        g = clamp_color(self.g * k)
        b = clamp_color(self.b * k)
        return color(r, g, b)


def char(c):
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    # short
    return struct.pack('=h', w)

def dword(w):
    # long
    return struct.pack('=l', w)


BLACK =  color(0, 0, 0)
WHITE =  color(255, 255, 255)



def writeBMP(filename, width, height, framebuffer):
        f = open(filename, 'bw')

        # File header (14)
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + 3*(width * height)))
        f.write(dword(0))
        f.write(dword(14 + 40))

        # Info header (40)
        f.write(dword(40))
        f.write(dword(width))
        f.write(dword(height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(3*(width*height)))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        # Bitmap (se recorre el framebuffer completo, para meter los bytes en un array de 4)
        for y in range(height):
            for x in range(width):
                try:
                    f.write(framebuffer[y][x].toBytes())
                except:
                    pass
        f.close()

def reflect(I, N):
    return norm(sub(I, mul(N, 2 * (dot(I, N)))))  # R = I - 2(N . I) N
# se puede calcula la intensidad de la luz, utilizando el producto punto entre la reflexion y la luz

def refract(I, N, refractive_index):
    cosi = -max(-1, min(1, dot(I, N))) # angulo en que entro la luz
    
    etai = 1  # indice de refraccion que trae el rayo
    etat = refractive_index # indice de refraccion de la transmision dentro del material
    # se vuelven a calcular los valores en caso de que sean negativos  
    if cosi < 0:
        cosi = -cosi
        etai, etat = etat, etai # switcharu
        N = mul(N, -1)

    eta = etai/etat
    # se calcula el angulo theta
    k = 1 - eta**2 *(1 - cosi**2)
    if k < 0:
        return None

    return norm(sum(mul(I, eta), mul(N, eta * cosi + k**0.5)))


class Material(object):
    def __init__(self, diffuse, albedo, spec, refractive_index = 0):
        self.diffuse = diffuse
        self.albedo = albedo
        self.spec = spec
        self.refractive_index = refractive_index

    def __repr__(self):
        return 'difu'

class Intersect(object):
    def __init__(self, distance, point, normal):
        self.distance = distance
        self.point = point
        self.normal = normal


# esta es como la luz del sol
class Light(object):
    def __init__(self, position, intensity, color):
        self.position = position # ubicacion de luz
        self.intensity = intensity  
        self.color = color

# este bounding box va a recibir los 3 parametros A,B,C
def bbox(A, B, C):
    xs = [A.x, B.x, C.x]
    xs.sort()
    ys = [A.y, B.y, C.y]
    ys.sort()
    # zs = [A.z, B.z, C.z]
    # zs.sort()
    # se utiliza -1 para regresar al ulitmo valor del array
    return V3(xs[0], ys[0]), V3(xs[-1], ys[-1])


def cross(v0, v1):
    # el producto cruz entre 3 vectores se calcula
    cx = v0.y * v1.z - v0.z * v1.y
    cy = v0.z * v1.x - v0.x * v1.z
    cz = v0.x * v1.y - v0.y * v1.x
    return V3(cx, cy, cz)

def barycentric(A, B, C, P):
    # calcular producto cruz entre dos vectores para calcular las 3 variables.
    bary = cross(
    V3(C.x - A.x, B.x - A.x, A.x - P.x), 
    V3(C.y - A.y, B.y - A.y, A.y - P.y)
  )

    if abs(bary[2]) < 1:
        return -1, -1, -1    # con esto se evita la division entre 0

    # para forzar a que uno sea 1 hay que dividirlos a todos entre cz
    w = 1 - (bary[0] + bary[1]) / bary[2]
    v = bary[1] / bary[2]
    u = bary[0] / bary[2]  # siempre que aparezca una división, hay una posibilidad que cz de 0. Esto significa que el triangulo es solo una linea

    # si ya tenemos herramienta, modulo que se va a priorizar sobretoido el valor de cleinte ubicar que clase o metodos hay que trabajar primero. se tiene que considerar refactorizarlo 
    # que framework de pruebas se van a utilizar.

    return w, v, u


def sub(v0, v1):
    return V3(
        v0.x - v1.x,
        v0.y - v1.y,
      
        v0.z - v1.z,
    )

def sum(v0, v1):
  """
    Input: 2 size 3 vectors
    Output: Size 3 vector with the per element sum
  """
  return V3(v0.x + v1.x, v0.y + v1.y, v0.z + v1.z)

def mul(v0, k):
  """
    Input: 2 size 3 vectors
    Output: Size 3 vector with the per element multiplication
  """
  return V3(v0.x * k, v0.y * k, v0.z *k)

def length(v0):
    return(v0.x**2 + v0.y**2 +v0.z**2) ** 0.5

def norm(v0):
    l = length(v0)
    if l ==0:
        return V3(0,0,0)

    return V3(
        v0.x / l,
        v0.y / l,
        v0.z / l
    )

def dot(v0, v1):
    return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z
