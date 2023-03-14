from math import sin, cos, radians


def rotateX(vertex_list, degree, center=None):
    y_shift = 0
    z_shift = 0
    if center:
        _, y_shift, z_shift = center

    sinTheta = sin(radians(degree))
    cosTheta = cos(radians(degree))
    for i, point in enumerate(vertex_list):
        x, y, z = point
        y -= y_shift
        z -= z_shift
        vertex_list[i] = (x, y * cosTheta - z * sinTheta + y_shift, z * cosTheta + y * sinTheta + z_shift)

    return vertex_list


def rotateY(vertex_list, degree, center):
    x_shift = 0
    z_shift = 0
    if center:
        x_shift, _, z_shift = center
    sinTheta = sin(radians(degree))
    cosTheta = cos(radians(degree))
    for i, point in enumerate(vertex_list):
        x, y, z = point
        x -= x_shift
        z -= z_shift
        vertex_list[i] = (x * cosTheta + z * sinTheta + x_shift, y, z * cosTheta - x * sinTheta + z_shift)
    return vertex_list


def rotateZ(vertex_list, degree, center):
    x_shift = 0
    y_shift = 0
    z_shift = 0
    if center:
        x_shift, y_shift, _ = center
    sinTheta = sin(radians(degree))
    cosTheta = cos(radians(degree))
    for point in vertex_list:
        x, y, z = point
        x -= x_shift
        y -= y_shift
        point = (x * cosTheta - y * sinTheta + x_shift, y * cosTheta + x * sinTheta + y_shift, z)
    return vertex_list


def scale(vertex_list, factor: tuple):
    xf, yf, zf = factor
    for point in vertex_list:
        x, y, z = point
        point = x * xf, y * yf, z * zf
    return vertex_list
