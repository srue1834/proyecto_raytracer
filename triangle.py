from lib import * 

class Triangle(object):

    def __init__(self, v0, v1, v2, material):
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2
        self.material = material

    def ray_intersect(self, origin, direction):
        v0v1  = sub(self.v1, self.v0)
        v0v2 = sub(self.v2, self.v0)

        pvec = cross(direction, v0v2) 

        det = dot(v0v1, pvec) 

        if det < 0.000001:
            return None

        invDet = 1.0 / det
        tvec = sub(origin, self.v0)

        u = dot(tvec, pvec) * invDet

        if u < 0 or u > 1:
            return None

        qvec = cross(tvec, v0v1)

        v = norm(dot(direction, qvec) * invDet)

        if v < 0 or u + v > 1:
            return None

        t = dot(v0v2, qvec) * invDet

        return Intersect(
                    distance=t,
                    # normal
                    normal = u,
                    # posicion del punto 
                    point = v
                    ) # si pego

