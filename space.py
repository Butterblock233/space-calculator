from math import sin, cos


class Point:
    '''A point in space which is implemented by using its coordinate.'''
    type_tag = 'point'

    def __init__(self, name, x, y, z):
        self.name = name
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f'Point({self.x}, {self.y}, {self.z})'

    def __str__(self):
        return f'{self.name}({self.x}, {self.y}, {self.z})'

    def distance(self, other):
        return ((self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2) ** 0.5


class UnitVector:
    '''The definition of unit vector in space.'''
    def __init__(self):
        self.i = VectorWithCoordinate(1, 0, 0)
        self.j = VectorWithCoordinate(0, 1, 0)
        self.k = VectorWithCoordinate(0, 0, 1)


class VectorOperation:
    '''The operation interface for vector which represent with coordinate or point in space.'''
    type_tag = 'vector'

    def __add__(self, other):
        assert not (isinstance(other.type_tag, int) or isinstance(other.type_tag, float)), '''You can't add a scalar to a vector.'''
        return VectorWithCoordinate(self.x+other.x, self.y+other.y, self.z+other.z)
    
    def __sub__(self, other):
        assert not (isinstance(other.type_tag, int) or isinstance(other.type_tag, float)), '''You can't add a scalar to a vector.'''
        return VectorWithCoordinate(self.x-other.x, self.y-other.y, self.z-other.z)

    @property
    def magnitude(self):
        if self.branch == 'geometry':
            return self.point_s.distance(self.point_e)
        elif self.branch == 'algebra':
            return (self.x**2 + self.y**2 + self.z**2) ** 0.5

    def num_mul_vector(self, num):
        assert type(num) is int or type(num) is float
        return VectorWithCoordinate(num*self.x, num*self.y, num*self.z)
    def __mul__(self):
        pass
    def __rmul__(self, scalar):
        return self.__mul__(scalar)
    __mul__ = num_mul_vector
 
    def quantity_product(self, other):
        return self.x*other.x + self.y*other.y + self.z*other.z

    def cross_product(self, other):
        return VectorWithCoordinate( (self.y*other.z - self.z*other.y), 
                                    -(self.x*other.z - self.z*other.x),
                                     (self.x*other.y - self.y*other.x) )
                                    
    def direction_cos(self):
        self.cos_x = self.x / self.magnitude
        self.cos_y = self.y / self.magnitude
        self.cos_z = self.z / self.magnitude
    
    def cos_angle(self, other):
        assert isinstance(other, VectorOperation) and self.magnitude != 0, ''
        return self.quantity_product(other) / self.magnitude*other.magnitude

    def projection(self, other):
        assert isinstance(other, VectorOperation) and self.magnitude != 0, ''
        return self.magnitude * self.cos_angle(other)
         

class VectorWithPoint(VectorOperation):
    '''Vector represent with point.'''
    branch = 'geometry'

    def __init__(self, point_start, point_end):
        super().__init__()
        self.point_s = point_start
        self.point_e = point_end 

    def __repr__(self):
        return f'Verctor({self.point_s.name}{self.point_e.name}) = {VectorWithCoordinate(
                            (self.point_e.x - self.point_s.x),
                            (self.point_e.y - self.point_s.y), 
                            (self.point_e.z - self.point_s.z))}'

    def __str__(self):
        return f'{self.point_s.name.upper()}->{self.point_e.name.upper()}'

    @property
    def x(self):
        return self.point_e.x - self.point_s.x
    @property
    def y(self):
        return self.point_e.y - self.point_s.y
    @property
    def z(self):
        return self.point_e.z - self.point_s.z


class VectorWithCoordinate(VectorOperation):
    '''Vector represent with coordinate.'''
    branch = 'algebra'

    def __init__(self, x, y, z):
        super().__init__()
        self.x = x 
        self.y = y 
        self.z = z 

    def __repr__(self):
        return f'Vector({self.x}i + {self.y}j + {self.z}k)'

    def __str__(self):
        return f'({self.x}, {self.y}, {self.z})'


class StraightLine:
    type_tag = 'straight'

    def __init__(self):
        pass

class Plane:
    type_tag = 'plane'

    def __init__(self):
        pass
        

if __name__ == "__main__":
    A = Point('A', 1, 1, 1)
    B = Point('B', 1, 5, 4)
    C = Point('C', 1, 0, 0)

    AB = VectorWithPoint(A, B)
    AC = VectorWithPoint(A, C)
    a = AB + AC
    b = AB - AC

    print('a = AB + AC = ', a)
    print('a = AB + AC = ', b)
    print(repr(a)) 
    print(repr(b)) 

    print('|a| =', a.magnitude)

    VectorOperation.direction_cos(a)
    print('a.cos_x =', a.cos_x, 'a.cos_y =', a.cos_y, 'a.cos_z =', a.cos_z)

    print('3a =', a*3)
    print('3a =', 3*a)

    print('a·a =', a.quantity_product(a))
    print('a·b =', a.quantity_product(b))

    print('PrjbA =', a.projection(b))
    print('PrjbA =', a.projection(b))

    print('a x b =', a.cross_product(b))
