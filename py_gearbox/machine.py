import math
import primitive as prim
import transform as xfm


def rack(length, pitch, depth):
    """
    A toothed linear component  
    Pitch determines compatibility with other gears
    """
    points = []
    indices = []
    num_teeth = int(length / pitch)

    if depth == 0:
        return num_teeth

    for tooth in range(num_teeth):
        new_points, new_indices = prim.gear_tooth(pitch, depth)
        points = xfm.translate(points, pitch, 0, 0)

        points, indices = xfm.merge(
            points, indices, new_points, new_indices)

    return points, indices


def pinion(radius, pitch, depth, arc_degrees):
    """
    A partial circumference spur gear 
    Pitch determines compatibility with other gears
    """
    points = []
    indices = []
    num_teeth = int(math.pi * 2 * radius / pitch)

    if depth == 0:
        return num_teeth

    arc_per_tooth = 360 / num_teeth

    for tooth in range(int(num_teeth * (arc_degrees/360))):
        new_points, new_indices = prim.gear_tooth(pitch, depth)
        new_points = xfm.translate(new_points, 0, radius, 0)
        new_points = xfm.rotate(new_points, arc_per_tooth * tooth, 2)

        points, indices = xfm.merge(
            points, indices, new_points, new_indices)

    return points, indices

def gear_wheel(radius, pitch, depth):
    """
    A "cog"
    Pitch determines compatibility with other gears
    """
    points = []
    indices = []
    num_teeth = int(math.pi * 2 * radius / pitch)

    if depth == 0:
        return num_teeth

    arc_per_tooth = 360 / num_teeth

    for tooth in range(num_teeth):
        new_points, new_indices = prim.gear_tooth(pitch, depth)
        new_points = xfm.translate(new_points, 0, radius, 0)
        new_points = xfm.rotate(new_points, arc_per_tooth * tooth, 2)

        points, indices = xfm.merge(
            points, indices, new_points, new_indices)

    return points, indices


def internal_gear(radius, pitch, depth):
    """
    Inward facing teeth
    """
    points = []
    indices = []
    num_teeth = int(math.pi * 2 * radius / pitch)

    if depth == 0:
        return num_teeth

    arc_per_tooth = 360 / num_teeth

    for tooth in range(num_teeth):
        new_points, new_indices = prim.gear_tooth(pitch, depth)
        new_points = xfm.translate(new_points, 0, -radius, 0)
        new_points = xfm.rotate(new_points, arc_per_tooth * tooth, 2)

        points, indices = xfm.merge(
            points, indices, new_points, new_indices)

    return points, indices


def twisted_spur(radius, pitch, depth, twist, scale):
    """
    piece-wise linear approximation of helical spur gear
    """
    points = []
    indices = []
    n_slabs = 16
    slab_size = depth/n_slabs

    for offset in range(n_slabs):
        points_temp, indices_temp = gear_wheel(radius, pitch, slab_size)
        points_temp = xfm.translate(points_temp, 0, 0, slab_size * offset)
        points, indices = xfm.merge(
            points, indices, points_temp, indices_temp)

    points = xfm.gradient_rotate(points, twist/radius, 2, depth)
    if scale:
        points = xfm.gradient_scale(points, scale, scale, 1, 2, depth)

    return points, indices


def twisted_internal(radius, pitch, depth, twist):
    """
    piecewise linear approximation of helical spur gear
    """
    points = []
    indices = []
    n_slabs = 16
    slab_size = depth/n_slabs

    for offset in range(n_slabs):
        points_temp, indices_temp = internal_gear(radius, pitch, slab_size)
        points_temp = xfm.translate(points_temp, 0, 0, slab_size * offset)
        points, indices = xfm.merge(
            points, indices, points_temp, indices_temp)

    points = xfm.gradient_rotate(points, -twist/radius, 2, depth)

    return points, indices


def face_gear(radius, pitch, depth):
    """
    Radial teeth on one face of disk
    """
    points = []
    indices = []
    num_teeth = int(math.pi * 2 * radius / pitch)

    if depth == 0:
        return num_teeth

    arc_per_tooth = 360 / num_teeth

    for tooth in range(num_teeth):
        new_points, new_indices = prim.gear_tooth(pitch, depth)
        new_points = xfm.rotate(new_points, 90, 0)
        new_points = xfm.translate(new_points, 0, -radius + depth, 0)
        new_points = xfm.rotate(new_points, arc_per_tooth * tooth, 2)

        points, indices = xfm.merge(
            points, indices, new_points, new_indices)

    return points, indices
