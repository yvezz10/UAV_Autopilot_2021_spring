import cv2
import numpy as np
import time

def main():
    cap = cv2.VideoCapture(0)

    #parameters
    kernel_size = 5
    trackingFlag = 0
    movFlag = 0 #0水平 1鉛直
    horFlag = 0 #0向右 1向左
    verFlag = 0 #0向上 1向下
    turnCnt = 0
    frameCnt = -1
    
    #calibration data
    dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
    parameters = cv2.aruco.DetectorParameters_create()
    
    cv_file = cv2.FileStorage("data.xml", cv2.FILE_STORAGE_READ)
    intrinsic = cv_file.getNode("intrinsic").mat()
    distortion = cv_file.getNode("distortion").mat()
    cv_file.release()

    print(">> send cmd: takeoff")
    print("ok!")

    #start
    while(True):
        ret, img = cap.read()
        frameCnt+=1

        if frameCnt%30 == 0:             #30幀判斷一次

            frame = img[0:720,0:1080]
            
            #frame convert
            if np.all(frame is not None):
                gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
                blur_gray = cv2.GaussianBlur(gray,(kernel_size, kernel_size), 0)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) #aruco
                edges_frame = cv2.Canny(blur_gray, 70, 200)
                dilation = cv2.dilate(edges_frame, (kernel_size, kernel_size), 2)
                #dilation = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            markerCorners, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(frame, dictionary, parameters=parameters)

            #dectect aruco
            if np.all(markerIds is not None):

                frame = cv2.aruco.drawDetectedMarkers(frame, markerCorners, markerIds)

                for i in range(0, len(markerIds)):
                    rvec, tvec, _objPoints = cv2.aruco.estimatePoseSingleMarkers(markerCorners[i], 15, intrinsic ,distortion)
                    (rvec-tvec).any() #我也不知道為什麼要有這個

                    #到起點
                    if(markerIds[i] == 2):

                        # 定位起點
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

                        #land
                        if trackingFlag ==2:
                            time.sleep(2)
                            print("end!")
                            print(">> send cmd: land")

            if(trackingFlag == 1 or trackingFlag==2):
                state = [0, 0, 0, 0] #up down left right
                pixCnt = 0

                ##scan the frame
                #上邊
                for i in range(1080):
                    if dilation[0][i] == 255 :
                        pixCnt+=1
                if pixCnt>=2:
                    state[0] =1
                    pixCnt = 0

                #下邊
                for i in range(1080):
                    if dilation[719][i] == 255 :
                        pixCnt+=1
                if pixCnt>=2:
                    state[1] =1
                    pixCnt = 0

                #左邊
                for i in range(720):
                    if dilation[i][0] == 255 :
                        pixCnt+=1
                if pixCnt>=2:
                    state[2] =1
                    pixCnt = 0
                
                #右邊
                for i in range(720):
                    if dilation[i][1079] == 255 :
                        pixCnt+=1
                if pixCnt>=2:
                    state[3] =1
                    pixCnt = 0
  
                ##identifiate the state
                if state == [0,0,1,1]: #水平直線
                    if horFlag == 0:
                        print(">> send cmd: right 30")
                    else:
                        print(">> send cmd: left 30")

                elif state == [1,1,0,0]: #垂直直線
                    if verFlag == 0:
                        print(">> send cmd: up 30")
                    else:
                        print(">> send cmd: down 30")

                elif state == [1,0,1,0]: #J彎
                    turnCnt+=1
                    if movFlag ==0 :
                        print(">> send cmd: up 30")
                        verFlag = 0
                        movFlag = 1
                
                elif state == [0,1,0,1]: #ㄏ彎
                    turnCnt+=1
                    if movFlag ==0 and horFlag==1:
                        print(">> send cmd: down 30")
                        verFlag = 1
                        movFlag = 1
                    else :
                        print(">> send cmd: right 30")
                        movFlag = 0
                        horFlag = 0
                
                elif state == [0,1,1,0]: #7彎
                    turnCnt+=1                    
                    if movFlag == 1 :
                        print(">> send cmd: left 30")
                        horFlag = 1
                        movFlag = 0
                
                if turnCnt>=5:
                    trackingFlag = 2


        cv2.imshow("drone", dilation)
        key = cv2.waitKey(1)
            
        #if key!= -1: 
            #drone.keyboard(key)
            
if __name__ == "__main__": 
    main()
