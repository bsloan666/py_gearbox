import machine as mach
import transform as xfm
import primitive as prim


def simple_spur(radius, axle_radius, depth, pitch):
    points1, indices1 = mach.gear_wheel(radius, pitch, depth)
    points2, indices2 = prim.tube(axle_radius, radius - 1, depth, 64)
    points1, indices1 = xfm.merge(points1, indices1, points2, indices2)

    return points1, indices1

def spur(radius, axle_radius, depth, pitch, twist):
    points1, indices1 = mach.twisted_spur(radius, pitch, depth, twist, 0)
    points2, indices2 = prim.tube(axle_radius, radius - pitch/3, depth, 64)
    points1, indices1 = xfm.merge(points1, indices1, points2, indices2)

    return points1, indices1

def bevel_spur(radius, axle_radius, depth, pitch, twist):
    points1, indices1 = mach.twisted_spur(radius, pitch, depth, twist, (radius - depth)/radius)
    points2, indices2 = prim.conical_bushing(radius - 2, radius - (depth + 1.5), axle_radius, depth, 64)
    points1, indices1 = xfm.merge(points1, indices1, points2, indices2)

    return points1, indices1


def ring(radius, depth, pitch, twist):
    points1, indices1 = mach.twisted_internal(radius, pitch, depth, twist) 
    points2, indices2 = prim.tube(radius + pitch/3, radius + 2, depth, 64)
    points1, indices1 = xfm.merge(points1, indices1, points2, indices2)

    return points1, indices1


def reducer(ratio, minor_radius, axle_radius, depth, flip, pitch, twist):

    points1, indices1 = spur(minor_radius, pitch, depth, twist)

    points2, indices2 = spur(minor_radius/ratio, pitch, depth, twist=twist)

    if flip:
        points2 = xfm.translate(points2, 0, 0, depth)
    else:    
        points1 = xfm.translate(points1, 0, 0, depth)

    points1, indices1 = xfm.merge(points1, indices1, points2, indices2)

    points2, indices2 = prim.tube(axle_radius, minor_radius - 1, depth, 64)

    points3, indices3 = prim.tube(
        axle_radius, minor_radius/ratio - 1, depth, 64)

    if flip:
        points3 = xfm.translate(points3, 0, 0, depth)
    else:
        points2 = xfm.translate(points2, 0, 0, depth)

    points2, indices2 = xfm.merge(points2, indices2, points3, indices3)

    points1, indices1 = xfm.merge(points1, indices1, points2, indices2)

    return points1, indices1

def cycloidal_cog(radius, cam_radius, rod_radius, travel, depth, num_waves, length):
    """
    points1, indices1 = prim.sinus_cog(28.5, 5, 360, 12, 0.8)
    points2, indices2 = prim.sinus_ring(32.5, 10, 360, 11.6129, 0.8)
    """
    points1, indices1 = prim.sinus_cog(radius, depth, 360, 360/num_waves, length)

    points2, indices2 = prim.tube(cam_radius, cam_radius + 5, depth, 64)

    points1, indices1 = xfm.merge(points1, indices1, points2, indices2)

    for index in range(6):
        points2, indices2 = prim.tube(rod_radius + travel, rod_radius + travel + 5, depth, 64)
        points2 = xfm.translate(points2, cam_radius + (radius - cam_radius) / 2 , 0, 0)
        points2 = xfm.rotate(points2, 60 * index, 2)
        points1, indices1 = xfm.merge(points1, indices1, points2, indices2)

    return points1, indices1

def cycloidal_ring(radius,  depth, num_waves, length):
    """
    points1, indices1 = prim.sinus_cog(28.5, 5, 360, 12, 0.8)
    points2, indices2 = prim.sinus_ring(32.5, 10, 360, 11.6129, 0.8)
    """
    points1, indices1 = prim.sinus_ring(radius, depth, 360, 360/num_waves, length)

    # points2, indices2 = prim.tube(radius + length, radius + length + 4, depth, 64)

    # points1, indices1 = xfm.merge(points1, indices1, points2, indices2)

    return points1, indices1
