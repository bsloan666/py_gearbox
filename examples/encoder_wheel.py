import transform as xfm
import primitive as prim
import stlio
import sys


def to_bin_string(in_val:int):
    """
    convert an integer to a binary string
    """
    return bin(in_val)


def to_integer(in_val:str):
    """
    convert a binary string to an integer
    """
    return int(in_val, 2)


def to_graycode(in_val:int):
    """
    convert an ordinal integer into a graycode integer
    """
    result = "0b"
    binstr = "0" + to_bin_string(512 + in_val)[-8:]
    for index in range(8):
        a = int(binstr[index])
        b = int(binstr[index + 1])
        if a == b:
            result += '0'
        else:
            result += '1'

    return to_integer(result)


def run():
    mapping = []
    for x in range(256):
        y = to_graycode(x)
        mapping.append(y)  

    inv_map = [0] * 256
    for x, y in enumerate(mapping):
        inv_map[y] = x

    print("int gray_lookup[256] = {")

    columns = 8
    column_count = 0
    row = "  "

    for x in inv_map:
        row  += f"{x:4},"
        column_count += 1
        if column_count > 7:
            print(row)
            row = "  "
            column_count = 0


    print(row)

    print("};")


    INNER_DIA = 18
    RING_WIDTH = 4
    SUPPORT_WIDTH = 1
    
    points, indices = prim.tube(INNER_DIA - SUPPORT_WIDTH * 3, INNER_DIA, 2, 256, 360)

    # make retainer rings
    for index in range(8):
        inner = INNER_DIA + index * RING_WIDTH 
        points1, indices1 = prim.tube(inner+(RING_WIDTH-SUPPORT_WIDTH), inner + RING_WIDTH, 2, 256, 360)
        points, indices = xfm.merge(
           points, indices, points1, indices1)
  
    steps = pow(2, 8)
    degrees = 360/256 

    sections = [[],[],[],[],[],[],[],[]]

    for step in range(steps):
        for index in range(8):
            degree_offset = index * 10
            inner = INNER_DIA + (7 - index) * RING_WIDTH 
            if ((mapping[step] >> index) & 1) == 0:
                
                points1, indices1 = prim.tube(inner, inner+(RING_WIDTH-SUPPORT_WIDTH), 2, 512, degrees)
                points1 = xfm.rotate(points1, degrees * step + degree_offset, 2)

                points, indices = xfm.merge(
                   points, indices, points1, indices1)

    stlio.save(sys.argv[1], points, indices)


if __name__ == "__main__":
    run()
