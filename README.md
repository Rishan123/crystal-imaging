# crystal-imaging

Using computer vision and OpenCV and a simple handheld microscope in order to photograph paracetamol crystals
Using these technologies I am to find out crystal dimensions, sizes and other metrics which may be useful in pharmaceuticals 

test_paracetamol.py - tries to find the contours of the crystals and uses hierarchies to find the 'closed' contours, basically the crystal contours and also takes into account whether the crystals contain holes or not
test_paracetamol2.py - an attempt to detect the contours of the real crystals but fails due to detecting the entire image as a contour, and also fails to correctly determine the crystals
test_paracetamol3.py - uses a binary mask to identify the crystals and does so somewhat successfully
calibrate_ruler.py - used AI to generate this program - connect two points on the calibration scale and the program will calculate the number of pixels between that specific distance - the program outputs a json file which includes the scale factor
