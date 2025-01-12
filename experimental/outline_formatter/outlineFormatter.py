import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread('msg4.jpg', 0)

# find lines by horizontally blurring the image and thresholding
blur = cv2.blur(image, (91,9))
b_mean = np.mean(blur, axis=1)/256

# hist, bin_edges = np.histogram(b_mean, bins=100)
# threshold = bin_edges[66]
threshold = np.percentile(b_mean, 66)
t = b_mean > threshold
'''
get the image row numbers that has text (non zero)
a text line is a consecutive group of image rows that 
are above the threshold and are defined by the first and 
last row numbers
'''
tix = np.where(1-t)
tix = tix[0]
lines = []
start_ix = tix[0]
for ix in range(1, tix.shape[0]-1):
    if tix[ix] == tix[ix-1] + 1:
        continue
    # identified gap between lines, close previous line and start a new one
    end_ix = tix[ix-1]
    lines.append([start_ix, end_ix])
    start_ix = tix[ix]
end_ix = tix[-1]
lines.append([start_ix, end_ix])

l_starts = []
for line in lines:
    center_y = int((line[0] + line[1]) / 2)
    xx = 500
    for x in range(0,500):
        col = image[line[0]:line[1], x]
        if np.min(col) < 64:
            xx = x
            break
    l_starts.append(xx)

median_ls = np.median(l_starts)

paragraphs = []
p_start = lines[0][0]

for ix in range(1, len(lines)):
    if l_starts[ix] > median_ls * 2:
        p_end = lines[ix][0] - 10
        paragraphs.append([p_start, p_end])
        p_start = lines[ix][0]

p_img = np.array(image)
n_cols = p_img.shape[1]
for paragraph in paragraphs:
    cv2.rectangle(p_img, (5, paragraph[0]), (n_cols - 5, paragraph[1]), (128, 128, 0), 5)

cv2.imwrite('paragraphs_out.jpg', p_img)