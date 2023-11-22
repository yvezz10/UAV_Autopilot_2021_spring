import cv2
import numpy as np

img = cv2.imread('Lenna.png')
h, w = img.shape[:2]

new = np.zeros([h,w,3],dtype=np.uint8)
for i in range(h):
    for j in range(w):
        new[i,j] = img[i,w-j-1]

cv2.imwrite('flip_result.jpg', new)

new2 = np.zeros([w,h,3],dtype=np.uint8)
for i in range(w):
    for j in range(h):
        new2[i,j] = img[j,-i]

cv2.imwrite('rotate_result.jpg', new2)

new3 = np.zeros([h*3,w*3,3],dtype=np.uint8)
for i in range(h*3):
    for j in range(w*3):
        x = round(j/3)
        if (x>w-1):
            x = w-1
        y = round(i/3)
        if (y>h-1):
            y = h-1
        new3[i,j] = img[y,x]


cv2.imwrite('nearst_result.jpg', new3)


new4 = np.zeros([h*3,w*3,3],dtype=np.uint8)
for i in range(h*3):
    for j in range(w*3):
        x = int(j/3)
        y = int(i/3)
        if(x ==w-1 or y == h-1):
            break
        else:
            p1 = ((j-x*3)/3)*img[y,x+1] + (((x+1)*3-j)/3)*img[y,x]
            p2 = ((j-x*3)/3)*img[y+1,x+1] + (((x+1)*3-j)/3)*img[y+1,x]
            px = ((i-y*3)/3)*(p2) + (((y+1)*3-i)/3)*(p1)
        new4[i,j] = px

cv2.imwrite('bilinear_result.jpg', new4)

# cv2.imshow('result', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# cv2.waitKey(1)