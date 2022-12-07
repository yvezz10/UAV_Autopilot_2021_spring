import cv2
import numpy as np
import tello
import time


def main():
    drone = tello.Tello('', 8889)
    
    
    dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
    parameters = cv2.aruco.DetectorParameters_create()
    
    cv_file = cv2.FileStorage("data.xml", cv2.FILE_STORAGE_READ)
    intrinsic = cv_file.getNode("intrinsic").mat()
    distortion = cv_file.getNode("distortion").mat()
    cv_file.release()
    time.sleep(10)
    print("ok")

    drone.takeoff()

    while(True):
        frame = drone.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        markerCorners, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(frame, dictionary, parameters=parameters)

        if (markerIds == 2):
            frame = cv2.aruco.drawDetectedMarkers(frame, markerCorners, markerIds)
            rvec, tvec, _objPoints = cv2.aruco.estimatePoseSingleMarkers(markerCorners, 15 ,intrinsic ,distortion )
            label = "x: "+ str(round(tvec[0][0][0],2))+" y: "+ str(round(tvec[0][0][1],2))+ " z: "+ str(round(tvec[0][0][2],2))
            frame = cv2.aruco.drawAxis(frame, intrinsic, distortion, rvec, tvec, 6)
            cv2.putText(frame,label,(360,640),cv2.FONT_HERSHEY_SIMPLEX ,1,(255,255,255),2)
            zDistance = round((70 - tvec[0][0][2])/100,3)
            yDistance = round(tvec[0][0][1]/100,3)
            xDistance = round(tvec[0][0][0]/100,3)
            zAngle = round(rvec[0][0][2],3)
            
            if (zAngle>0.05):
                drone.rotate_cw(zAngle*180*0.5/3.1415927)
            elif(zAngle < -0.05):
                drone.rotate_ccw(-zAngle*180*0.5/3.1415927)

            if (zDistance < -0.1) :
                drone.move_forward(-zDistance*0.6)
            elif(zDistance > 0.1) :
                drone.move_backward(zDistance*0.6)

            if (yDistance < -0.03) :
                drone.move_up (-yDistance)
            elif(yDistance > 0.03):
                drone.move_down(yDistance)

            if (xDistance < -0.03) :
                drone.move_right(-xDistance)
            elif(xDistance > 0.03):
                drone.move_left(xDistance)

            


        cv2.imshow("drone", frame)
        key = cv2.waitKey(1)
        
        if key!= -1: 
            drone.keyboard(key)
    
    cv2.destroyAllWindows()
            
if __name__ == "__main__": 
    main()


        