import cv2
import numpy as np
import dlib

def main():
    #calibration data
    cv_file = cv2.FileStorage("data.xml", cv2.FILE_STORAGE_READ)
    intrinsic = cv_file.getNode("intrinsic").mat()
    distortion = cv_file.getNode("distortion").mat()
    cv_file.release()
    
    cap = cv2.VideoCapture(0)

    # initialize the HOG descriptor/person detector
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    #initialize the dlib face dctector
    detector = dlib.get_frontal_face_detector()


    while(True):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #body
        rects, weights = hog.detectMultiScale(gray,winStride=(8,8), scale=1.2, useMeanshiftGrouping = False)
        i = -1
        for (x, y, w, h) in rects:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
            objPoints = np.array([[(0,0,0),(80,0,0),(80,180,0),(0,180,0)]],dtype=np.float)
            imgPoints = np.array([[(x,y), (x + w,y),(x + w, y + h),(x,y+h)]],dtype=np.float)
            retval,rvec,tvec = cv2.solvePnP(objPoints,imgPoints,intrinsic,distortion)
            label =" bz: "+ str(round(tvec[2][0],2))
            i+=1
            cv2.putText(frame,label,(360+i*200,480),cv2.FONT_HERSHEY_SIMPLEX ,1,(0,255,255),2)
            
        #face decteciton
        face_rects = detector(gray, 0)
        for i, d in enumerate(face_rects):
            x1 = d.left()
            y1 = d.top()
            x2 = d.right()
            y2 = d.bottom()

            cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)
            objPoints = np.array([[(0,0,0),(14,0,0),(14,14,0),(0,14,0)]],dtype=np.float)
            imgPoints = np.array([[(x1,y1), (x2,y1),(x2,y2),(x1,y2)]],dtype=np.float)
            retval,rvec,tvec = cv2.solvePnP(objPoints,imgPoints,intrinsic,distortion)
            label =" fz: "+ str(round(tvec[2][0],2))
            cv2.putText(frame,label,(360+i*200,640),cv2.FONT_HERSHEY_SIMPLEX ,1,(0,255,0),2)
            
        cv2.imshow("Dectect",frame)

        if (cv2.waitKey(33)&0xFF == ord('q')):
            break
    cap.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)  

if __name__ == "__main__":
    main()
  