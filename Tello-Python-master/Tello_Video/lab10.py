import cv2
import numpy as np
import tello
import time

def main():
    cap = cv2.VideoCapture(0)
    kernel_size = 5
    trackingFlag = 0
    movFlag = 0
    threshold =2000
    drone = tello.Tello('', 8889)
    
    dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
    parameters = cv2.aruco.DetectorParameters_create()
    
    cv_file = cv2.FileStorage("data.xml", cv2.FILE_STORAGE_READ)
    intrinsic = cv_file.getNode("intrinsic").mat()
    distortion = cv_file.getNode("distortion").mat()
    cv_file.release()

    drone.takeoff()
    print("ok!")
    while(True):
        ret, img = cap.read()
        frame = img[0:720,0:1080]
        if np.all(frame is not None):
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            blur_gray = cv2.GaussianBlur(gray,(kernel_size, kernel_size), 0)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) #aruco
            edges_frame = cv2.Canny(blur_gray, 70, 200)
            dilation = cv2.dilate(edges_frame, (kernel_size, kernel_size), 1)

        markerCorners, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(frame, dictionary, parameters=parameters)

        if np.all(markerIds is not None):

            frame = cv2.aruco.drawDetectedMarkers(frame, markerCorners, markerIds)

            for i in range(0, len(markerIds)):
                rvec, tvec, _objPoints = cv2.aruco.estimatePoseSingleMarkers(markerCorners[i], 15, intrinsic ,distortion)
                (rvec-tvec).any() #我也不知道為什麼要有這個

                #到起點
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

                    if (abs(zAngle)<30 and abs(zDistance)<0.35 and abs(xDistance)<0.15 and abs (yDistance)<0.15):
                        print("check!")
                        if trackingFlag ==0 :
                            drone.move_right(0.4)
                            time.sleep(4)

                        if trackingFlag ==1:
                            time.sleep(2)
                            print("end!")
                            drone.land()
        if(trackingFlag == 1):
            first = 0
            second = 0
            third = 0
            forth = 0

            for i in range(360):
                for j in range(480):
                    if dilation[i][j] == 255:
                        second+=1
            for i in range(360):
                for j in range(481,959):
                    if dilation[i][j] == 255:
                        first+=1
            for i in range(361,719):
                for j in range(480):
                    if dilation[i][j] == 255:
                        third +=1
            for i in range(361,719):
                for j in range(481,959):
                    if dilation[i][j] == 255:
                        forth +=1

            if movFlag == 0 : #水平向右飛行
                if (first + forth)> threshold :
                    if(first>forth):
                        drone.move_up(0.3)
                        movFlag = 1
                        time.sleep(1)
                    else:
                        drone.move_down(0.3)
                        movFlag = 3
                        time.sleep(1)
                else:
                    drone.move_right(0.3)
                    time.sleep(1)

            if movFlag == 1 : #垂直向上飛行
                if (first + second)> threshold :
                    if(first>second):
                        drone.move_right(0.3)
                        movFlag = 0
                        time.sleep(1)
                    else:
                        drone.move_left(0.3)
                        movFlag = 2
                        time.sleep(1)
                else:
                    drone.move_up(0.3)
                    time.sleep(1)

            if movFlag == 2 : #水平向左飛行
                if (third + second)> threshold :
                    if(second>third):
                        drone.move_up(0.3)
                        movFlag = 1
                        time.sleep(1)
                    else:
                        drone.move_down(0.3)
                        trackingFlag =1
                        movFlag = 3
                        time.sleep(1)
                else:
                    drone.move_left(0.3)
                    time.sleep(1)
            
            if movFlag == 3 : #垂直向下飛行
                trackingFlag = 2
                if (third+forth)> threshold :
                    if(forth>third):
                        drone.move_right(0.3)
                        movFlag = 0
                        time.sleep(1)
                    else:
                        drone.move_left(0.3)
                        movFlag = 2
                        time.sleep(1)
                else:
                    drone.move_down(0.3)
                    time.sleep(1)

        cv2.imshow("drone", dilation)
        key = cv2.waitKey(1)
        
        if key!= -1: 
            drone.keyboard(key)
            
if __name__ == "__main__": 
    main()
