# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 11:47:58 2023

@author: gmart
"""

import cv2
import numpy as np

cap = cv2.VideoCapture(2)


while True:
    ret, frame = cap.read()
    
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    #Template laden
    template = cv2.imread('F:\Hochschule\DBV\dbv_projekt\src\Templates\erster_test_template.jpg', cv2.IMREAD_GRAYSCALE)
    height, width = template.shape
    
    # # all possible methods
    # methods = [cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED, cv2.TM_CCORR, cv2.TM_CCORR_NORMED,
    #             cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]
    
    # # Testign out all methods
    # for method in methods: 
        
    method = cv2.TM_CCOEFF
    
    result = cv2.matchTemplate(img, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    # Two methods are different, so you need to take the min-value
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        location = min_loc
    else:
        location = max_loc
    
    # Drawing the boxes
    bottom_right = (location[0] + width, location[1] + height)
    cv2.rectangle(frame, location, bottom_right, 255, 5)
    
    cv2.imshow("Window", frame)
    
    if cv2.waitKey(1) == ord("q"):
        break
    
cap.release()
cv2.destroyAllWindows()