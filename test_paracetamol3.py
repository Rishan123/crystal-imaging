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
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	lower_gray = 0   
	upper_gray = 140  
	mask = cv2.inRange(gray, lower_gray, upper_gray)

	# cleans up image and crops the outer boundary due to issues with detecting the entire image as a single contour
	kernel = np.ones((5, 5), np.uint8)
	mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

	margin = 15
	mask[:margin, :] = 0
	mask[-margin:, :] = 0
	mask[:, :margin] = 0
	mask[:, -margin:] = 0

	contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	output_img = img.copy()
	img_h, img_w = img.shape[:2]
	total_area = img_w * img_h

	for i, cnt in enumerate(contours):
		area = cv2.contourArea(cnt)
		

		if 200 < area < (0.70 * total_area):
			rect = cv2.minAreaRect(cnt)
			box = np.intp(cv2.boxPoints(rect))
			
			(x, y), (w, h), angle = rect
			length = max(w, h)
			width = min(w, h)
			
			cv2.drawContours(output_img, [cnt], -1, (0, 255, 0), 2)
			cv2.drawContours(output_img, [box], 0, (0, 0, 255), 2)
			
			label = f"{int(length)}x{int(width)}px"
			cv2.putText(output_img, label, (int(x) - 40, int(y)),
						cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

	cv2.imshow('Binary Mask', mask)
	cv2.imshow('Measured crystals', output_img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
