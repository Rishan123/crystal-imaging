import cv2 
import numpy as np

img = cv2.imread("/home/pi/summer-project/nacl1.jpg")
bw_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(bw_img, 240, 255, cv2.THRESH_BINARY_INV)
contours, hierarchy= cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
cv2.drawContours(image=img, contours=contours, contourIdx=-1, color=(0,255,0), thickness=2, lineType=cv2.LINE_AA)
cv2.imshow('contours', img)
cv2.waitKey(0)