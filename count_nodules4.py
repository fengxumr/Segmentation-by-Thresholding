import numpy as np
import argparse, cv2, random

parser = argparse.ArgumentParser()
parser.add_argument('--input', dest='img_in')
parser.add_argument('--size', dest='size', type=int)
parser.add_argument('--optional_output', dest='img_out')
args = parser.parse_args()

img_binary = cv2.imread(args.img_in, 0)
assert(img_binary.size)

## first pass ##

matrix_colour = np.zeros(shape=img_binary.shape)
a, b = img_binary.shape
colour = 1
for i in range(a):
    for j in range(b):
        if img_binary[i][j] == 0:

            neighbour = []
            for n in [[0, -1], [0, 1], [-1, 0], [1, 0]]:
                aa = i + n[0]
                bb = j + n[1]
                if aa >= 0 and aa < a and bb >= 0 and bb < b:
                    neighbour.append([aa, bb])

            con = []
            for m in neighbour:
                if matrix_colour[m[0]][m[1]] > 0:
                    con.append(matrix_colour[m[0]][m[1]])

            if con:
                matrix_colour[i][j] = min(con)
            else:
                matrix_colour[i][j] = colour
                colour += 1

## second pass ##

group = {}
for i in range(a):
    for j in range(b):
        if matrix_colour[i][j] > 0:
            neighbour = []
            for n in [[0, -1], [0, 1], [-1, 0], [1, 0], [0, 0]]:
                aa = i + n[0]
                bb = j + n[1]
                if aa >= 0 and aa < a and bb >= 0 and bb < b:
                    neighbour.append([aa, bb])

            pro = sorted(list(set(matrix_colour[m[0]][m[1]] for m in neighbour) - {0}))

            for k in pro:
                if (k not in group) or (k in group and group[k] > pro[0]):
                    group[k] = pro[0]

flag = 1
while flag:
    flag = 0
    for l in group:
        cur = l
        con = []
        while group[cur] != cur:
            con.append(cur)
            cur = group[cur]
        if len(con) > 1:
            flag = 1
            for e in con[:-1]:
                group[e] = cur

for i in range(a):
    for j in range(b):
        if matrix_colour[i][j] != 0:
            matrix_colour[i][j] = group[matrix_colour[i][j]]

img_colour = np.zeros(shape=img_binary.shape + (3,), dtype=np.uint8) + 255

n = 0
for k in group:
    img_colour[matrix_colour == k] = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
    
    m = np.sum(matrix_colour == k)
    if m > args.size:
        n += 1

print('the number of nodules with area larger than', args.size, 'pixels in the image:', n)

## optional ##

if args.img_out:
    cv2.imwrite(args.img_out, img_colour)
    cv2.imshow(args.img_out, img_colour)
    cv2.waitKey(0)
    cv2.destroyAllWindows()