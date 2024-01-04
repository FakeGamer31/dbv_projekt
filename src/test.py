import cv2
import math
import numpy as np
from matplotlib import pyplot as plt

g = 0
kernel_morph = (5,5)


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




# Funktion für die Objekterkennung
def detect_lego_blocks(dst,lower, upper, color):
    global g
    global kernel_morph

    # Grayscale
    # mask = cv2.inRange(cv2.cvtColor(dst, cv2.COLOR_BGR2HSV), lower, upper)
    mask = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
    cv2.imshow('mask', mask)

    # Blur
    blurred_image = cv2.GaussianBlur(mask, (3, 3), 0)
    cv2.imshow('blurred', blurred_image)

    # Morph
    morph2 = cv2.morphologyEx(blurred_image, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT,(3,3)))
    # erode = cv2.erode(edges, cv2.getStructuringElement(cv2.MORPH_RECT,(1,1)), iterations=100)
    # morph = cv2.dilate(erode, cv2.getStructuringElement(cv2.MORPH_RECT,(1,1)), iterations=1)
    cv2.imshow('morph', morph2)
 

    g = cv2.getTrackbarPos('min', 'edges')
    cv2.getTrackbarPos('kernel', 'edges')
    # print(kernel_morph)
    # print(g, ' and ',b)
    print(g)
    edges2 = cv2.Canny(morph2, g, g*3)
    cv2.imshow('edges', edges2)

 
    
    testaray= np.array([])
    # Konturfindung
    contours, _ = cv2.findContours(edges2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # Objekterkennung und Markierung
    for contour in contours:
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)

        if area > 0:
            compactness =  (perimeter**2) / (4 * np.pi * area)
        else:
            compactness = 0
        testaray = np.append(testaray, (area,perimeter,compactness))
        print('area: ', area, '   perimeter: ', perimeter, '     compactness: ', compactness )
        print('')
        if area > 100 and ((4/np.pi)*0.96) <= compactness <= (((4/np.pi)*1.04)) :  # Beispielgrenze für die Mindestgröße der Kontur
            x, y, w, h = cv2.boundingRect(contour)
            # cv2.rectangle(frame2, (x, y), (x + w, y + h), (180, 255, 50), 2)
            box = np.intp(cv2.boxPoints(cv2.minAreaRect(contour)))
            cv2.drawContours(dst, [box], 0, (0,255,0), 2)
            cv2.putText(dst, color, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 0, cv2.LINE_AA)


color_ranges = {
    'white': (np.array([0, 0, 180]), np.array([255, 255, 255])),
    # 'yellow': (np.array([20, 100, 100]), np.array([40, 255, 255])),
    # 'blue': (np.array([100, 100, 100]), np.array([140, 255, 255])),
    # 'red': (np.array([0, 100, 100]), np.array([10, 255, 255])),
    # 'grey': (np.array([0, 0, 80]), np.array([180, 40, 200])),
    # 'green': (np.array([40, 40, 40]), np.array([80, 255, 255])),
    # 'black': (np.array([0, 0, 0]), np.array([180, 255, 50])),
}

cv2.namedWindow('edges') 
cv2.createTrackbar('min','edges',100,255,something)
cv2.createTrackbar('kernel','edges',0,4,change_kernel)

# Öffnen Sie die Kamera (0 steht für die Standardkamera, kann angepasst werden)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)

## Erfassen Sie ein Frame von der Kamera
# ret, frame = cap.read()
# frame_processed = frame.copy()

# # Überprüfen Sie, ob das Frame korrekt erfasst wurde
# if not ret:
#     print('Kein Bild')

frame = img = cv2.resize(cv2.imread('../images/iris_8_blocks.jpg'), None, fx=0.35, fy=0.35, interpolation=cv2.INTER_LINEAR)
frame_processed = frame.copy()

counter = 0

for color, (lower, upper) in color_ranges.items():
    # Objekterkennung auf dem aktuellen Frame durchführen
    detect_lego_blocks(frame_processed,lower,upper, color)
    counter = counter + 1

    # Zeigen Sie das Original- und das bearbeitete Frame an
    cv2.imshow('Original', frame)
    cv2.imshow('Processed', frame_processed)
    cv2.waitKey(0)

    # Brechen Sie die Schleife ab, wenn die 'q'-Taste gedrückt wird
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Freigeben der Kamera und Schließen der Fenster
cap.release()
cv2.destroyAllWindows()
