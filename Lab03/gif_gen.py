import cv2
import imageio
 
cap = cv2.VideoCapture('output.mp4')
image_lst = []
 
while cap.isOpened():
    ret, frame = cap.read()
    if ret == True:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image_lst.append(frame_rgb)
        
        # cv2.imshow('a', frame)
        key = cv2.waitKey(30)
        if key == ord('q'):
            break
        
cap.release()
cv2.destroyAllWindows()
 
# Convert to gif using the imageio.mimsave method
imageio.mimsave('output.gif', image_lst, fps=20)