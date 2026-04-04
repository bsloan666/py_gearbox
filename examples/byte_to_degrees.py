import os 
import sys


a_min = 0
a_max = 255


b_min = 0
b_max = 360 


scale = (b_max - b_min)/(a_max - a_min)
offset = (a_min + b_min)

columns = 8
column_count = 0
row = "  "

print("int degree_lookup[256] = {")

for x in range(a_max - a_min):
    row  += f"{round(x * scale + offset):4},"
    column_count += 1
    if column_count > 7:
        print(row)
        row = "  "
        column_count = 0


print(row)

print("};")



