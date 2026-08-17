import cv2 
import numpy as np
import os
import json


path = "/home/pi/crystal-imaging/paracetamol_imgs"
directory = os.fsencode(path)
calibration_config = "/home/pi/crystal-imaging/calibration_config.json"
output_json = '/home/pi/crystal-imaging/crystal_output.json'
measurements_data = []
crystal_id = 1

with open(calibration_config) as calibration_config_data:
	data = json.load(calibration_config_data)
	scale_factor = data["units_per_pixel"]


for folder in os.listdir(path):
	for file in os.listdir(path+'/'+folder):
		#print(file)
		filepath = path+"/"+folder+"/"+os.fsdecode(file)
		print(filepath)
		img = cv2.imread(filepath)
		img = cv2.resize(img, (500,400))
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		lower_gray = 0   
		upper_gray = 140  
		mask = cv2.inRange(gray, lower_gray, upper_gray)

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
			area_px = cv2.contourArea(cnt)
			

			if 200 < area_px < (0.70 * total_area):
				rect = cv2.minAreaRect(cnt)
				box = np.intp(cv2.boxPoints(rect))
				
				(x, y), (w, h), angle = rect
				length_px = max(w, h)
				width_px = min(w, h)
				
				# measurements#
				length_real = length_px * scale_factor
				width_real = width_px * scale_factor
				area_real = area_px * (scale_factor**2)
				aspect_ratio = length_px / width_px
				perimeter_px = cv2.arcLength(cnt, True)
				perimeter_real = perimeter_px * scale_factor

				hull = cv2.convexHull(cnt)
				hull_area_px = cv2.contourArea(hull)

				if perimeter_px > 0:
					circularity = (4 * np.pi * area_px) / (perimeter_px ** 2)
				else:
					circularity = 0
				
				if hull_area_px > 0:
					solidity = area_px / hull_area_px
				else:
					solidity = 0
				if (length_px * width_px) > 0:
					extent = area_px / (length_px * width_px)
				else:
					extent = 0
				d_eq_real = np.sqrt((4 * area_real) / np.pi)
				
				record = {
					"particle_id": crystal_id,
					"filename": filepath,
					"length_mm": length_real,
					"width_mm": width_real,
					"d_eq": d_eq_real,
					"perimeter_mm": perimeter_real,
					"aspect_ratio": aspect_ratio,
					"circularity": circularity,
					"solidity": solidity,
					"extent": extent
				}
				measurements_data.append(record)
				cv2.drawContours(output_img, [cnt], -1, (0, 255, 0), 2)
				cv2.drawContours(output_img, [box], 0, (0, 0, 255), 2)
				
				label = f"{int(length_px)}x{int(width_px)}px"
				cv2.putText(output_img, label, (int(x) - 40, int(y)),
							cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
				crystal_id += 1
		if measurements_data:
			with open(output_json, "w") as f:
				json.dump(measurements_data, f, indent=4)
print(f"Exported {len(measurements_data)} records to '{output_json}'.")
			
		#cv2.imshow('Binary Mask', mask)
		#cv2.imshow('Measured', output_img)
		#cv2.waitKey(0)
		#cv2.destroyAllWindows()
