# image-proc-gauge-reader
OpenCV based gauge reader
### About the Project

x is the image/gauge number
* gauge-x-calibration.jpg is the image overlayed with detected circle boundary and angles marked in it
* gauge-x-lines.jpg is the image overlayed with detected line segment of the needle
* gauge-x-tempdst.jpg is the image with different values of threshold, i.e if pixel value more than something, it will be white and if less than that, then black. Easier for line detection and circle detection to be working

gauge-reader-online.py is the starting program: It connects to the Firebase database and downloads
the image,takes the gauge number and call all other relevant functions

cv_reader.py is the program containing the computer vision based analog gauge detection
and pulls in calibration data from gauge-details.csv through gauge_calibration.py

imageMod.py is an extra program provided in case we may need to do modifications the image for better
detection by cv_reader.py

