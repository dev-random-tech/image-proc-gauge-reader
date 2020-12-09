import cv2
import numpy as np

def drawCircles(img,x,y,r):
    img2 = img.copy()
    cv2.circle(img2, (x, y), r, (0, 0, 255), 3, cv2.LINE_AA) 
    cv2.circle(img2, (x, y), 2, (0, 255, 0), 3, cv2.LINE_AA)

    cv2.imwrite('./images/circle-detected.jpg', img)
def calbrationCircle(img,x,y,r):
    img2 = img.copy()

    separation = 10.0 
    interval = int(360 / separation)
    p1 = np.zeros((interval,2))  
    p2 = np.zeros((interval,2))
    p_text = np.zeros((interval,2))
    for i in range(0,interval):
        for j in range(0,2):
            if (j%2==0):
                p1[i][j] = x + 0.9 * r * np.cos(separation * i * 3.14 / 180) 
            else:
                p1[i][j] = y + 0.9 * r * np.sin(separation * i * 3.14 / 180)
    text_offset_x = 10
    text_offset_y = 5
    for i in range(0, interval):
        for j in range(0, 2):
            if (j % 2 == 0):
                p2[i][j] = x + r * np.cos(separation * i * 3.14 / 180)
                p_text[i][j] = x - text_offset_x + 1.2 * r * np.cos((separation) * (i+9) * 3.14 / 180) 
            else:
                p2[i][j] = y + r * np.sin(separation * i * 3.14 / 180)
                p_text[i][j] = y + text_offset_y + 1.2* r * np.sin((separation) * (i+9) * 3.14 / 180) 

    for i in range(0,interval):
        cv2.line(img, (int(p1[i][0]), int(p1[i][1])), (int(p2[i][0]), int(p2[i][1])),(0, 255, 0), 2)
        cv2.putText(img, '%s' %(int(i*separation)), (int(p_text[i][0]), int(p_text[i][1])), cv2.FONT_HERSHEY_SIMPLEX, 0.3,(0,0,0),1,cv2.LINE_AA)
    
    cv2.imwrite('./gauge-%s-calibration.%s' % (gauge_number, file_type), img2)

def drawLines(img,lines):
    img2 = img.copy()
    for x1,y1,x2,y2 in lines[i]:
        cv2.line(img2, (x1, y1), (x2, y2), (0, 255, 0), 2)
    
    cv2.imwrite('./gauge-%s-lines-2.%s' % (gauge_number, file_type), img2)


