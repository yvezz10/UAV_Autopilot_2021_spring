import cv2
import numpy as np

img = cv2.imread('input.jpg')
h, w = img.shape[:2]
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

a = [0] * 256
for i in range(h):
    for j in range(w):
        k=gray[i,j]
        p = int(k)
        a[p]+=1

avg = [0]*256
aavg = 0 
for i in range(256):
    avg[i] = a[i]*i
for j in range(256):
    aavg = aavg +avg[i]

sum_of_a = 0
sum_of_avg = 0
for i in range(256):
    sum_of_a = sum_of_a+a[i]
    sum_of_avg = sum_of_avg+avg[i]

max_num = 0
flag = 0
target_number = 0
current_nb = 0
current_no = sum_of_a
current_ub = 0
current_uo = sum_of_avg
#culculate threshold from 0-255
for i in range(255):
    current_nb = current_nb+a[i]
    current_no = current_no-a[i]
    current_ub = current_ub+avg[i]
    current_uo = current_uo-avg[i]
    target_number = current_nb*current_no*(current_ub/current_nb-current_uo/current_no)*(current_ub/current_nb-current_uo/current_no)
    if(target_number>max_num):
        max_num=target_number
        flag = i

new = np.zeros([h,w,1],dtype=np.uint8)
for i in range(h):
    for j in range(w):
        if (gray[i,j]>118):
            new[i,j]=255
        else:
            new[i,j]=0

cv2.imshow('result', new)
cv2.imwrite('result.jpg', new)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)