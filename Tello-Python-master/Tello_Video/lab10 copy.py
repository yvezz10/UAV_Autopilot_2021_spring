import cv2
import numpy as np
import time

def main():
    cap = cv2.VideoCapture(1)
    kernel_size = 5
    trackingFlag = 0
    movFlag = 0
    threshold =2000
    
    dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
    parameters = cv2.aruco.DetectorParameters_create()
    
    cv_file = cv2.FileStorage("data.xml", cv2.FILE_STORAGE_READ)
    intrinsic = cv_file.getNode("intrinsic").mat()
    distortion = cv_file.getNode("distortion").mat()
    cv_file.release()

    print(">> send cmd: takeoff")
    print("ok!")
    while(True):
        ret, img = cap.read()
        frame = img[0:720,0:1080]
        if np.all(frame is not None):
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            blur_gray = cv2.GaussianBlur(gray,(kernel_size, kernel_size), 0)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) #aruco
            #edges_frame = cv2.Canny(blur_gray, 70, 200)
            #dilation = cv2.dilate(edges_frame, (kernel_size, kernel_size), 2)
            dilation = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        markerCorners, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(frame, dictionary, parameters=parameters)

        if np.all(markerIds is not None):

            frame = cv2.aruco.drawDetectedMarkers(frame, markerCorners, markerIds)

            for i in range(0, len(markerIds)):
                rvec, tvec, _objPoints = cv2.aruco.estimatePoseSingleMarkers(markerCorners[i], 15, intrinsic ,distortion)
                (rvec-tvec).any() #我也不知道為什麼要有這個

                #到起點
                if(markerIds[i] == 2):
                    if trackingFlag ==0 :
                        print ("set！！！")
                        label = "x: "+ str(round(tvec[0][0][0],2))+" y: "+ str(round(tvec[0][0][1],2))+ " z: "+ str(round(tvec[0][0][2],2))
                        frame = cv2.aruco.drawAxis(frame, intrinsic, distortion, rvec, tvec, 6)
                        cv2.putText(frame,label,(360,640),cv2.FONT_HERSHEY_SIMPLEX ,1,(255,255,255),2)

                        zDistance = round((40 - tvec[0][0][2])/100,2)
                        yDistance = round(tvec[0][0][1]/100,2)
                        xDistance = round(tvec[0][0][0]/100,2)
                        zAngle = round(rvec[0][0][2]*180/3.1415927,2)


                        if (yDistance < 0) :
                            print(">> send cmd: up ",-yDistance*100)
                        elif(yDistance > 0):
                            print(">> send cmd: down ",yDistance*100)

                        if (xDistance < 0) :
                            print(">> send cmd: left ",-xDistance*100)
                        elif(xDistance > 0):
                            print(">> send cmd: right ",xDistance*100)

                        if (zAngle>0):
                            print(">> send cmd: cw ",zAngle*0.9)
                        elif(zAngle < 0):
                            print(">> send cmd: ccw ",-zAngle*0.9)

                        if (zDistance < -0.1) :
                            print(">> send cmd: forward ",-zDistance*0.6*100)
                        elif(zDistance > 0.1) :
                            print(">> send cmd: backward ",zDistance*0.6*100)

                        if (abs(zAngle)<30 and abs(zDistance)<0.35 and abs(xDistance)<0.15 and abs (yDistance)<0.15):
                            print("check!")
                            if trackingFlag ==0 :
                                print(">> send cmd: right ",40)
                                time.sleep(4)
                                trackingFlag =1

                            '''if trackingFlag ==2:
                                time.sleep(2)
                                print("end!")
                                print(">> send cmd: land")'''
        if(trackingFlag == 1):
            first = 0
            second = 0
            third = 0
            forth = 0

            for i in range(360):
                for j in range(540):
                    if dilation[i][j] == 255:
                        second+=1
            for i in range(360):
                for j in range(541,1079):
                    if dilation[i][j] == 255:
                        first+=1
            for i in range(361,719):
                for j in range(540):
                    if dilation[i][j] == 255:
                        third +=1
            for i in range(361,719):
                for j in range(541,1079):
                    if dilation[i][j] == 255:
                        forth +=1

            '''if movFlag == 0 : #水平向右飛行
                if (first + forth)> threshold :
                    if(first>forth):
                        print(">> send cmd: up 30")
                        movFlag = 1
                        time.sleep(2)
                    else:
                        print(">> send cmd: down 30")
                        movFlag = 3
                        time.sleep(2)
                else:
                    print(">> send cmd: right 30")
                    time.sleep(2)

            elif movFlag == 1 : #垂直向上飛行
                if (first + second)> threshold :
                    if(first>second):
                        print(">> send cmd: right 30")
                        movFlag = 0
                        time.sleep(2)
                    else:
                        print(">> send cmd: left 30")
                        movFlag = 2
                        time.sleep(2)
                else:
                    print(">> send cmd: up 30")
                    time.sleep(2)

            elif movFlag == 2 : #水平向左飛行
                if (third + second)> threshold :
                    if(second>third):
                        print(">> send cmd: up 30")
                        movFlag = 1
                        time.sleep(2)
                    else:
                        print(">> send cmd: down 30")
                        trackingFlag =1
                        movFlag = 3
                        time.sleep(2)
                else:
                    print(">> send cmd: left 30")
                    time.sleep(2)
            
            elif movFlag == 3 : #垂直向下飛行
                if (third+forth)> threshold :
                    if(forth>third):
                        print(">> send cmd: right 30")
                        movFlag = 0
                        time.sleep(2)
                    else:
                        print(">> send cmd: left 30")
                        movFlag = 2
                        time.sleep(2)
                else:
                    print(">> send cmd: down 30")
                    time.sleep(2)'''
            print(first, second, third, forth)
        cv2.imshow("drone", dilation)
        key = cv2.waitKey(1)
            
        time.sleep(2)
        #if key!= -1: 
            #drone.keyboard(key)
            
if __name__ == "__main__": 
    main()
