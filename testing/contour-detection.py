import cv2 
import numpy as np

img = cv2.imread("/home/pi/crystal-imaging/testing/nacl3.jpg", cv2.IMREAD_GRAYSCALE)

img_h, img_w = img.shape[:2]


_, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)

contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

output = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

if hierarchy is not None:
	hierarchy = hierarchy[0]
    
	for i, cnt in enumerate(contours):
		x, y, w, h = cv2.boundingRect(cnt)
		if w >= img_w - 2 and h >= img_h - 2:
			continue

		child_idx = hierarchy[i][2]   
		parent_idx = hierarchy[i][3]  

		is_outer = False
		if parent_idx == -1:
			is_outer = True
		else:
			px, py, pw, ph = cv2.boundingRect(contours[parent_idx])
			if pw >= img_w - 2 and ph >= img_h - 2:
				is_outer = True

		if is_outer:
            # A stroke-based closed shape will enclose a hole (has a child)
			is_closed = child_idx >= 0
			if is_closed:
				color = (0, 255, 0)
				label = "Closed"
				cv2.drawContours(output, contours, i, color, 2)
				cv2.putText(output, label, (x, max(y - 5, 15)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
				output = cv2.inRange(output,(0,250,0), color)
cv2.imshow('contours', output)
cv2.waitKey(0)
