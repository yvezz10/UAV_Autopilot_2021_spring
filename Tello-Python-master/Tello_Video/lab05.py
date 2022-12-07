import cv2
import numpy as np
import tello
import time


def main():
    drone = tello.Tello('', 8889)
    time.sleep(10)
    
    while(True):
        frame = drone.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
        parameters = cv2.aruco.DetectorParameters_create()
        markerCorners, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(frame, dictionary, parameters=parameters)
        
        
        intrinsic = np.mat([[9.2759580579431076e+02, 0, 5.2185963300061076e+02],[ 0, 9.3864921003663153e+02,  3.4223452702244828e+02 ] ,[0,  0,  1 ]])
        distortion = np.mat([-5.1075504953904290e-02, 3.7896085121237044e-02, 3.6352870304909291e-04 , -3.0427323365178004e-03, 2.2915388996498648e-01])
        
        
        print(markerIds)
        if (markerIds!=None):
            frame = cv2.aruco.drawDetectedMarkers(frame, markerCorners, markerIds)
            rvec, tvec, _objPoints = cv2.aruco.estimatePoseSingleMarkers(markerCorners, 15 ,intrinsic ,distortion )
            label = "x: "+ str(round(tvec[0][0][0],2))+" y: "+ str(round(tvec[0][0][1],2))+ " z: "+ str(round(tvec[0][0][2],2))
            frame = cv2.aruco.drawAxis(frame, intrinsic, distortion, rvec, tvec, 6)
            cv2.putText(frame,label,(360,640),cv2.FONT_HERSHEY_SIMPLEX ,1,(255,255,255),2)

        cv2.imshow("drone", frame)
        key = cv2.waitKey(1)

        
        if key!= -1: 
            drone.keyboard(key)
            
        cv2.destroyAllWindows()
if __name__ == "__main__": 
    main()