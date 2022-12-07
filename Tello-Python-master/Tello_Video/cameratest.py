import cv2
import tello
import numpy as np
import time

cap = cv2.VideoCapture(0)
dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
parameters = cv2.aruco.DetectorParameters_create()
    
cv_file = cv2.FileStorage("data.xml", cv2.FILE_STORAGE_READ)
intrinsic = cv_file.getNode("intrinsic").mat()
distortion = cv_file.getNode("distortion").mat()
cv_file.release()
kernel_size = 5
trackingFlag =0
drone = tello.Tello('', 8889)

while True:
    ret, img = cap.read()
    frame = img[0:720,0:1080]
    if np.all(frame is not None):
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) #aruco
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        blur_gray = cv2.GaussianBlur(gray,(kernel_size, kernel_size), 0)
        edges_frame = cv2.Canny(blur_gray, 70, 200)

    markerCorners, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(frame, dictionary, parameters=parameters)

    if np.all(markerIds is not None):
        frame = cv2.aruco.drawDetectedMarkers(frame, markerCorners, markerIds)
        for i in range(0, len(markerIds)):
            rvec, tvec, _objPoints = cv2.aruco.estimatePoseSingleMarkers(markerCorners[i], 15, intrinsic ,distortion)
            (rvec-tvec).any() #我也不知道為什麼要有這個

            #到起
            if(markerIds[i] == 2):
                print ("set！！！")
                label = "x: "+ str(round(tvec[0][0][0],2))+" y: "+ str(round(tvec[0][0][1],2))+ " z: "+ str(round(tvec[0][0][2],2))
                frame = cv2.aruco.drawAxis(frame, intrinsic, distortion, rvec, tvec, 6)
                cv2.putText(frame,label,(360,640),cv2.FONT_HERSHEY_SIMPLEX ,1,(255,255,255),2)

                zDistance = round((40 - tvec[0][0][2])/100,3)
                yDistance = round(tvec[0][0][1]/100,3)
                xDistance = round(tvec[0][0][0]/100,3)
                zAngle = round(rvec[0][0][2]*180/3.1415927,3)


                if (yDistance < 0) :
                    drone.move_up (-yDistance)
                elif(yDistance > 0):
                    drone.move_down(yDistance)

                if (xDistance < 0) :
                    drone.move_left(-xDistance)
                elif(xDistance > 0):
                    drone.move_right(xDistance)

                if (zAngle>0):
                    drone.rotate_cw(zAngle*0.9)
                elif(zAngle < 0):
                    drone.rotate_ccw(-zAngle*0.9)

                if (zDistance < -0.1) :
                    drone.move_forward(-zDistance*0.6)
                elif(zDistance > 0.1) :
                    drone.move_backward(zDistance*0.6)

                if (abs(zAngle)<40 and abs(zDistance)<0.35 and abs(xDistance)<0.15 and abs (yDistance)<0.15 and trackingFlag ==0):
                        print("check!")
                        time.sleep(2)
                        if trackingFlag ==0 :
                            drone.move_right(0.4)
                            trackingFlag =1
                        if trackingFlag ==1 :
                            drone.land()

    


    cv2.imshow("result", frame)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
