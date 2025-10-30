import transform as xfm
import machine as mach
import primitive as prim
import objio  as obj
import stlio
import sys

if __name__ == "__main__":

    points, indices = mach.gear_wheel(12, 3, 7)
    stlio.save("/Users/bsloan/Desktop/rack_gear.stl", points, indices)


