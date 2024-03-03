import cv2
import numpy as np

def automatic_brithness_and_contrast(image, clip_hist_percent=1):
    """
    Adjusts the brightness and contrast of an image automatically.

    Args:
        image (np.array): The image to be adjusted.
        clip_hist_percent (float, optional): The percentage of the histogram to be clipped. Defaults to 1.

    Returns:
        tuple: A tuple containing the adjusted image, the scale factor, and the delta used for scaling.
    """
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # If the image is completely black or white, no adjustments are needed
    if np.all(gray == 0) or np.all(gray == 255):
        return (image, 1.0, 0.0)
    
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
    # call width and height of original image
    height, width = image.shape[:2]

    # calculate the aspect ratio of the original image
    aspect_ratio = width / float(height)
    
    # determine if the width or height exceeds the limit
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
        # the image is already smaller than the target size
        return image

    # use cv2.resize to scale the image to the new aspect ratio
    resized_image = cv2.resize(image, (new_width, new_height))

    return resized_image


def dominant_color_from_roi(org_image, contour): 
    """
    Determines the dominant color of an object in an image.
    
    Args:
        org_image (np.array): The original image.
        contour (np.array): The contour of the object.
    Returns:
        np.array: The dominant color of the object.
    """

    # extraxt the area of the image
    rect = cv2.minAreaRect(contour)
    box2 = cv2.boxPoints(rect)
    box2 = np.int0(box2)

    # create a mask for the area inside the rectangle
    mask = np.zeros_like(org_image)
    cv2.drawContours(mask, [box2], 0, (255, 255, 255), thickness=cv2.FILLED)

    # extract the area of the image inside the rectangle
    roi = cv2.bitwise_and(org_image, mask)
    
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
        # biggest contour (assuming the object is the biggest contour)
    if len(contours) == 1:
        prev_largest_contour = contours[0]
    if len(contours) == 0:
        prev_largest_contour = contour
    largest_contour = prev_largest_contour

    # mask for the object
    mask = np.zeros_like(roi)
    cv2.drawContours(mask, [largest_contour], 0, (255, 255, 255), thickness=cv2.FILLED)

    # dominant color of the object
    dominant_color = np.median(roi[mask == 255].reshape(-1, 3), axis=0)

    return dominant_color

def calculate_iou(box1, box2):
    """
    Calculates the Intersection over Union (IoU) of two bounding boxes.

    Args:
        box1 (tuple): The coordinates of the first bounding box in the format (x, y, w, h).
        box2 (tuple): The coordinates of the second bounding box in the format (x, y, w, h).
    Returns:
        float: The IoU of the two bounding boxes.
    """
    # get the coordinates of the bounding boxes
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2

    # Koordinaten der Überlappung berechnen
    # calculate the coordinates of the intersection rectangle
    x_left = max(x1, x2)
    y_top = max(y1, y2)
    x_right = min(x1 + w1, x2 + w2)
    y_bottom = min(y1 + h1, y2 + h2)

    # intersection area calculation
    intersection_area = max(0, x_right - x_left) * max(0, y_bottom - y_top)

    # calculate the area of both bounding boxes
    area1 = w1 * h1
    area2 = w2 * h2
    union_area = area1 + area2 - intersection_area

    # calculate the intersection over union by taking the intersection area and dividing it by the union area
    iou = intersection_area / union_area if union_area > 0 else 0

    return iou

def filter_duplicate_coordinates(brick_list, iou_threshold=0.7):
    """
    Filters out duplicate coordinates from a list of bricks.

    Args:
        brick_list (list): A list of bricks.
        iou_threshold (float, optional): The threshold for the Intersection over Union (IoU). Defaults to 0.7.
    Returns:
        list: A list of bricks with duplicate coordinates removed.
    """
    filtered_list = []
    counter = 1

    # iterate through the list of bricks
    for i, brick1 in enumerate(brick_list):
        should_add = True

        # iterate through the filtered list of bricks
        for j, brick2 in enumerate(filtered_list):
            # calculate the IoU of the two bricks
            iou = calculate_iou(brick1.coordinates, brick2.coordinates)

            # if the IoU is greater than the threshold, the brick should not be added to the filtered list
            if iou > iou_threshold:
                should_add = False
                break

        # if the brick should be added to the filtered list, assign it a number and add it to the list
        if should_add:
            brick1.number = counter
            counter = counter + 1
            filtered_list.append(brick1)

    return filtered_list