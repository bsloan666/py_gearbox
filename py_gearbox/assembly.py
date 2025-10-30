import os
import sys
import primitive as prim
import machine as mach
import transform as xfm
import stlio
import component as comp


def planetary(sun_radius, ring_radius, planet_axle_radius, sun_axle_radius, depth, pitch, twist, out_dir):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    sun_teeth = mach.gear_wheel(sun_radius, pitch, 0)
    planet_radius = (ring_radius - sun_radius)/2
    planet_teeth = mach.gear_wheel(planet_radius, pitch, 0)
    
    ring_teeth = mach.internal_gear(ring_radius, pitch, 0)
    required_ring_teeth = planet_teeth * 2 + sun_teeth

    print("RING_TEETH:")
    print("    ACTUAL:  ", ring_teeth)
    print("    REQUIRED:", required_ring_teeth)
    print("    {0} + {1} X 2".format(sun_teeth, planet_teeth))

    print("GEAR_RATIO: {0}".format(sun_teeth/(ring_teeth + sun_teeth)))
    
    points1, indices1 = comp.spur(sun_radius, sun_axle_radius, depth, pitch, -twist) 
    points2, indices2 = comp.spur(planet_radius, planet_axle_radius, depth, pitch, twist)
    points3, indices3 = comp.ring(ring_radius, depth, pitch, -twist)

    points1 = xfm.rotate(points1, 360/sun_teeth/-1.6, 2)
    stlio.save(os.path.join(out_dir, "sun.stl"), points1, indices1)

    points3 = xfm.rotate(points3, 360/ring_teeth/1.6, 2)
    stlio.save(os.path.join(out_dir, "ring.stl"), points3, indices3)

    points2 = xfm.translate(points2, sun_radius + planet_radius, 0, 0)
    stlio.save(os.path.join(out_dir, "planet_1.stl"), points2, indices2)
        
    points2 = xfm.translate(points2, (sun_radius + planet_radius) * -2, 0, 0)
    stlio.save( os.path.join( out_dir, "planet_2.stl"), points2, indices2)

    points2 = xfm.translate(points2, sun_radius + planet_radius, 0, 0)
    points2 = xfm.translate(points2, 0, sun_radius + planet_radius,  0)
    stlio.save(os.path.join( out_dir, "planet_3.stl"), points2, indices2)
    
    points2 = xfm.translate(points2, 0, (sun_radius + planet_radius) * -2,  0)
    stlio.save(os.path.join(out_dir, "planet_4.stl"), points2, indices2)


def reducer_stack(ratio, repeats, minor_radius, axle_radius, depth, flip, twist, out_dir):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    height = -depth

    for index in range(repeats):
        sign = 1    
        if index % 2:
            sign = -1
        if index == repeats - 1:
            points, indices = comp.spur(minor_radius/ratio, axle_radius, depth, twist*sign)
        else:    
            points, indices = comp.reducer(ratio, minor_radius, axle_radius, depth, flip, twist=twist*sign)
        points = xfm.translate(points, 0, 0, (index + 1) * depth)
        if not index:
            points = xfm.rotate(points, 7, 2)
        if index % 2:
            points = xfm.rotate(points, 3, 2)
            points = xfm.translate(points, minor_radius + minor_radius / ratio, 0, 0)

        stlio.save(
            os.path.join(
                out_dir, "reducer_{0}.stl".format(index)), points, indices)
        height -= depth

    height -= depth * 2
    points, indices = prim.cylinder(axle_radius - 0.1, height, 64)
    points = xfm.translate(points, 0, 0, -height)
    stlio.save(os.path.join(out_dir, "axle_1.stl"), points, indices)
    points = xfm.translate(points, minor_radius + minor_radius / ratio, 0, 0)
    stlio.save(os.path.join(out_dir, "axle_2.stl"), points, indices)
    points, indices = prim.tube(axle_radius, minor_radius / ratio, depth / 2, 64)
    points = xfm.translate(points, 0, 0, depth/2)
    stlio.save(os.path.join(out_dir, "case_1.stl"), points, indices)
    points = xfm.translate(points, minor_radius + minor_radius / ratio, 0, 0)
    stlio.save(os.path.join(out_dir, "case_2.stl"), points, indices)
    points = xfm.translate(points, 0, 0, (repeats + 1) * depth)
    stlio.save(os.path.join(out_dir, "case_3.stl"), points, indices)
    points = xfm.translate(points, -(minor_radius + minor_radius / ratio), 0, 0)
    stlio.save(os.path.join(out_dir, "case_4.stl"), points, indices)


def right_angle_transmission(radius, axle_radius_in, axle_radius_out, depth, twist, out_dir):
    nteeth = mach.gear_wheel(radius, 6,  0)
    points, indices = comp.bevel_spur(radius, axle_radius_in,  depth, twist)
    points = xfm.rotate(points, 360/nteeth/2, 2)
    stlio.save(os.path.join(out_dir, "bevel_gear1.stl"), points, indices)
    points, indices = comp.bevel_spur(radius, axle_radius_out,  depth, -twist)
    points = xfm.rotate(points, 180, 2)
    points = xfm.rotate(points, -90, 1)
    points = xfm.translate(points, radius, 0, radius)
    stlio.save(os.path.join(out_dir, "bevel_gear2.stl"), points, indices)


def single_gear(radius, axle_radius, pitch, depth, out_dir):
    nteeth = mach.gear_wheel(radius, pitch, 0)
    print(f"Simple spur gear with {nteeth} teeth.")
    points, indices = comp.simple_spur(radius, axle_radius, depth, pitch)
    stlio.save(os.path.join(out_dir, "single_gear.stl"), points, indices)

    
def cycloidal_drive(radius, cam_radius, rod_radius, travel, depth, num_waves, crest, out_dir):
    points, indices = comp.cycloidal_cog(radius - crest * 2, cam_radius, rod_radius, travel, depth, num_waves, crest)
    stlio.save(os.path.join(out_dir, "cycloid_hub.stl"), points, indices)
    points, indices = comp.cycloidal_ring(radius + crest * 2,  depth, num_waves + 1, crest)
    stlio.save(os.path.join(out_dir, "cycloid_ring.stl"), points, indices)
