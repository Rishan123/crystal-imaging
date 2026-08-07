import cv2
import numpy as np

img = cv2.imread("/home/pi/crystal-imaging/testing/nacl3.jpg")
bw = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(img, 100,200)
cv2.imshow('edges',edges)
cv2.waitKey(0)
