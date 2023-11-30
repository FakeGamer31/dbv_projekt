import cv2
import numpy as np
from matplotlib import pyplot as plt

# Funktion für die Objekterkennung
def detect_lego_blocks(frame):
    # Hier implementieren Sie Ihre Bildverarbeitungsschritte
    # ...
        # Bild laden
    frame2 = frame
    # Farbsegmentierung 
    # Untere Grenzwerte (lower bounds) für Blau
    lower = np.array([100, 50, 50])

    # Obere Grenzwerte (upper bounds) für Blau
    upper = np.array([130, 255, 255])
    mask = cv2.inRange(cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV), lower, upper)
    blurred_image = cv2.GaussianBlur(mask, (7, 7), 0)
    # Kantenerkennung
    edges = cv2.Canny(blurred_image, 50, 150)
    
    cv2.imshow('edges', edges)
    # Konturfindung
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # Objekterkennung und Markierung
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:  # Beispielgrenze für die Mindestgröße der Kontur
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame2, (x, y), (x + w, y + h), (180, 255, 50), 2)
    # Bild anzeigen
    return frame2

# Öffnen Sie die Kamera (0 steht für die Standardkamera, kann angepasst werden)
cap = cv2.VideoCapture(1)

while True:
    # Erfassen Sie ein Frame von der Kamera
    ret, frame = cap.read()

    # Überprüfen Sie, ob das Frame korrekt erfasst wurde
    if not ret:
        break

    # Objekterkennung auf dem aktuellen Frame durchführen
    processed_frame = detect_lego_blocks(frame)

    # Zeigen Sie das Original- und das bearbeitete Frame an
    cv2.imshow('Original', frame)
    cv2.imshow('Processed', processed_frame)

    # Brechen Sie die Schleife ab, wenn die 'q'-Taste gedrückt wird
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Freigeben der Kamera und Schließen der Fenster
cap.release()
cv2.destroyAllWindows()
