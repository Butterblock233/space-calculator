from space import *


def menu():
    print('=======================================================')
    print('====================SPACE CALCULATOR===================')
    print('=======================================================')
    print('This a calculator for simply compute in solid geometry.')
    print("---------------Type 'help()' to see usage--------------")

def constructor():
    pass

def calculator():
    pass

def help():
    print('Constructor')
    print('\t[object] = ([object_name], x, y, z)               \tTo construct a point in space')
    print('\t[object] = VectorWithPoint(start_point, end_point)\tTo construct a vector with points')
    print('\t[object] = VectorWithCoordinate(x ,y, z)          \tTo construct a vector with coordinate')
    print('Operator')
    print('\t[vector1] + [vector2]                             \tAdd vector1 to vector2')
    print('\t[vector].magnitude                                \tGet the magnitude of vector')
    print('\tVectorOperation.direction_cos([vector])           \tEvaluate the direction cosine of the vector in python interpreter')
    print('\t[vector].cos_[x, y, z]                            \tOutput the direction cosine of vector (Using it after evalution)')
    print('\t[scalar]*[vector] or [vector]*[scalar]            \tMultiply a number(scalar) by a vector or reverse')
    print('\t[vector1].quantity_product([vector1])             \tGet [vector1]·[vector2]')
    print('\t[vector1].cross_product([vector2])                \tGet [vector1]x[vector2]')
    print('\t[vector1].projection([vector2])                   \tGet the projection of [vector1] a onto [vector2]')


if __name__ == "__main__":
    menu()
