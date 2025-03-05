from space import *


def menu():
    print('=======================================================')
    print('====================SPACE CALCULATOR===================')
    print('=======================================================')
    print('This a calculator for simply compute in solid geometry.')
    print("---------Type 'help([command])' to see usage-----------")

def constructor():
    pass

def calculator():
    pass

def help(command=None):
    print('The [command] is that the mathematic element you want to use, and it is string-format.')

    if command == 'vector':
        print('Constructor')
        print('\t[object] = ([object_name], x, y, z)               \tConstruct a point in space')
        print('\t[object] = VectorWithPoint(start_point, end_point)\tConstruct a vector with points')
        print('\t[object] = VectorWithCoordinate(x ,y, z)          \tConstruct a vector with coordinate')
        print('Operator')
        print('\t[vector1] + [vector2]                             \tAdd vector1 to vector2')
        print('\t[vector].magnitude                                \tGet the magnitude of vector')
        print('\tVectorOperation.direction_cos([vector])           \tEvaluate the direction cosine of the vector in python interpreter')
        print('\t[vector].cos_[x, y, z]                            \tOutput the direction cosine of vector (Using it after evalution)')
        print('\t[scalar]*[vector] or [vector]*[scalar]            \tMultiply a number(scalar) by a vector or reverse')
        print('\t[vector1].quantity_product([vector1])             \tGet [vector1]·[vector2]')
        print('\t[vector1].cross_product([vector2])                \tGet [vector1]x[vector2]')
        print('\t[vector1].projection([vector2])                   \tGet the projection of [vector1] onto [vector2]')
    elif command == 'plane':
        print('Constructor')
        print('\t[object] = PlaneWithGeo([point1], [point2], [point3])       \tConstruct a plane with three point')
        print('Operator')
        print('\t[object].normal_vector                                      \tGet the normal vector of the plane')
        print('\t[object].intercept_repr()                                   \tGet the intercept form of the plane')
        print('\t[plane1].angle([plane2])[0]                                 \tGet the cosine of the angle between [plane1] and [plane2]')
        print('\t[plane1].angle([plane2])[1]                                 \tGet the angle between [plane1] and [plane2]')
        print('\t[plane1].is_vertical([plane2])                              \tJudge whether [plane1] is perpendicular to [plane2] or not, and return a bool value')
        print('\t[plane1].is_parallel([plane2])                              \tJudge whether [plane1] is parallel to [plane2] or not, and return a bool value')
        print('\t[plane].distance_to_point([point])                          \tGet the distance from [point] to [plane]')



if __name__ == "__main__":
    menu()
