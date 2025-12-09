import transform as xfm
import primitive as prim
import stlio
import sys


def run():
    INNER_DIA=14
    RING_WIDTH=6
    SUPPORT_WIDTH=2
    EXTENT=0.711111111
    # EXTENT=1
    
    points, indices = prim.tube(INNER_DIA - 2, INNER_DIA, 2, 256, 360 * EXTENT)

    for index in range(8):
        inner = INNER_DIA + index * 6
        steps = pow(2, index + 1)
        degrees = 360.0 / steps 
        for step in range(steps//2):
            points1, indices1 = prim.tube(inner, inner+(RING_WIDTH-SUPPORT_WIDTH), 2, 512, degrees * EXTENT)
            points1 = xfm.rotate(points1, degrees * 2 * step * EXTENT, 2)

            points, indices = xfm.merge(
               points, indices, points1, indices1)

        points1, indices1 = prim.tube(inner+(RING_WIDTH-SUPPORT_WIDTH), inner + RING_WIDTH, 2, 256, 360 * EXTENT)

        points, indices = xfm.merge(
           points, indices, points1, indices1)

    stlio.save(sys.argv[1], points, indices)


if __name__ == "__main__":
    run()
