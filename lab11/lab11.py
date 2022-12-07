import numpy as np
import cv2 
import matplotlib.pyplot as plt
import time

start = time.perf_counter() #timestart

img1 = cv2.imread('1.jpg',cv2.IMREAD_GRAYSCALE)          # queryImage
img2 = cv2.imread('2.jpg',cv2.IMREAD_GRAYSCALE)          # trainImage

# Initiate detector
#detector = cv2.xfeatures2d.SURF_create()
#detector = cv2.xfeatures2d.SIFT_create()
detector = cv2.ORB_create()

# find the keypoints and descriptors with SIFT
kp1, des1 = detector.detectAndCompute(img1,None)
kp2, des2 = detector.detectAndCompute(img2,None)


bf = cv2.BFMatcher()
matches = bf.knnMatch(des1,des2,k=2)

# Apply ratio test
good = []
for m,n in matches:
    if m.distance < 0.75*n.distance:
        good.append([m])

end = time.perf_counter()
print("Time spent by mothod of ORB:",end - start)

#cv.drawMatchesKnn expects list of lists as matches.
img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good[:51],None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

plt.imshow(img3),plt.show()

