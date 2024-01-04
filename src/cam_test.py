import cv2
import numpy as np
from matplotlib import pyplot as plt

# Funktion für die Objekterkennung
def detect_lego_blocks(frame):
    def something(x):
        pass
    
        
    cv2.namedWindow('edges') 
    cv2.createTrackbar('min','edges',0,255,something)
    cv2.createTrackbar('max','edges',0,255,something)
    
    # Bild laden
    frame2 = frame.copy()
    # Grayscale
    mask = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    cv2.imshow('mask', mask)
    # Blur
    blurred_image = cv2.GaussianBlur(mask, (3, 3), 0)
    cv2.imshow('blurred', blurred_image)

    # Kantenerkennung
    # edges = cv2.Canny(blurred_image, 30, 90)
    # cv2.imshow('edges', edges)

    while(1):
        g = cv2.getTrackbarPos('min', 'edges')
        b = cv2.getTrackbarPos('max', 'edges')
        print(g, ' and ',b)
        edges = cv2.Canny(blurred_image, g, b)
        cv2.imshow('edges', edges)
        k = cv2.waitKey (1) & 0xFF
        if k == 27:
            break


    # Opening
    opening = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT,(3,3)))
    cv2.imshow('opening',opening )
    

    # Konturfindung
    contours, _ = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # Objekterkennung und Markierung
    for contour in contours:
        print(cv2.contourArea(contour))
        area = cv2.contourArea(contour)
        if area > 100:  # Beispielgrenze für die Mindestgröße der Kontur
            mean_color = cv2.mean(frame2, mask=mask)
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame2, (x, y), (x + w, y + h), (180, 255, 50), 2)
            cv2.putText(frame2, 'test', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, mean_color, 2, cv2.LINE_AA)
    # Bild anzeigen
    return frame2

# Öffnen Sie die Kamera (0 steht für die Standardkamera, kann angepasst werden)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOCUS, 20)

    # Erfassen Sie ein Frame von der Kamera
ret, frame = cap.read()

# Überprüfen Sie, ob das Frame korrekt erfasst wurde
if not ret:
    cap.release()
    cv2.destroyAllWindows()


# Objekterkennung auf dem aktuellen Frame durchführen
processed_frame = detect_lego_blocks(frame)

# Zeigen Sie das Original- und das bearbeitete Frame an
cv2.imshow('Original', frame)
cv2.imshow('Processed', processed_frame)

# Brechen Sie die Schleife ab, wenn die 'q'-Taste gedrückt wird
if cv2.waitKey(1) & 0xFF == ord('q'):
    # Freigeben der Kamera und Schließen der Fenster
    cap.release()
    cv2.destroyAllWindows()
