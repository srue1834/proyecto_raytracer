
from lib import *

class Plane(object):
  def __init__(self, position, normal, material):
    self.position = position
    self.material = material
    self.normal = norm(normal)

  def ray_intersect(self, origin, direction):
    epsilon = 1e-6
    denom = dot(direction, self.normal)
    if abs(denom) > epsilon:
      t = dot(self.normal, sub(self.position, origin)) / denom
      
    # dx = -(orig.x + self.x) / direction.x
      if t > 0:
        hit = sum(origin, mul(direction, t))

        return Intersect(
          distance=t,
          point=hit,
          normal=self.normal
        )
      else:
                  return None
