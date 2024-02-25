import cv2
import numpy as np

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


def resize_image(image, target_width=640, target_height=480):
    # Höhe und Breite des Originalbildes abrufen
    height, width = image.shape[:2]

    # Berechne das Seitenverhältnis des Originalbildes
    aspect_ratio = width / float(height)
    
    # Bestimme, ob die Breite oder Höhe die Grenze überschreitet
    if width > target_width:
        # print(f'width bigger than target width {width}')
        new_width = target_width
        new_height = int(new_width / aspect_ratio)
    elif height > target_height:
        # print('height bigger than target height')
        new_height = target_height
        new_width = int(new_height * aspect_ratio)
    else:
        # print('image same')
        # Das Bild ist bereits kleiner als die Zielgröße
        return image

    # Verwende cv2.resize, um das Bild mit dem neuen Seitenverhältnis zu skalieren
    resized_image = cv2.resize(image, (new_width, new_height))

    return resized_image


def dominant_color_from_roi(org_image, contour): 
      # 1. Extrahieren Sie den Bereich des Bildes
            rect = cv2.minAreaRect(contour)
            box2 = cv2.boxPoints(rect)
            box2 = np.int0(box2)

            # Erstellen Sie eine Maske für den Bereich innerhalb des Rechtecks
            mask = np.zeros_like(org_image)
            cv2.drawContours(mask, [box2], 0, (255, 255, 255), thickness=cv2.FILLED)

            # Extrahieren Sie den Bereich des Bildes innerhalb des Rechtecks
            roi = cv2.bitwise_and(org_image, mask)
            # cv2.imshow('roi', roi) #hier ist nur  noch der block vlt nutzen für die farbe

            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            largest_contour_area = 0
            prev_largest_contour_area = 0
            largest_contour = 0
            prev_largest_contour = 0
            if len(contours) != 0:
                for contour in contours:
                    # find the biggest countour (c) by the area
                    largest_contour_area = cv2.contourArea(contour)
                    largest_contour = contour
                    if prev_largest_contour_area < largest_contour_area:
                        prev_largest_contour_area = largest_contour_area
                        prev_largest_contour = largest_contour
                # Größte Kontur (Annahme: Das Objekt ist die größte Kontur)
            largest_contour = prev_largest_contour

            # Maske für das Objekt erstellen
            mask = np.zeros_like(roi)
            cv2.drawContours(mask, [largest_contour], 0, (255, 255, 255), thickness=cv2.FILLED)

            # Dominante Farbe bestimmen# Dominante Farbe bestimmen
            dominant_color = np.median(roi[mask == 255].reshape(-1, 3), axis=0)

            return dominant_color

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

def filter_duplicate_coordinates(brick_list, iou_threshold=0.7):
    filtered_list = []
    counter = 1

    for i, brick1 in enumerate(brick_list):
        should_add = True

        for j, brick2 in enumerate(filtered_list):
            iou = calculate_iou(brick1.coordinates, brick2.coordinates)

            if iou > iou_threshold:
                should_add = False
                break

        if should_add:
            brick1.number = counter
            counter = counter + 1
            filtered_list.append(brick1)

    return filtered_list