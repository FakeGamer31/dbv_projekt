import cv2
import numpy as np
from matplotlib import pyplot as plt

# Bild laden
image = cv2.imread('../images/legos.jpg')

plt.imshow(image[...,::-1], cmap='gray')
plt.title('Lego Detec')
plt.axis('off')
count = 0
color_ranges = {
    'blue': (np.array([100, 50, 50]), np.array([130, 255, 255])),
    'green': (np.array([30, 50, 50]), np.array([80, 255, 255])),
}
for color, (lower, upper) in color_ranges.items():
    count = count + 1
    mask = cv2.inRange(cv2.cvtColor(image, cv2.COLOR_BGR2HSV), lower, upper)
    plt.imshow(mask, cmap='gray')
    plt.title('mask')
    plt.axis('off')

    blurred_image = cv2.GaussianBlur(mask, (5, 5), 0)
    plt.imshow(blurred_image[...,::-1], cmap='gray')
    plt.title('blurred_image')
    plt.axis('off')
    plt.show()

    # Kantenerkennung
    edges = cv2.Canny(blurred_image, 50, 150)
    plt.imshow(edges[...,::-1], cmap='gray')
    plt.title('edges')
    plt.axis('off')

    # Konturfindung
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    print("Anzahl der Konturen:", len(contours))

    # Objekterkennung und Markierung
    for contour in contours:
        area = cv2.contourArea(contour)
        print(area)
        if area > 100:  # Beispielgrenze für die Mindestgröße der Kontur
            x, y, w, h = cv2.boundingRect(contour)
            mean_color = cv2.mean(image, mask=mask)
            cv2.rectangle(image, (x, y), (x + w, y + h), mean_color, 2)
            cv2.putText(image, color, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, mean_color, 2, cv2.LINE_AA)
    # Bild anzeigen
    print(' ')
    plt.imshow(image[...,::-1], cmap='gray')
    plt.title('Lego Detec')
    plt.axis('off')
plt.show()
print('###########', count)