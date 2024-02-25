from matplotlib import pyplot as plt
from model.brick import Brick
from itertools import product

import cv2
import utils
import numpy as np

g = 102
maxx = 255
sig = 2
kernel_morph = (9,9)
kernel_blur = (1,1)

blur_kernel = [(3,3),(5,5,),(7,7,)]
morph_kernel = [(3,3),(5,5),(7,7)]
canny_min = [0, 50, 100, 150, 200, 255]

combinations = list(product(blur_kernel, morph_kernel, canny_min))

def calculate_iou(box1, box2):
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2

    # Koordinaten der Überlappung berechnen
    x_left = max(x1, x2)
    y_top = max(y1, y2)
    x_right = min(x1 + w1, x2 + w2)
    y_bottom = min(y1 + h1, y2 + h2)

    # Überlappungsfläche berechnen
    intersection_area = max(0, x_right - x_left) * max(0, y_bottom - y_top)

    # Gesamtfläche der beiden Bounding-Boxen berechnen
    area1 = w1 * h1
    area2 = w2 * h2
    union_area = area1 + area2 - intersection_area

    # IOU berechnen
    iou = intersection_area / union_area if union_area > 0 else 0

    return iou

def filter_duplicate_coordinates(objekt_liste, iou_threshold=0.8):
    gefilterte_objekte = []

    for i, objekt1 in enumerate(objekt_liste):
        should_add = True

        for j, objekt2 in enumerate(gefilterte_objekte):
            iou = calculate_iou(objekt1.coordinates, objekt2.coordinates)

            if iou > iou_threshold:
                should_add = False
                break

        if should_add:
            gefilterte_objekte.append(objekt1)

    return gefilterte_objekte



def something(x):
    pass

def change_kernel(x):
    global kernel_morph
    if x == 0:
        kernel_morph = (1,1)
    elif x == 1:
        kernel_morph = (3,3)
    elif x == 2:
        kernel_morph = (5,5)
    elif x == 3:
        kernel_morph = (7,7)
    elif x == 4:
        kernel_morph = (9,9)


def change_kernel_blur(x):
    global kernel_blur
    if x == 0:
        kernel_blur = (1,1)
    elif x == 1:
        kernel_blur = (3,3)
    elif x == 2:
        kernel_blur = (5,5)
    elif x == 3:
        kernel_blur = (7,7)
    elif x == 4:
        kernel_blur = (9,9)




# Funktion für die Objekterkennung
def detect_lego_blocks(dst, org_img, blur_kernel,morph_kernel,canny_min):
    global g
    global kernel_morph
    global kernel_blur
    global sig
    global maxx

    brick_list = []

    # Grayscale
    # mask = cv2.inRange(cv2.cvtColor(dst, cv2.COLOR_BGR2HSV), lower, upper)
    mask = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
    cv2.imshow('mask', mask)

    # Blur
    cv2.getTrackbarPos('kernel_blur', 'blurred')
    sig = cv2.getTrackbarPos('blur_sigma', 'blurred')
    # print('sigma ',sig)
    # print('kernel blur  ', kernel_blur)
    blurred_image = cv2.GaussianBlur(mask, blur_kernel,0)
    cv2.imshow('blurred', blurred_image)

    # Morph
    morph2 = cv2.morphologyEx(blurred_image, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT,morph_kernel))
    # erode = cv2.erode(edges, cv2.getStructuringElement(cv2.MORPH_RECT,(1,1)), iterations=100)
    # morph = cv2.dilate(erode, cv2.getStructuringElement(cv2.MORPH_RECT,(1,1)), iterations=1)
    cv2.imshow('morph', morph2)
 

    g = cv2.getTrackbarPos('min', 'edges')
    maxx = cv2.getTrackbarPos('max', 'edges')
    # print('canny thresh  ', g)
    cv2.getTrackbarPos('kernel', 'edges')
    # print('kernel morph  ',kernel_morph)
    # print(kernel_morph)
    # print(g, ' and ',b)
    edges2 = cv2.Canny(morph2, canny_min, canny_min*3)
    cv2.imshow('edges', edges2)

 
    
    testaray= np.array([])
    # Konturfindung
    contours, _ = cv2.findContours(edges2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Objekterkennung und Markierung
    # print('start####################################')
    index_counter = 0
    for contour in contours:
        # print(contour)
        area = cv2.contourArea(contour)
        circumference = cv2.arcLength(contour, True)

        if area > 0:
            compactness =  (circumference**2) / (4 * np.pi * area)
        else:
            compactness = 0
        testaray = np.append(testaray, (area,circumference,compactness))
        # print('area: ', area, '   perimeter: ', circumference, '     compactness: ', compactness )
        # print('')
        # if area > 500 and ((4/np.pi)*0.8) <= compactness <= (((4/np.pi)*1.2)) :  # Beispielgrenze für die Mindestgröße der Kontur
        if 576*0.9 <= area <= 576*1.1:  # Beispielgrenze für die Mindestgröße der Kontur
            # print(f'perimeter: {circumference}')
            x, y, w, h = cv2.boundingRect(contour)
            # cv2.rectangle(frame2, (x, y), (x + w, y + h), (180, 255, 50), 2)
            dominant_color = utils.dominant_color_from_roi(org_image=org_img, contour=contour)
            brick_list.append(Brick(area=area, circumference=circumference, color_code=dominant_color, original_image=org_img, coordinates=(x,y,w,h), contour=contour))
            index_counter += 1
    # print('stop##########################################')
    return brick_list


cv2.namedWindow('edges') 
cv2.namedWindow('blurred') 
cv2.createTrackbar('min','edges',102,255,something)
cv2.createTrackbar('max','edges',255,255,something)
cv2.createTrackbar('kernel','edges',4,4,change_kernel)
cv2.createTrackbar('kernel_blur','blurred',0,4,change_kernel_blur)
cv2.createTrackbar('blur_sigma','blurred',2,15,something)

# Öffnen Sie die Kamera (0 steht für die Standardkamera, kann angepasst werden)
# cap = cv2.VideoCapture('http://192.168.178.36:4747/mjpegfeed')
# cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)


show_list = True
brick_list = []
while True:
    ## Erfassen Sie ein Frame von der Kamera
    # ret, org_img = cap.read()
    # frame_processed = org_img.copy()

    # Überprüfen Sie, ob das Frame korrekt erfasst wurde
    # if not ret:
    #     print('Kein Bild')
    org_img = cv2.imread('../images/newest/legos_down_view.jpg')
    frame, _, _  = utils.automatic_brithness_and_contrast(org_img,1)
    frame = utils.resize_image(frame)
    frame_processed = org_img.copy()

    # Objekterkennung auf dem aktuellen Frame durchführen
    if show_list:
        for (blur_kernel,morph_kernel,canny_min) in combinations:
            brick_list = brick_list + detect_lego_blocks(frame, frame_processed, blur_kernel,morph_kernel,canny_min)
    
    brick_list = filter_duplicate_coordinates(brick_list)
    for brick in brick_list:
        contour = brick.contour
        x, y, w, h = cv2.boundingRect(contour)
        box = np.intp(cv2.boxPoints(cv2.minAreaRect(contour)))
        cv2.drawContours(frame_processed, [box], 0, (0,255,0), 1)
        cv2.putText(frame_processed,f'{brick.color_str}' , (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255,255,255), 0, cv2.LINE_AA)

    # Zeigen Sie das Original- und das bearbeitete Frame an
    cv2.imshow('Original', org_img)
    cv2.imshow('Auto contrast and brithness', frame)
    cv2.imshow('Processed', frame_processed)
    
    if len(brick_list) < 1 and show_list:
        print('No Bricks detected')
    elif len(brick_list) > 1 and show_list:
        for b in brick_list:
            print(str(b))
        show_list =  False




    # Brechen Sie die Schleife ab, wenn die 'q'-Taste gedrückt wird
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Freigeben der Kamera und Schließen der Fenster
# cap.release()
cv2.destroyAllWindows()
