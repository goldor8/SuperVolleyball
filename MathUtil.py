import math


def magnitude(vector):
    return math.sqrt(vector[0] ** 2 + vector[1] ** 2)


def dot(vector, axis):
    return vector[0] * axis[0] + vector[1] * axis[1]


def project(vector, axis):
    axis_magnitude = magnitude(axis)
    if axis_magnitude == 0:
        return 0
    return dot(vector, axis) / axis_magnitude


def normalize(vector):
    vector_magnitude = magnitude(vector)
    if vector_magnitude == 0:
        return 0, 0
    return vector[0] / vector_magnitude, vector[1] / vector_magnitude


def project_vector(vector, axis):
    normalized_axis = normalize(axis)
    return project(vector, axis) * normalized_axis[0], project(vector, axis) * normalized_axis[1]