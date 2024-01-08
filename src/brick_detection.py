import cv2
import math
import numpy as np
from matplotlib import pyplot as plt

def automatic_brithness_and_contrast(image, clip_hist_percent=1):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Calculate grayscale histogram
    hist = cv2.calcHist([gray],[0],None,[256],[0,256])
    hist_size = len(hist)
    
    # Calculate cumulative distribution from the histogram
    accumulator = []
    accumulator.append(float(hist[0]))
    for index in range(1, hist_size):
        accumulator.append(accumulator[index -1] + float(hist[index]))
    
    # Locate points to clip
    maximum = accumulator[-1]
    clip_hist_percent *= (maximum/100.0)
    clip_hist_percent /= 2.0
    
    # Locate left cut
    minimum_gray = 0
    while accumulator[minimum_gray] < clip_hist_percent:
        minimum_gray += 1
    
    # Locate right cut
    maximum_gray = hist_size -1
    while accumulator[maximum_gray] >= (maximum - clip_hist_percent):
        maximum_gray -= 1
    
    # Calculate alpha and beta values
    alpha = 255 / (maximum_gray - minimum_gray)
    beta = -minimum_gray * alpha
    
    '''
    # Calculate new histogram with desired range and show histogram 
    new_hist = cv2.calcHist([gray],[0],None,[256],[minimum_gray,maximum_gray])
    plt.plot(hist)
    plt.plot(new_hist)
    plt.xlim([0,256])
    plt.show()
    '''

    auto_result = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return (auto_result, alpha, beta)

g = 38
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

    # Grayscale
    # mask = cv2.inRange(cv2.cvtColor(dst, cv2.COLOR_BGR2HSV), lower, upper)
    mask = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
    cv2.imshow('mask', mask)

    # Blur
    cv2.getTrackbarPos('kernel_blur', 'blurred')
    sig = cv2.getTrackbarPos('blur_sigma', 'blurred')
    print('sigma ',sig)
    print('kernel blur  ', kernel_blur)
    blurred_image = cv2.GaussianBlur(mask, kernel_blur,sig)
    cv2.imshow('blurred', blurred_image)

    # Morph
    morph2 = cv2.morphologyEx(blurred_image, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT,kernel_morph))
    # erode = cv2.erode(edges, cv2.getStructuringElement(cv2.MORPH_RECT,(1,1)), iterations=100)
    # morph = cv2.dilate(erode, cv2.getStructuringElement(cv2.MORPH_RECT,(1,1)), iterations=1)
    cv2.imshow('morph', morph2)
 

    g = cv2.getTrackbarPos('min', 'edges')
    print('canny thresh  ', g)
    cv2.getTrackbarPos('kernel', 'edges')
    print('kernel morph  ',kernel_morph)
    # print(kernel_morph)
    # print(g, ' and ',b)
    edges2 = cv2.Canny(morph2, g, g*3)
    cv2.imshow('edges', edges2)

 
    
    testaray= np.array([])
    # Konturfindung
    contours, _ = cv2.findContours(edges2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Objekterkennung und Markierung
    # print('start####################################')
    for contour in contours:
        # print(contour)
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)

        if area > 0:
            compactness =  (perimeter**2) / (4 * np.pi * area)
        else:
            compactness = 0
        testaray = np.append(testaray, (area,perimeter,compactness))
        # print('area: ', area, '   perimeter: ', perimeter, '     compactness: ', compactness )
        # print('')
        # if area > 100 and ((4/np.pi)*0.96) <= compactness <= (((4/np.pi)*1.04)) :  # Beispielgrenze für die Mindestgröße der Kontur
        if 576*0.9 <= area <= 576*1.1:  # Beispielgrenze für die Mindestgröße der Kontur
            x, y, w, h = cv2.boundingRect(contour)
            # cv2.rectangle(frame2, (x, y), (x + w, y + h), (180, 255, 50), 2)
            box = np.intp(cv2.boxPoints(cv2.minAreaRect(contour)))
            cv2.drawContours(org_img, [box], 0, (0,255,0), 2)
            cv2.putText(org_img, color, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 0, cv2.LINE_AA)
    # print('stop##########################################')


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
cv2.namedWindow('blurred') 
cv2.createTrackbar('min','edges',38,255,something)
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
while True:
    org_img = cv2.imread('../images/newest/legos_top_view_spaced.jpg')
    frame, _, _  = automatic_brithness_and_contrast(org_img,1)
    if (org_img.shape[0] > 480 and org_img.shape[1] > 640):
        frame = cv2.resize(frame, None, fx=0.35, fy=0.35, interpolation=cv2.INTER_LINEAR)
    frame_processed = org_img.copy()

    counter = 0

    for color, (lower, upper) in color_ranges.items():
        # Objekterkennung auf dem aktuellen Frame durchführen
        detect_lego_blocks(frame, frame_processed, lower, upper, color)
        counter = counter + 1

    # Zeigen Sie das Original- und das bearbeitete Frame an
    cv2.imshow('Original', org_img)
    cv2.imshow('Auto con and brith', frame)
    cv2.imshow('Processed', frame_processed)

    # Brechen Sie die Schleife ab, wenn die 'q'-Taste gedrückt wird
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Freigeben der Kamera und Schließen der Fenster
cap.release()
cv2.destroyAllWindows()
