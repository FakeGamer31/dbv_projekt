import numpy as np
import matplotlib.pyplot as plt
import cv2

bgr_color = np.uint8([[[255,255,0 ]]])
hsv_color = cv2.cvtColor(bgr_color,cv2.COLOR_BGR2HSV)
print(hsv_color)

bgr_color2 = np.uint8([[[255,0,80 ]]])
hsv_color2 = cv2.cvtColor(bgr_color2,cv2.COLOR_BGR2HSV)
print(hsv_color2)


print(cv2.cvtColor(hsv_color, cv2.COLOR_HSV2BGR))

