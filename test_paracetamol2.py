import cv2 
import numpy as np
import os
path = "/home/pi/crystal-imaging/paracetamol_imgs/1"
directory = os.fsencode(path)
for file in os.listdir(directory):
	filepath = path+"/"+os.fsdecode(file)
	print(filepath)
	img = cv2.imread(filepath)
	img = cv2.resize(img, (500,400))
	img_area = 500*400
	source_img = img.copy()
	grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	_, thresh = cv2.threshold(grey, 180,255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
	
	
	im_floodfill = thresh.copy()
	h, w = thresh.shape[:2]
	mask = np.zeros((h + 2, w + 2), np.uint8)
	cv2.floodFill(im_floodfill, mask, (0, 0), 255)
	im_floodfill_inv = cv2.bitwise_not(im_floodfill)
	filled_binary = thresh | im_floodfill_inv
	
	kernel = np.ones((7, 7), np.uint8)
	cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
	
	margin = 5
	cleaned[:margin, :] = 0
	cleaned[-margin:, :] = 0
	cleaned[:, :margin] = 0
	cleaned[:, -margin:] = 0
	
	
	
	contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	for i,cnt in enumerate(contours):
		if 30 < cv2.contourArea(cnt) <  (0.7*img_area):
			cv2.drawContours(source_img, [cnt], -1, (0,255,0), 2)
			rect = cv2.minAreaRect(cnt)
			box = cv2.boxPoints(rect)
			box = np.intp(box)
			cv2.drawContours(source_img, [box], 0, (0,0,255), 1)
			(x,y), (w,h), angle = rect
			length = max(w,h)
			width = min(w,h)
			if length >=450:
				continue
			else:
				label = f"#{i+1}: {int(length)}px"
				cv2.putText(source_img, label, (int(x)-10, int(y)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(255,0,0), 2)
				print(label)
	cv2.imshow("detected crystals", source_img)
	cv2.waitKey(0)
	
					
