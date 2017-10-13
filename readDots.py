#!/usr/bin/env python 
#Based on http://answers.opencv.org/question/58775/detect-fiducial-of-dots/
import cv2
import time
start = time.time()
import math
def sqdist( p1, p2):
    return abs(p1[0]-p2[0])**2 + abs(p1[1]-p2[1])**2
    
MAXSQUAREAREA = 7000
MINSQUAREAREA = 1
im_col = cv2.imread('2017-10-12-193434.jpg',cv2.IMREAD_COLOR)

#https://docs.opencv.org/trunk/d7/d4d/tutorial_py_thresholding.html
im = cv2.cvtColor(im_col,cv2.COLOR_BGR2GRAY)

(threshold,bw) = cv2.threshold(im,190,255,cv2.THRESH_BINARY)
#(threshold,bw) = cv2.threshold(im,200,255,cv2.THRESH_OTSU)

#Take a look at that b/w:
cv2.namedWindow("res")
cv2.imshow("res",bw)
#cv2.waitKey()

try:
    conts, hier = cv2.findContours(bw,cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
except ValueError:
    #Python3-opencv3
    image, conts, hier = cv2.findContours(bw,cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

cleaned = []
points = []
sizes = []
#Filter by area size:
for c in conts:
    a = cv2.contourArea(c)
    #Explore this..
    #print(eval(raw_input('>')))
    print (a)
    if a <= MAXSQUAREAREA and a >= MINSQUAREAREA:
        cleaned.append(c)

        x,y,w,h = cv2.boundingRect(c)
        #Green show rectangle:
        cv2.rectangle(im_col,(x,y),(x+w,y+h),(0,255,0),2)
        points.append( (x+w/2.0, y+w/2.0) )
        sizes.append( w )

print( points )
for (i, pt) in enumerate(points):
    print (pt, i)
    nearby = 0
    w = sizes[i]
    for p2 in points:
        if sqdist(pt, p2) < 2.8*w*2.8*w:
            nearby+= 1
    print( pt, w )
    print( 'has %s neighbors' % (nearby,))
    if nearby > 6:
        #print((int(i) for i in pt))
        #RED points 0,0,255
        cv2.circle( im_col, tuple(int(i) for i in pt) , 2, (0,0,255),2 )
        
        cv2.imshow("res", im_col)
        #cv2.waitKey()
print( 'that took %f' % (time.time() - start) )
#cv2.drawContours(im_col,cleaned,-1,(0,0,0), 3)

cv2.imshow("res", im_col)
cv2.waitKey()
