import cv2
import utils
import numpy as np
from matplotlib import pyplot as plt
from model.brick import Brick

g = 102
max = 255
sig = 2
kernel_morph = (9,9)
kernel_blur = (1,1)


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
def detect_lego_blocks(dst, org_img, lower, upper, color):
    global g
    global kernel_morph
    global kernel_blur
    global sig
    global max

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
    blurred_image = cv2.GaussianBlur(mask, kernel_blur,sig)
    cv2.imshow('blurred', blurred_image)

    # Morph
    morph2 = cv2.morphologyEx(blurred_image, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT,kernel_morph))
    # erode = cv2.erode(edges, cv2.getStructuringElement(cv2.MORPH_RECT,(1,1)), iterations=100)
    # morph = cv2.dilate(erode, cv2.getStructuringElement(cv2.MORPH_RECT,(1,1)), iterations=1)
    cv2.imshow('morph', morph2)
 

    g = cv2.getTrackbarPos('min', 'edges')
    max = cv2.getTrackbarPos('max', 'edges')
    # print('canny thresh  ', g)
    cv2.getTrackbarPos('kernel', 'edges')
    # print('kernel morph  ',kernel_morph)
    # print(kernel_morph)
    # print(g, ' and ',b)
    edges2 = cv2.Canny(morph2, g, max)
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
        print('area: ', area, '   perimeter: ', circumference, '     compactness: ', compactness )
        print('')
        if area > 500 and ((4/np.pi)*0.8) <= compactness <= (((4/np.pi)*1.2)) :  # Beispielgrenze für die Mindestgröße der Kontur
        # if 576*0.9 <= area <= 576*1.1:  # Beispielgrenze für die Mindestgröße der Kontur
            brick_list.append(Brick(area=area, circumference=circumference, color=color,original_image=org_img,number=index_counter+1))
            print(f'perimeter: {circumference}')
            x, y, w, h = cv2.boundingRect(contour)
            # cv2.rectangle(frame2, (x, y), (x + w, y + h), (180, 255, 50), 2)
            box = np.intp(cv2.boxPoints(cv2.minAreaRect(contour)))
            cv2.drawContours(org_img, [box], 0, (0,255,0), 2)
            cv2.putText(org_img,f'# {index_counter+1} {color}' , (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255,255,255), 0, cv2.LINE_AA)
            index_counter += 1
    # print('stop##########################################')
    return brick_list


color_ranges = {    
    '-': (np.array([0, 0, 0]), np.array([0, 0, 0])),
    # 'white': (np.array([0, 0, 180]), np.array([255, 255, 255])),
    # 'yellow': (np.array([20, 100, 100]), np.array([40, 255, 255])),
    # 'blue': (np.array([100, 100, 100]), np.array([140, 255, 255])),
    # 'red': (np.array([0, 100, 100]), np.array([10, 255, 255])),
    # 'grey': (np.array([0, 0, 80]), np.array([180, 40, 200])),
    # 'green': (np.array([40, 40, 40]), np.array([80, 255, 255])),
    # 'black': (np.array([0, 0, 0]), np.array([180, 255, 50])),
}

cv2.namedWindow('edges') 
cv2.namedWindow('blurred') 
cv2.createTrackbar('min','edges',102,255,something)
cv2.createTrackbar('max','edges',255,255,something)
cv2.createTrackbar('kernel','edges',4,4,change_kernel)
cv2.createTrackbar('kernel_blur','blurred',0,4,change_kernel_blur)
cv2.createTrackbar('blur_sigma','blurred',2,15,something)

# Öffnen Sie die Kamera (0 steht für die Standardkamera, kann angepasst werden)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)

## Erfassen Sie ein Frame von der Kamera
# ret, frame = cap.read()
# frame_processed = frame.copy()

# # Überprüfen Sie, ob das Frame korrekt erfasst wurde
# if not ret:
#     print('Kein Bild')
show_list = True
brick_list = []
while True:
    org_img = cv2.imread('../images/newest/legos_top_view.jpg')
    frame, _, _  = utils.automatic_brithness_and_contrast(org_img,1)
    frame = utils.resize_image(frame)
    frame_processed = org_img.copy()

    for color, (lower, upper) in color_ranges.items():
        # Objekterkennung auf dem aktuellen Frame durchführen
        brick_list = detect_lego_blocks(frame, frame_processed, lower, upper, color)

    # Zeigen Sie das Original- und das bearbeitete Frame an
    cv2.imshow('Original', org_img)
    cv2.imshow('Auto contrast and brithness', frame)
    cv2.imshow('Processed', frame_processed)

    if len(brick_list) < 1 and show_list:
        print('No Bricks detected')
    else:
        for b in brick_list:
            print(str(b))
        show_list =  False




    # Brechen Sie die Schleife ab, wenn die 'q'-Taste gedrückt wird
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Freigeben der Kamera und Schließen der Fenster
cap.release()
cv2.destroyAllWindows()
