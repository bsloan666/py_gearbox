import transform as xfm
import primitive as prim
import stlio
import sys

if __name__ == "__main__":

#    points1, indices1 = prim.cylinder(2.6, 30, 64)
    points1, indices1 = prim.tube(2.6, 24, 10, 64, 180)

#    points1, indices1 = xfm.merge(
#        points1, indices1, points2, indices2)

#    points2, indices2 = prim.torus(30, 8, 64, 360)

#    points2 = xfm.translate(points2, 0, 0, -20)

#    points1, indices1 = xfm.merge(
#        points1, indices1, points2, indices2)

#    points2, indices2 = prim.box(20, 20, 20)

#    points2 = xfm.translate(points2, -10, -10, 20)

#    points1, indices1 = xfm.merge(
#        points1, indices1, points2, indices2)

#    points2, indices2 = prim.cone(5, 20, 20, 64)

 #   points2 = xfm.translate(points2, 0, 0, 40)

#    points1, indices1 = xfm.merge(
#        points1, indices1, points2, indices2)

#    points2, indices2 = prim.sphere(15, 64, 180)

#    points2 = xfm.translate(points2, 0, 0, 80)

#    points1, indices1 = xfm.merge(
#        points1, indices1, points2, indices2)

    stlio.save(sys.argv[1], points1, indices1)
