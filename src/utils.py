import cv2

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
        print(f'width bigger than target width {width}')
        new_width = target_width
        new_height = int(new_width / aspect_ratio)
    elif height > target_height:
        print('height bigger than target height')
        new_height = target_height
        new_width = int(new_height * aspect_ratio)
    else:
        print('image same')
        # Das Bild ist bereits kleiner als die Zielgröße
        return image

    # Verwende cv2.resize, um das Bild mit dem neuen Seitenverhältnis zu skalieren
    print('call cv2.resize')
    resized_image = cv2.resize(image, (new_width, new_height))

    return resized_image