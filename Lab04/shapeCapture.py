#!/usr/bin/env python
# coding: utf-8

# In[3]:


import numpy as np
import cv2




cap = cv2.VideoCapture(0)
img = cv2.imread('warp.jpg')
capCorner = np.float32([[0,0], [0,719], [1279,719], [1279,0]])
imgCorner = np.float32([[241,201], [258,630],[433,761],[573,246]])
perMatrix = cv2.getPerspectiveTransform(capCorner, imgCorner)
inverse = np.linalg.inv(perMatrix)
def inSquare(x,y):
    if((45*x-222*y+33777)<0 and (131*x-175*y+76452)>0): 
        if((429*x-17*y-99972)>0 and (515*x+30*y-245825)<0):
            return True
while(True):
    ret, frame = cap.read()
    new = np.zeros([937,750,3],dtype=np.uint8)
    new = img
    for i in range(201,761):
        for j in range(241,463):
            if inSquare(j,i) == True:
                x1 = inverse[0][0]*j + inverse[0][1]*i + inverse[0][2]
                y1 = inverse[1][0]*j + inverse[1][1]*i + inverse[1][2]
                if(x1>1280 or y1 >720):
                    new[i][j] = img[i][j]
                else:
                    p1 = (x1- int(x1))*frame[int(y1)][int(x1)+1] + (1 - x1 + int(x1))*frame[int(y1)][int(x1)]
                    p2 = (x1- int(x1))*frame[int(y1)+1][int(x1)+1] + (1 - x1 + int(x1))*frame[int(y1)+1][int(x1)]
                    px = (y1- int(y1))*p2 + (1 - y1 + int(y1))*p1
                    new[i][j] = px
            else:
                new[i][j] = img[i][j]
    #show result
    cv2.imshow("frame", new)
    if (cv2.waitKey(33)&0xFF == ord('q')):
        break
cap.release()
cv2.destroyAllWindows()
cv2.waitKey(1)

