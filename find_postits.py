#!/usr/bin/env python

'''
Simple "Square Detector" program.

Loads several images sequentially and tries to find squares in each image.
'''

# Python 2/3 compatibility
import sys
PY3 = sys.version_info[0] == 3

import numpy as np
import cv2
from matplotlib import pyplot as plt
from imutils import perspective, opencv2matplotlib

import kde

def show(title, image):
    plt.figure(title)
    plt.imshow(opencv2matplotlib(image))
    plt.show()

def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

def find_squares(img):
    img = cv2.GaussianBlur(img, (5, 5), 0)
    squares = []
    areas = []
    for gray in cv2.split(img):
        for thrs in range(0, 255, 25):

            if thrs == 0:
                bin = cv2.Canny(gray, 0, 50, apertureSize=5)
                bin = cv2.dilate(bin, None)
                
            else:
                retval, bin = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)

            bin, contours, hierarchy = \
                cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            
            for cnt in contours:
                cnt_len = cv2.arcLength(cnt, True)
                cnt = cv2.approxPolyDP(cnt, 0.02 * cnt_len, True)
                # cnt = cv2.approxPolyDP(cnt, 0.04 * cnt_len, True)
                area = cv2.contourArea(cnt)
                if len(cnt) == 4 and area > 1000 and cv2.isContourConvex(cnt):
                    cnt = cnt.reshape(-1, 2)
                    max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in range(4)])
                    # if max_cos < 0.1:
                    if max_cos < 0.5:
                        areas.append(area)
                        squares.append(cnt)

                    
    area_mode = kde.median(areas)
    print >> sys.stderr, area_mode
    
    result = []
    for area, square in zip(areas, squares):
        if area_mode / 5.0 <= area <= area_mode * 5.0:
            result.append(square)

    similar_squares = kde.cluster(result)

    return similar_squares

def histogram_equalize(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
    b, g, r = cv2.split(img)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    b1 = clahe.apply(b)
    g1 = clahe.apply(g)
    r1 = clahe.apply(r)
    # red = cv2.equalizeHist(r)
    # green = cv2.equalizeHist(g)
    # blue = cv2.equalizeHist(b)
    # result = cv2.merge((blue, green, red))
    result = cv2.merge((b1, g1, r1))
    return cv2.cvtColor(result, cv2.COLOR_YCrCb2BGR)

if __name__ == '__main__':

    filename = sys.argv[1]
    img = cv2.imread(filename)
    squares = find_squares(img)

    print >> sys.stderr, 'n squares', len(squares)

    histogram_equalize(img)
    drawn = img.copy()
    cv2.drawContours(drawn, squares, -1, (0, 255, 0), 5 )
    show('squares', drawn)

    postit_size = 200
    pts2 = np.float32([[0,0],[0,postit_size],[postit_size,postit_size],[postit_size,0]])
    for number, square in enumerate(squares, 1):
        print square, pts2
        M = cv2.getPerspectiveTransform(
            perspective.order_points(square.astype('float32')),
            perspective.order_points(pts2),
        )
        dst = cv2.warpPerspective(img, M, (postit_size, postit_size))
        histogram_equalize(dst)
        # show('one', dst)
        outname = 'yomama-postit-%02i.png' % number
        cv2.imwrite(outname, dst)
    
