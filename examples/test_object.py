import sys
import primitive as prim
import machine as mach
import stlio

#points, indices = prim.torus(60, 40, 64, 90)
#points, indices = prim.tapered_torus_arc(60, 40, 30, 64, 90)
points, indices = mach.pinion(13.8, 4, 9, 180)

stlio.save(sys.argv[1], points, indices)
