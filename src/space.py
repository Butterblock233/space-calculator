from math import acos, pi, fabs


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

class PlaneOperation:
    '''The operation interface for plane which represent with geometrical represent or algebraic represent in space.'''
    type_tag = 'plane'

    
    def normal_vec_repr(self):
        assert isinstance(self, PlaneWithGeo), '''A point argument is required, while the object dosen't have.'''
        return f'{self.normal_vector.x}(x-{self.point_1.x}) + {self.normal_vector.y}(y-{self.point_1.y}) + {self.normal_vector.z}(z-{self.point_1.z}) = 0'

    def general_repr(self):
        if self.branch == 'geometry':
            self.constant = self.point_1.x*self.normal_vector.x + self.point_1.y*self.normal_vector.y + self.point_1.z*self.normal_vector.z
        return f'{self.normal_vector.x}x + {self.normal_vector.y}y + {self.normal_vector.z}z + {self.constant} = 0'

    def intercept_repr(self):
        if self.normal_vector.x == 0:
            self.a = 0
        else:
            self.a = -(self.constant/self.normal_vector.x)
        if self.normal_vector.y == 0:
            self.b = 0
        else:
            self.b = -(self.constant/self.normal_vector.y)
        if self.normal_vector.z == 0:
            self.c = 0
        else:
            self.c = -(self.constant/self.normal_vector.z)
        
        if self.branch == 'geometry':
            self.constant = self.point_1.x*self.normal_vector.x + self.point_1.y*self.normal_vector.y + self.point_1.z*self.normal_vector.z
        return f'x/{self.a} + y/{self.b} + z/{self.c} = 1'

    def angle(self, other):
        cos_a = (self.normal_vector.quantity_product(other.normal_vector)) / self.normal_vector.magnitude * other.normal_vector.magnitude
        angle = acos(cos_a)
        return [cos_a, f'{angle/pi}pi']

    def is_vertical(self, other):
        return self.angle(other)[0] == 0

    def is_parallel(self, other):
        return self.normal_vector.cross_product(other.normal_vector).magnitude == 0

    def distance_to_plane(self, point):
        assert isinstance(point, Point), ''
        A = self.normal_vector.x
        B = self.normal_vector.y
        C = self.normal_vector.z
        x0 = point.x; y0 = point.y; z0 = point.z
        return fabs(A*x0 + B*y0 + C*z0 + self.constant) / self.normal_vector.magnitude

class PlaneWithGeo(PlaneOperation):
    '''Plane construct by geometrical elements.'''
    branch = 'geometry'

    def __init__(self, point_1, point_2, point_3):
        super().__init__()
        self.point_1 = point_1
        self.point_2 = point_2
        self.point_3 = point_3

    @property
    def normal_vector(self):
        vector_a = VectorWithPoint(self.point_1, self.point_2)
        vector_b = VectorWithPoint(self.point_1, self.point_3)
        return vector_a.cross_product(vector_b)

    @property
    def constant(self):
        return -(self.normal_vector.x*self.point_1.x + 
                 self.normal_vector.y*self.point_1.y +
                 self.normal_vector.z*self.point_1.z)

    def __repr__(self):
        return f'Plane({super().normal_vec_repr()})'
    
    def __str__(self):
        return f'{PlaneOperation.type_tag}-{self.point_1.name}{self.point_2.name}{self.point_3.name}'


class PlaneWithAlg(PlaneOperation):
    '''Plane construct by algebraic elements.'''
    branch = 'algebra'

    def __init__(self, normal_vec, constant):
        super().__init__()
        self.constant = constant
        self.normal_vector = normal_vec
    
    def __repr__(self):
        return f'Plane({super().general_repr()})'

    def __str__(self):
        return f'{PlaneOperation.type_tag}: {super().general_repr()}'
        



if __name__ == "__main__":
    A = Point('A', 1, 1, 1)
    B = Point('B', 1, 5, 4)
    C = Point('C', 1, 0, 0)


    ABC = PlaneWithGeo(A, B, C)
    print(repr(ABC))
    print('plane ABC:', ABC)
    print('normal vector of ABC:', ABC.normal_vector)

    PI_1 = PlaneWithAlg(ABC.normal_vector, 5)
    print(repr(PI_1))
    print(PI_1)
    print(PI_1.intercept_repr())

    n = VectorWithCoordinate(0, 1, 0)
    PI_2 = PlaneWithAlg(n, 5)
    print('cos_a =', PI_2.angle(PI_1)[0], 'a =', PI_2.angle(PI_1)[1])
    m = VectorWithCoordinate(0, 3, 0)
    PI_3 = PlaneWithAlg(m, 5)
    print('PI_1 perpendicular to PI_2?', PI_1.is_vertical(PI_2))
    print('PI_2 parallel to PI_3?', PI_2.is_parallel(PI_3))
    D = Point('D', 0, 0, 0)
    print('Distance from D to PI_1:', PI_1.distance_to_plane(D))
    