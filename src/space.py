from math import acos, pi, fabs
import random


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

    def random_point(num):
        '''Return 'num' points in space.'''
        for _ in range(num):
            x = random.randint(-50, 50)
            y = random.randint(-50, 50)
            z = random.randint(-50, 50)

            return Point('_', x, y, z)

        
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
    def magnitude(self) -> float:
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
 
    def quantity_product(self, other) -> float:
        return self.x*other.x + self.y*other.y + self.z*other.z

    def cross_product(self, other):
        return VectorWithCoordinate( (self.y*other.z - self.z*other.y), 
                                    -(self.x*other.z - self.z*other.x),
                                     (self.x*other.y - self.y*other.x) )
                                    
    def direction_cos(self) -> dict:
        self.cos_x = self.x / self.magnitude
        self.cos_y = self.y / self.magnitude
        self.cos_z = self.z / self.magnitude
        return {'cos_x': self.cos_x, 'cos_y': self.cos_y, 'cos_z': self.cos_z}
    
    def cos_angle(self, other) -> float:
        assert isinstance(other, VectorOperation) and self.magnitude != 0, ''
        return fabs(self.quantity_product(other)) / (self.magnitude*other.magnitude)

    def projection(self, other) -> float:
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
        super().__init__()
        return f'Vector({self.point_s.name}{self.point_e.name}) == {VectorWithCoordinate((self.point_e.x - self.point_s.x), (self.point_e.y - self.point_s.y), (self.point_e.z - self.point_s.z))}'

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

    @property
    def normal_vector(self) -> VectorWithCoordinate:
        if self.branch == 'geometry':
            vector_a = VectorWithPoint(self.point_1, self.point_2)
            vector_b = VectorWithPoint(self.point_1, self.point_3)
            return vector_a.cross_product(vector_b)
        elif self.branch == 'algebra':
            return VectorWithCoordinate(self.A, self.B, self.C)

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

    def angle(self, other: VectorOperation) -> list:
        cos_a = (self.normal_vector.quantity_product(other.normal_vector)) / self.normal_vector.magnitude * other.normal_vector.magnitude
        angle = acos(cos_a)
        return [cos_a, f'{angle/pi}pi']

    def is_vertical(self, other: VectorOperation) -> bool:
        return self.angle(other)[0] == 0

    def is_parallel(self, other: VectorOperation) -> bool:
        return self.normal_vector.cross_product(other.normal_vector).magnitude == 0

    def distance_to_plane(self, point: Point) -> float:
        assert isinstance(point, Point), ''
        A = self.normal_vector.x
        B = self.normal_vector.y
        C = self.normal_vector.z
        x0 = point.x; y0 = point.y; z0 = point.z
        return fabs(A*x0 + B*y0 + C*z0 + self.constant) / self.normal_vector.magnitude

    def point_at_plane(self, point: Point) -> bool:
        return self.normal_vector.x * point.x + self.normal_vector.y * point.y + self.normal_vector.z * point.z + self.constant == 0


class PlaneWithGeo(PlaneOperation):
    '''Plane construct by geometrical elements.'''
    branch = 'geometry'

    def __init__(self, point_1: Point, point_2: Point, point_3: Point):
        super().__init__()
        self.point_1 = point_1
        self.point_2 = point_2
        self.point_3 = point_3

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

    def __init__(self, A, B, C, constant):
        super().__init__()
        self.A = A
        self.B = B
        self.C = C
        self.constant = constant
    
    def __repr__(self):
        return f'Plane({super().general_repr()})'

    def __str__(self):
        return f'{PlaneOperation.type_tag}: {super().general_repr()}'
        

class StraightLineOperation:
    '''The operation interface for straight line which represent with geometrical represent or algebraic represent in space.'''
    type_tag = 'straight'

    @property
    def direction_vector(self) -> VectorWithCoordinate:
        if self.branch == 'geometry':
            return self.plane_1.normal_vector.cross_product(self.plane_2.normal_vector)
        elif self.branch == 'algebra':
            return VectorWithCoordinate(self.m, self.n, self.p)

    def distance_point_line(self, point: Point) -> float:
        # if self.branch == 'geometry':
            # M0 = Point.random_point(1) 
            # while self.point_at_line(M0) == False:
                # M0 = Point.random_point(1)
        return (1/self.direction_vector.magnitude) * VectorWithPoint(point, self.M0).cross_product(self.direction_vector).magnitude
        # elif self.branch == 'algebra':
            # return (1/self.direction_vector.magnitude) * VectorWithPoint(point, self.M0).cross_product(self.direction_vector).magnitude

    def point_at_line(self, point: Point) -> bool:
        if self.branch == 'geometry':
            p1 = self.plane_1.normal_vector.x*point.x + self.plane_1.normal_vector.y*point.y + self.plane_1.normal_vector.z*point.z + self.plane_1.constant == 0
            p2 = self.plane_2.normal_vector.x*point.x + self.plane_2.normal_vector.y*point.y + self.plane_2.normal_vector.z*point.z + self.plane_2.constant == 0
            return p1 and p2
        elif self.branch == 'algebra':
            e1 = (point.x-self.M0.x) / self.m
            e2 = (point.y-self.M0.y) / self.n
            e3 = (point.z-self.M0.z) / self.n
            return e1 == e2 and e1 == e3 and e2 == e3

    @property
    def direction_cos(self) -> dict:
        return self.direction_vector.direction_cos()

    def cos_angle(self, other) -> float:
        assert other.type_tag == 'straight', ''
        return self.direction_vector.cos_angle(other.direction_vector)
    
    def sin_angle(self, other: PlaneOperation) -> float:
        return fabs(self.direction_vector.cos_angle(other.normal_vector))

    def is_at_plane(self, plane: PlaneOperation) -> bool:
        return self.sin_angle(plane) == 0

    def perp_to_straight(self, straight) -> bool:
        assert straight.type_tag == 'straight', ''
        return self.direction_vector.quantity_product(straight.direction_vector) == 0

    def para_to_straight(self, straight) -> bool:
        assert straight.type_tag == 'straight', ''
        return self.direction_vector.cross_product(straight.direction_vector) == 0

    def perp_to_plane(self, plane: PlaneOperation) -> bool:
        return self.direction_vector.cross_product(plane.normal_vector) == 0

    def para_to_plane(self, plane: PlaneOperation) -> bool:
        assert self.is_at_plane(plane) == False, ''
        return self.direction_vector.quantity_product(plane.normal_vector) == 0


class StraightLineWithGeo(StraightLineOperation):
    '''Straight line construct by geometrical elements.'''
    branch = 'geometry'

    def __init__(self, plane_1: PlaneOperation, plane_2: PlaneOperation):
        super().__init__()
        assert plane_1.is_parallel(plane_2) == False, '''planes parallel to each other haven't intersection.'''
        self.plane_1 = plane_1
        self.plane_2 = plane_2

    def __repr__(self):
        super().__repr__()
        return f'|{self.plane_1.normal_vector.x}x + {self.plane_1.normal_vector.y}y + {self.plane_1.normal_vector.z}z + {self.plane_1.constant} == 0 \n|{self.plane_2.normal_vector.x}x + {self.plane_2.normal_vector.y}y + {self.plane_2.normal_vector.z}z + {self.plane_2.constant} == 0'

    def __str__(self):
        super().__str__()
        return f'{self.type_tag}: ({self.direction_vector.x}, {self.direction_vector.y}, {self.direction_vector.z})'

    @property
    def M0(self) -> Point:
        point = Point.random_point(1)
        while self.point_at_line(point) == False:
            point = Point.random_point(1)
        return point


class StraightLineWithAlg(StraightLineOperation):
    '''Straight line construct by algebraic elements.'''
    branch = 'algebra'

    def __init__(self, m, n, p, M0: Point):
        super().__init__()
        self.m = m
        self.n = n
        self.p = p
        self.M0 = M0

    def __repr__(self):
        super().__repr__()
        return f'l: (x-{self.M0.x}) / {self.direction_vector.x} == (y-{self.M0.y}) / {self.direction_vector.y} == (z-{self.M0.z}) / {self.direction_vector.z}'

    def __str__(self):
        super().__str__()
        return f'|x == {self.M0.x} + {self.direction_vector.x}t \n|y == {self.M0.y} + {self.direction_vector.y}t \n|z == {self.M0.z} + {self.direction_vector.z}t'


if __name__ == "__main__":
    A = Point('A', 1, 1, 1)
    B = Point('B', 1, 0, 1)
    C = Point('C', 0, 1, 1)
    O = Point('D', 0, 0, 0)
    
    PI_1 = PlaneWithGeo(A, B, C)
    PI_2 = PlaneWithAlg(5, 0, 0, 5)
    print('is PI_1 // PI_2?', PI_1.is_parallel(PI_2))

    n = StraightLineWithGeo(PI_1, PI_2)
    print(repr(n))
    print(n)

    l = StraightLineWithAlg(1, 3, 5, O)
    print(repr(l))
    print(l)

    R = Point.random_point(1)
    print(R)

    print('distance from O to l:', l.distance_point_line(O))
    print('is O at n:', l.point_at_line(O))
    print('distance from O to l:', n.distance_point_line(O))
    print('is O at n:', n.point_at_line(O))

    print('cos_x of l:', l.direction_cos['cos_x']) 
    print('cos_y of l:', l.direction_cos['cos_y']) 
    print('cos_z of l:', l.direction_cos['cos_z']) 

    print(l.direction_vector, n.direction_vector)
    print('cos<l, n> =', l.cos_angle(n))

    print('cos<PI_1, n> =', n.sin_angle(PI_1))
    print('is n at PI_1?', n.is_at_plane(PI_1))
    print('cos<PI_1, l> =', l.sin_angle(PI_1))
    print('is l at PI_1?', l.is_at_plane(PI_1))

    # print(n.para_to_plane(PI_1))
