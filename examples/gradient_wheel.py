import transform as xfm
import primitive as prim
import stlio
import sys
import math

def run():

    INNER_RAD = 45 
    RING_WIDTH = 5
    SUPPORT_WIDTH = 1
    THICKNESS = 2
    MIN_WID = 0.25

    steps = 160
    degrees = 360/steps 
    
    arclen = (math.pi * (INNER_RAD + RING_WIDTH) * 2) / steps - MIN_WID * 2

    increment = arclen / steps 


    points, indices = prim.tube(INNER_RAD - SUPPORT_WIDTH, INNER_RAD + 0.2, THICKNESS, 256, 360)

    points1, indices1 = prim.tube(INNER_RAD + RING_WIDTH, INNER_RAD + RING_WIDTH + SUPPORT_WIDTH, THICKNESS, 256, 360)
    points, indices = xfm.merge(
       points, indices, points1, indices1)


    for step in range(steps):
        width = MIN_WID +  step * increment

        points1, indices1 = prim.box(5, width, THICKNESS) 
                
        points1 = xfm.translate(points1, INNER_RAD, -arclen/2, 0)
        points1 = xfm.rotate(points1, degrees * step, 2)
        points, indices = xfm.merge(
           points, indices, points1, indices1)

    stlio.save(sys.argv[1], points, indices)


if __name__ == "__main__":
    run()
