import cv2
import numpy as np
import json

# Global storage for clicked points
points = []

def mouse_callback(event, x, y, flags, param):
    global points
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(points) < 2:
            points.append((x, y))
            print(f"Point {len(points)} selected: ({x}, {y})")

# 1. Load calibration slide image
image_path = '/home/pi/crystal-imaging/ruler_imgs/PHO00029.JPG'  
img = cv2.imread(image_path)
img = cv2.resize(img, (500,400))
if img is None:
    raise FileNotFoundError(f"Could not load image file: {image_path}")

clone = img.copy()

cv2.namedWindow("Calibration Tool")
cv2.setMouseCallback("Calibration Tool", mouse_callback)

print("--- MICROMETER CALIBRATION TOOL ---")
print("1. Left-click two known tick marks on the scale (e.g. 1 mm or 100 um apart).")
print("2. Press 'c' to confirm/calculate, or 'r' to reset points.")

while True:
    display = clone.copy()
    
    # Draw selected points and connecting line
    for pt in points:
        cv2.circle(display, pt, 2, (0, 0, 255), -1)
    if len(points) == 2:
        cv2.line(display, points[0], points[1], (0, 255, 0), 1)
        
    cv2.imshow("Calibration Tool", display)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("r"):
        points = []
        print("Points reset.")
    elif key == ord("c"):
        if len(points) == 2:
            break
        else:
            print("Please click exactly 2 points before pressing 'c'.")

cv2.destroyAllWindows()

# 2. Calculate pixel distance (Euclidean distance formula)
p1, p2 = points
pixel_distance = np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
print(f"\nMeasured Distance: {pixel_distance:.2f} pixels")

# 3. Prompt user for true scale values
real_distance = float(input("Enter true distance between points (e.g., 1.0 for 1mm, 100 for 100um): "))
unit_name = input("Enter physical unit (e.g., mm, um): ").strip()

# 4. Calculate conversions
pixels_per_unit = pixel_distance / real_distance
units_per_pixel = real_distance / pixel_distance

print("\n--- RESULTS ---")
print(f"Scale Factor: {pixels_per_unit:.4f} pixels/{unit_name}")
print(f"Resolution:   {units_per_pixel:.6f} {unit_name}/pixel")

# 5. Save calibration config for use in other scripts
config = {
    "pixels_per_unit": pixels_per_unit,
    "units_per_pixel": units_per_pixel,
    "unit": unit_name
}

with open("calibration_config.json", "w") as f:
    json.dump(config, f, indent=4)

print("Saved calibration factor to 'calibration_config.json'.")
