#!/usr/bin/env python
# coding: utf-8

# In[5]:


import cv2
import numpy as np

#讀取影片
cap  = cv2.VideoCapture('vtest.avi')
backSub = cv2.createBackgroundSubtractorMOG2()

cnt = 0    #numbers of frame

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (768, 576))

while cap.isOpened():
    flag = 0     #label of pixel
    cnt+=1
    label = []
    
    #catch frame
    ret, frame = cap.read()

    
    #substract the background
    fgmask = backSub.apply(frame)
    shadowval = backSub.getShadowValue()
    ret, nmask = cv2.threshold(fgmask, shadowval, 255, cv2.THRESH_BINARY)
    nmask = cv2.GaussianBlur(nmask,(7,7),0)
    
    #創建新的陣列
    (h,w) = np.shape(nmask)
    mask = np.zeros((h,w), dtype = int)
    for i in range(h):
        for j in range(w):
            mask[i][j] = int(nmask[i][j])
    
    #first pass
    for i in range(h):
        for j in range(w):
            if(mask[i][j]!=0):
                if(i==0 and j ==0):
                    flag+=1
                    mask[i][j] = flag
                elif(i==0):
                    if(mask[i][j-1]!=0):
                        mask[i][j] = mask[i][j-1]
                    else:
                        flag+=1
                        mask[i][j] = flag
                elif(j==0):
                    if(mask[i-1][j]!=0):
                        mask[i][j] =mask[i-1][j]
                    else:
                        flag+=1
                        mask[i][j] =flag
                else:
                    if(mask[i-1][j] != 0 and mask[i][j-1] != 0 and mask[i-1][j] != mask[i][j-1]):
                        mask[i][j] = min(mask[i][j-1], mask[i-1][j])
                        s = set([mask[i][j-1], mask[i-1][j]])
                        label.append(s)
                    elif(mask[i-1][j] != 0 and mask[i][j-1] != 0):
                        mask[i][j] = mask[i-1][j]
                    elif(mask[i][j-1]!=0):
                        mask[i][j] = mask[i][j-1]
                    elif(mask[i-1][j]!=0):
                        mask[i][j] = mask[i-1][j]

                    else:
                        flag+=1
                        mask[i][j] = flag
                        
    #find the same label
    pool = set(map(frozenset, label))
    groups = []
    while pool:
        groups.append(set(pool.pop()))
        while True:
            for candidate in pool:
                if groups[-1] & candidate:
                    groups[-1] |= candidate
                    pool.remove(candidate)
                    break
            else:
                break
                
    #second pass
    arr = [0]*flag
    for i in range(h):
        for j in range(w):
            if (mask[i][j]!=0):
                for m in range(len(groups)):
                    if mask[i][j] in groups[m]:
                        mask[i][j] = min(groups[m])
                arr[mask[i][j]]+=1
                
    #label people(th = 500)
    x1 = [None]*flag
    x2 = [None]*flag
    y1 = [None]*flag
    y2 = [None]*flag
    for i in range(h):
        for j in range(w):
            if (arr[mask[i][j]]>600):
                if(x1[mask[i][j]] == None or x1[mask[i][j]]>i): x1[mask[i][j]] = i
                if(x2[mask[i][j]] == None or x2[mask[i][j]]<i): x2[mask[i][j]] = i
                if(y1[mask[i][j]] == None or y1[mask[i][j]]>j): y1[mask[i][j]] = j
                if(y2[mask[i][j]] == None or y2[mask[i][j]]<j): y2[mask[i][j]] = j
    for i in range(flag):
        if(x1[i]!=None):
            cv2.rectangle(frame,(y1[i],x1[i]),(y2[i],x2[i]),(0,255,0),2)
    
    #show result
    cv2.imshow("frame", frame)
    out.write(frame)
    if (cv2.waitKey(33)&0xFF == ord('q')):
        break
cap.release()
out.release()
cv2.destroyAllWindows()
cv2.waitKey(1)

