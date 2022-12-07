import cv2
import numpy as np
import tello
import time

def main():
    cap = cv2.VideoCapture(1)
    dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
    parameters = cv2.aruco.DetectorParameters_create()

    cv_file = cv2.FileStorage("data.xml", cv2.FILE_STORAGE_READ)
    intrinsic = cv_file.getNode("intrinsic").mat()
    distortion = cv_file.getNode("distortion").mat()
    cv_file.release()

    while(True):
        ret, frame = cap.read()
        
        markerCorners, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(frame, dictionary, parameters=parameters)
        
        #intrinsic = np.mat([[17289.698936964553, 0, 611.94100644183834],[ 0, 4711.3322707483821, 306.94412706406268] ,[0,  0,  1 ]])
        #distortion = np.mat([-66.287911059283346, 14403.914445747248, 1.1442875801901846, -0.10487340945037757,  93.950771107346853])
        
        

        if markerIds!= None:
            frame = cv2.aruco.drawDetectedMarkers(frame, markerCorners, markerIds)
            rvec, tvec, _objPoints = cv2.aruco.estimatePoseSingleMarkers(markerCorners, 15,intrinsic ,distortion )
            label = "x: "+ str(round(tvec[0][0][0],2))+" y: "+ str(round(tvec[0][0][1],2))+ " z: "+ str(round(tvec[0][0][2],2))
            angle = "x: "+ str(round(rvec[0][0][0],2))+" y: "+ str(round(rvec[0][0][1],2))+ " z: "+ str(round(rvec[0][0][2],2))
            frame = cv2.aruco.drawAxis(frame, intrinsic, distortion, rvec, tvec, 6)
            cv2.putText(frame,label,(360,520),cv2.FONT_HERSHEY_SIMPLEX ,1,(255,255,255),2)
            cv2.putText(frame,angle,(360,640),cv2.FONT_HERSHEY_SIMPLEX ,1,(255,255,255),2)
        cv2.imshow("drone", frame)
        

        if (cv2.waitKey(33)&0xFF == ord('q')):
            break

if __name__ == "__main__": 
    main()
    