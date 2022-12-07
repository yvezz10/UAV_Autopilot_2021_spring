import cv2
import numpy as np
import time

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.1)

objp = np.zeros((6*9,3), np.float32)
objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)

objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.
cnt = 0
cap = cv2.VideoCapture(0)

    
    
while(True):
    ret, img = cap.read()
    frame = img[0:720,0:1080]
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, (9,6), None)
    
    if(ret == True):
        cnt +=1
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners2)
        if(cnt==50):
            retval, cameraMatrix, distCoeffs, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints,gray.shape[::-1], None,None)
            f = cv2.FileStorage('data.xml', cv2.FILE_STORAGE_WRITE)
            f.write("intrinsic", cameraMatrix)
            f.write("distortion", distCoeffs)
            f.release()
            print("finish")
            break
        
    cv2.imshow('frame', gray)
    if (cv2.waitKey(33)&0xFF == ord('q')):
        break
cv2.destroyAllWindows()
cv2.waitKey(1)