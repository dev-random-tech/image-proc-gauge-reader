import cv2
import numpy as np
import time
import imageMod as imgMod
import gauge_calibration as gc

#Out of all circles that are found out, taking the average best approximated the
#actual dial 
def avg_circles(circles, b):
    avg_x=0
    avg_y=0
    avg_r=0
    for i in range(b):
        avg_x = avg_x + circles[0][i][0]
        avg_y = avg_y + circles[0][i][1]
        avg_r = avg_r + circles[0][i][2]
    avg_x = int(avg_x/(b))
    avg_y = int(avg_y/(b))
    avg_r = int(avg_r/(b))
    return avg_x, avg_y, avg_r

#finding the distance between two sets of points
def dist_2_pts(x1, y1, x2, y2):
    #print np.sqrt((x2-x1)^2+(y2-y1)^2)
    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

#To detect the circle and calibrate t
def calibrate_gauge(img,gauge_number,file_type):

    #img = cv2.imread('./images/gauge-%s.%s' %(gauge_number, file_type),1)
    img2 = img.copy()
    height,width  = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  
    #gray = cv2.GaussianBlur(gray, (5, 5), 0)
    #gray = cv2.medianBlur(gray, 5)


    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, np.array([]), 100, 50, int(width*0.10), int(width*0.95))
    print(circles)
    
    a, b, c = circles.shape
    x,y,r = avg_circles(circles, b)

    cv2.circle(img2, (x, y), r, (0, 0, 255), 3, cv2.LINE_AA) 
    cv2.circle(img2, (x, y), 2, (0, 255, 0), 3, cv2.LINE_AA)

    cv2.imwrite('./gauge-%s-circles.%s' % (gauge_number, file_type), img2)
    
    '''
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
    
    cv2.imwrite('./gauge-%s-calibration.%s' % (gauge_number, file_type), img)
    '''
    return x, y, r	

#to find the relevant lines, it's angle and give it's output
#on the basis of calibration parameters
def get_current_value(img, min_angle, max_angle, min_value, max_value, x, y, r, gauge_number, file_type):

    #img = cv2.imread('gauge-%s.%s' % (gauge_number, file_type))
    img2 = img.copy()
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    thresh = 175
    maxValue = 255

    th, dst2 = cv2.threshold(gray2, thresh, maxValue, cv2.THRESH_BINARY_INV)

    #dst2 = cv2.medianBlur(dst2, 5)
    #dst2 = cv2.Canny(dst2, 50, 150)
    #dst2 = cv2.GaussianBlur(dst2, (5, 5), 0)

    #cv2.imwrite('./images/gauge-%s-tempdst2.%s' % (gauge_number, file_type), dst2)

    minLineLength = 70
    maxLineGap = 0
    lines = cv2.HoughLinesP(image=dst2, rho=3, theta=np.pi / 180, threshold=100,minLineLength=minLineLength, maxLineGap=0) 

    print(len(lines))
    final_line_list = []

    diff1LowerBound = 0.15 
    diff1UpperBound = 0.25
    diff2LowerBound = 0.5 
    diff2UpperBound = 1.0
    for i in range(0, len(lines)):
        for x1, y1, x2, y2 in lines[i]:
            diff1 = dist_2_pts(x, y, x1, y1)  
            diff2 = dist_2_pts(x, y, x2, y2)  
            cv2.line(img2, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            if (diff1 > diff2):
                temp = diff1
                diff1 = diff2
                diff2 = temp
            
            if (((diff1<diff1UpperBound*r) and (diff1>diff1LowerBound*r) and (diff2<diff2UpperBound*r)) and (diff2>diff2LowerBound*r)):
                line_length = dist_2_pts(x1, y1, x2, y2)
                print(line_length)
                final_line_list.append([x1, y1, x2, y2])
    cv2.imwrite('./gauge-%s-lines-2.%s' % (gauge_number, file_type), img2)
    
    # for i in range(0,len(final_line_list)):
    #     x1 = final_line_list[i][0]
    #     y1 = final_line_list[i][1]
    #     x2 = final_line_list[i][2]
    #     y2 = final_line_list[i][3]
    #     cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    x1 = final_line_list[0][0]
    y1 = final_line_list[0][1]
    x2 = final_line_list[0][2]
    y2 = final_line_list[0][3]

    #x1,y1,x2,y2 = (46,148,103,141)


    dist_pt_0 = dist_2_pts(x, y, x1, y1)
    dist_pt_1 = dist_2_pts(x, y, x2, y2)
    if (dist_pt_0 > dist_pt_1):
        x_angle = x1 - x
        y_angle = y - y1
    else:
        x_angle = x2 - x
        y_angle = y - y2
    
    res = np.arctan(np.divide(float(y_angle), float(x_angle)))
    #np.rad2deg(res) #coverts to degrees

    res = np.rad2deg(res)
    if x_angle > 0 and y_angle > 0:  #in quadrant I
        final_angle = 270 - res
    if x_angle < 0 and y_angle > 0:  #in quadrant II
        final_angle = 90 - res
    if x_angle < 0 and y_angle < 0:  #in quadrant III
        final_angle = 90 - res
    if x_angle > 0 and y_angle < 0:  #in quadrant IV
        final_angle = 270 - res

    old_min = float(min_angle)
    old_max = float(max_angle)

    new_min = float(min_value)
    new_max = float(max_value)

    old_value = final_angle

    old_range = (old_max - old_min)
    new_range = (new_max - new_min)
    new_value = (((old_value - old_min) * new_range) / old_range) + new_min

    return new_value

def cv(gauge_number,img_path,calibration_path,file_type):
    
    img = cv2.imread(img_path,1)
    #imgCopy = img.copy()
    print(img.shape)
    print('gauge number: 00%s' %gauge_number)
    min_angle, max_angle, min_value, max_value, units = gc.gauge_calibration(calibration_path,gauge_number) 
    #min_angle, max_angle, min_value, max_value, units = (40,320,0,200,'psi')
    x, y, r = calibrate_gauge(img,gauge_number, file_type) 
    print(x,y,r)

    #assert not isinstance(image,type(None)), 'image not found'
    val = get_current_value(img, min_angle, max_angle, min_value, max_value, x, y, r, gauge_number, file_type)
    return val,units

'''
def main():
    calibration_path = '/media/dev/Data1/transfer/IITDFSM/IITDTrialCodes/gauge-reading/gauge-details.csv'
    download_path = '/media/dev/Data1/transfer/IITDFSM/IITDTrialCodes/gauge-reading/images/gauge-1.jpg'
    fileType = download_path[-3:]
    gauge_index = 1
    val,unit = cv(gauge_index,download_path,calibration_path,fileType)
    print('Reading of the gauge: ',val,' ',unit)

if __name__=='__main__':
    main()
'''