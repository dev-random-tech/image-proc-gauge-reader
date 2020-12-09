import cv2
import numpy as np


def boxDrawing(img,start_point,end_point):
	color = (0,0,255) # BGR
	thickness = 3 #px
	new_img = cv2.rectangle(img,start_point,end_point,color,thickness)
	
	return new_img

def resizing(img,width,height):
	new_size = (width,height)
	new_img = cv2.resize(img,new_size,interpolation = cv2.INTER_AREA)

	return new_img

def cropping(img,topLeft_x,topLeft_y,width,height):
	crop_img = img[topLeft_y:topLeft_y+height,topLeft_x:topLeft_x+width]
	
	return crop_img
	