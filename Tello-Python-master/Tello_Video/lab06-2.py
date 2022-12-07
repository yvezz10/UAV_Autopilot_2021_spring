import cv2
import numpy as np
import tello
import time

crossFlag = 0
def main():
    drone = tello.Tello('', 8889)
    
    
    dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
    parameters = cv2.aruco.DetectorParameters_create()
    
    cv_file = cv2.FileStorage("data.xml", cv2.FILE_STORAGE_READ)
    intrinsic = cv_file.getNode("intrinsic").mat()
    distortion = cv_file.getNode("distortion").mat()
    cv_file.release()
    time.sleep(10)

    drone.takeoff()
    print("ok!")

    while(True):
        frame = drone.read()
        if np.all(frame is not None):
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        markerCorners, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(frame, dictionary, parameters=parameters)
        
        if np.all(markerIds is not None):

            frame = cv2.aruco.drawDetectedMarkers(frame, markerCorners, markerIds)

            for i in range(0, len(markerIds)):
                rvec, tvec, _objPoints = cv2.aruco.estimatePoseSingleMarkers(markerCorners[i], 15, intrinsic ,distortion)
                (rvec-tvec).any() #我也不知道為什麼要有這個

                #帶無人機跑
                if(markerIds[i] == 2):
                    label = "x: "+ str(round(tvec[0][0][0],2))+" y: "+ str(round(tvec[0][0][1],2))+ " z: "+ str(round(tvec[0][0][2],2))
                    frame = cv2.aruco.drawAxis(frame, intrinsic, distortion, rvec, tvec, 6)
                    cv2.putText(frame,label,(360,640),cv2.FONT_HERSHEY_SIMPLEX ,1,(255,255,255),2)

                    zDistance = round((90 - tvec[0][0][2])/100,3)
                    yDistance = round(tvec[0][0][1]/100,3)
                    xDistance = round(tvec[0][0][0]/100,3)
                    zAngle = round(rvec[0][0][2]*180/3.1415927,3)

                    if (zAngle>10):
                        drone.rotate_cw(zAngle)
                    elif(zAngle < -10):
                        drone.rotate_ccw(-zAngle)

                    if (yDistance < 0) :
                        drone.move_up (-yDistance)
                    elif(yDistance > 0):
                        drone.move_down(yDistance)

                    if (xDistance < 0) :
                        drone.move_left(-xDistance)
                    elif(xDistance > 0):
                        drone.move_right(xDistance)


                    if (zDistance < -0.1) :
                        drone.move_forward(-zDistance*0.6)
                    elif(zDistance > 0.1) :
                        drone.move_backward(zDistance*0.6)

                #越過山丘
                elif(markerIds[i] == 4):
                    print ("start rolling")
                    label = "x: "+ str(round(tvec[0][0][0],2))+" y: "+ str(round(tvec[0][0][1],2))+ " z: "+ str(round(tvec[0][0][2],2))
                    frame = cv2.aruco.drawAxis(frame, intrinsic, distortion, rvec, tvec, 6)
                    cv2.putText(frame,label,(360,640),cv2.FONT_HERSHEY_SIMPLEX ,1,(255,255,255),2)

                    zDistance = round((100 - tvec[0][0][2])/100,3)
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

                    if (abs(zAngle)<30 and abs(zDistance)<0.2 and abs(xDistance)<0.15 and abs (yDistance)<0.15):
                        print("check!")
                        time.sleep(2)
                        drone.move_forward(0.5)
                        time.sleep(2)
                        drone.move_up(0.8)
                        time.sleep(4)
                        drone.move_forward(1.5)
                        time.sleep(4)
                        drone.move_down(0.8)

                #穿過我的巴巴
                elif(markerIds[i] == 3):
                    print ("start throughing")
                    label = "x: "+ str(round(tvec[0][0][0],2))+" y: "+ str(round(tvec[0][0][1],2))+ " z: "+ str(round(tvec[0][0][2],2))
                    frame = cv2.aruco.drawAxis(frame, intrinsic, distortion, rvec, tvec, 6)
                    cv2.putText(frame,label,(360,640),cv2.FONT_HERSHEY_SIMPLEX ,1,(255,255,255),2)

                    zDistance = round((90 - tvec[0][0][2])/100,3)
                    yDistance = round(tvec[0][0][1]/100,3)
                    xDistance = round(tvec[0][0][0]/100,3)
                    zAngle = 0 #round(rvec[0][0][2]*180/3.1415927,3)


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

                    if (abs(zDistance)<0.2 and abs(xDistance)<0.15 and abs (yDistance)<0.15):
                        print("check!")
                        time.sleep(2)
                        drone.move_forward(0.5)
                        time.sleep(3)
                        drone.move_down(0.7)
                        time.sleep(3)
                        currentH = drone.get_height()
                        while(currentH > 0.5):
                            drone.move_down(0.1)
                            time.sleep(1)
                            currentH = drone.get_height()
                        drone.move_forward(1.5)
                        time.sleep(4)
                        drone.move_up(1)


                #降落
                elif(markerIds[i] == 5 ):
                    print ("start landing")
                    label = "x: "+ str(round(tvec[0][0][0],2))+" y: "+ str(round(tvec[0][0][1],2))+ " z: "+ str(round(tvec[0][0][2],2))
                    frame = cv2.aruco.drawAxis(frame, intrinsic, distortion, rvec, tvec, 6)
                    cv2.putText(frame,label,(360,640),cv2.FONT_HERSHEY_SIMPLEX ,1,(255,255,255),2)

                    zDistance = round((80 - tvec[0][0][2])/100,3)
                    yDistance = round(tvec[0][0][1]/100,3)
                    xDistance = round(tvec[0][0][0]/100,3)
                    zAngle = round(rvec[0][0][2]*180/3.1415927,3)

                    if (zAngle>0 and zAngle<20):
                        drone.rotate_cw(zAngle)
                    elif(zAngle>=20):
                        drone.rotate_cw(zAngle*0.5)
                        time.sleep(1)
                        drone.move_left(0.2)

                    elif(zAngle < 0 and zAngle> -20):
                        drone.rotate_ccw(-zAngle)

                    elif(zAngle<=-20):
                        drone.rotate_ccw(-zAngle*0.5)
                        time.sleep(1)
                        drone.move_right(0.2)

                    if (yDistance < 0) :
                        drone.move_up (-yDistance)
                    elif(yDistance > 0):
                        drone.move_down(yDistance)

                    if (xDistance < 0 and xDistance > -0.3) :
                        drone.move_left(-xDistance)
                    elif(xDistance<= -0.3):
                        drone.move_left(-xDistance*0.6)
                    elif(xDistance > 0 and xDistance<0.3):
                        drone.move_right(xDistance)
                    elif(xDistance>=0.3):
                            drone.move_right(xDistance*0.6)



                    if (zDistance < -0.1) :
                        drone.move_forward(-zDistance*0.5)
                    elif(zDistance > 0.1) :
                        drone.move_backward(zDistance*0.5)

                    while (abs(zDistance)<0.2 and abs(xDistance)<0.15 and abs (yDistance)<0.15 and abs(zAngle)<15):
                        print("check!")
                        time.sleep(2)
                        currentZ = round(tvec[0][0][2]/100,3)
                        while(currentZ > 0.6):
                            drone.move_forward(0.2)
                            time.sleep(1)
                            rvec, tvec, _objPoints = cv2.aruco.estimatePoseSingleMarkers(markerCorners[i], 15, intrinsic ,distortion)
                            (rvec-tvec).any()
                            currentZ = round(tvec[0][0][2]/100,3)
                        drone.land()


        cv2.imshow("drone", frame)
        key = cv2.waitKey(1)
        
        if key!= -1: 
            drone.keyboard(key)
    
    cv2.destroyAllWindows()
            
if __name__ == "__main__": 
    main()


        