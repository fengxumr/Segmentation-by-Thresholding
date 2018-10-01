import numpy as np
import argparse, cv2

parser = argparse.ArgumentParser()
parser.add_argument('--input', dest='img_in')
parser.add_argument('--output', dest='img_out')
parser.add_argument('--threshold', dest='print', action='store_true')
args = parser.parse_args()

# print(args.img_in, args.img_out, args.print)

## otsu_threshold ##

img = cv2.imread(args.img_in, 0)
assert(img.size)

u = float(np.sum(img)) / img.size
g_target = 0
th_target = 0

for th in range(256):
    fore = img > th
    back = img <= th
    fore_pix = np.sum(fore)
    back_pix = np.sum(back)

    if fore_pix * back_pix == 0:
        continue

    w0 = float(fore_pix) / img.size
    w1 = float(back_pix) / img.size

    u0 = float(np.sum(img * fore)) / fore_pix
    u1 = float(np.sum(img * back)) / back_pix

    g = w0 * ((u - u0) ** 2) + w1 * ((u - u1) ** 2)

    if g > g_target:
        g_target = g
        th_target = th

img_binary = img.copy()
img_binary[img_binary > th_target] = 255
img_binary[img_binary <= th_target] = 0 

if args.print:
    print('Threshold:', th_target)

cv2.imwrite(args.img_out, img_binary)

cv2.imshow('image', img_binary)
cv2.waitKey(0)
cv2.destroyAllWindows()