import cv2

cv_file = cv2.FileStorage("data.xml", cv2.FILE_STORAGE_READ)

matrix = cv_file.getNode("distortion").mat()
print(matrix)
cv_file.release()
