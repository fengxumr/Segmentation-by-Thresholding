import numpy as np
import argparse, cv2, math


def smoothing(img):
    m, n = img.shape
    for i in range(2, m - 2):
        for j in range(2, n - 2):
            img[i][j] = np.sum(img[i-2:i+3, j-2:j+3]) / 25

    img[img > 255] = 255
    img[img < 0] = 0


def otsu_threshold(arr):
    u = float(np.sum(arr)) / arr.size
    g_target = 0
    th_target = 0

    for th in range(256):
        fore = arr > th
        back = arr <= th
        fore_pix = np.sum(fore)
        back_pix = np.sum(back)

        if fore_pix == 0:
            break
        if back_pix == 0:
            continue

        w0 = float(fore_pix) / arr.size
        w1 = float(back_pix) / arr.size
        u0 = float(np.sum(arr * fore)) / fore_pix
        u1 = float(np.sum(arr * back)) / back_pix
        g = w0 * ((u - u0) ** 2) + w1 * ((u - u1) ** 2)

        if g > g_target:
            g_target = g
            th_target = th

    return th_target


parser = argparse.ArgumentParser()
parser.add_argument('--input', dest='img_in')
parser.add_argument('--output', dest='img_out')
args = parser.parse_args()

# print(args.img_in, args.img_out, args.grid)


img = cv2.imread(args.img_in, 0)
assert(img.size)

img_binary = img.copy()
smoothing(img_binary)

th = otsu_threshold(img_binary)
img_binary[img_binary > th] = 255
img_binary[img_binary <= th] = 0

cv2.imwrite(args.img_out, img_binary)

cv2.imshow('image', img_binary)
cv2.waitKey(0)
cv2.destroyAllWindows()


