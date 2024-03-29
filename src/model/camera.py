from utils import filter_duplicate_coordinates
from constants import (BLUR_KERNEL, CANNY_MIN, MORTPH_KERNEL)
from itertools import product
from enum import Enum
from model.brick import Brick
from PyQt5 import QtGui

import cv2
import utils
import numpy as np

combinations = list(product(BLUR_KERNEL, MORTPH_KERNEL, CANNY_MIN))

class ImageMode(Enum):
    live = 1
    static = 2

class BrickDetector(object):
    def __init__(self, ui):
        self.videoCapture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.org_frame = None
        self.frame = None
        self.processed_frame = None
        self.autofocus = 1
        self.focus = 0
        self.brightness = 128
        self.contrast = 128
        self.image_mode = ImageMode.live
        self.brick_list = ""
        self.ui = ui
        self.show_brick_list = False
        self.img_path = ""
        self.detect_flag = True
        pass

    def detect_blocks(self,blur_kernel,morph_kernel,canny_min): 
        """
        Detects blocks in the processed frame of the image.

        This function applies a series of image processing techniques including
        grayscale conversion, Gaussian blur, morphological operations, and Canny edge detection
        to detect blocks in the image. It then finds contours in the resulting image and calculates
        the compactness of each contour to determine if it represents a block.

        Parameters:
        blur_kernel (tuple): The kernel size for the Gaussian blur operation.
        morph_kernel (tuple): The kernel size for the morphological operation.
        canny_min (int): The minimum threshold for the Canny edge detection.

        Returns:
        brick_list (list): A list of detected bricks in the image.
        """
        brick_list = []

        gray = cv2.cvtColor(self.processed_frame, cv2.COLOR_BGR2GRAY)

        blurred = cv2.GaussianBlur(gray, blur_kernel, 0)

        morphed = cv2.morphologyEx(blurred, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, morph_kernel))

        edges = cv2.Canny(morphed, canny_min, canny_min*3)

        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            area = cv2.contourArea(contour)
            circumfurence = cv2.arcLength(contour, True)

            if area > 0:
                compactness = circumfurence**2 / (4 * np.pi *area)
            else:
                compactness = 0
            # if (576 * 0.9) <= area <= (576 * 1.1):
            if area > 500:  # Beispielgrenze für die Mindestgröße der Kontur
                x, y, w, h =cv2.boundingRect(contour)
                dominant_color = utils.dominant_color_from_roi(self.processed_frame, contour)
                brick_list.append(Brick(area=area, circumference=circumfurence, color_code=dominant_color, original_image=self.org_frame, coordinates=(x,y,w,h), contour=contour))
        return brick_list
    
    def loop(self):
        """
        Main loop for processing video frames and detecting bricks.

        This function continuously captures frames from the video source, processes them,
        and detects bricks. If bricks are detected, it updates the brick list. If no bricks
        are detected, it clears the brick list.

        In live mode, the function reads frames from the video capture, resizes them, and adjusts
        their brightness and contrast. It then detects blocks in the processed frame using various
        combinations of blur kernel, morph kernel, and canny min values. It filters out duplicate
        coordinates from the detected blocks and updates the brick list.

        In static mode, the function displays the processed frame and updates the brick list based
        on the detected bricks.

        Raises:
        Exception: If no image mode is selected.
        """
        brick_list = []   
        self.set_settings()
        if self.image_mode == ImageMode.static:
            if self.detect_flag:
                if self.img_path != '':
                    self.org_frame = cv2.imread(self.img_path)
                else:
                    self.org_frame = self.org_frame_copy
                self.org_frame = utils.resize_image(self.org_frame)
                self.processed_frame, _, _ = utils.automatic_brithness_and_contrast(self.org_frame,1)

                for (blur_kernel,morph_kernel,canny_min) in combinations:
                    brick_list = brick_list + self.detect_blocks(blur_kernel,morph_kernel,canny_min)

                temp_brick_list = []
                for brick in brick_list:
                    if brick.type != '-':
                        temp_brick_list.append(brick)
                    
                brick_list = filter_duplicate_coordinates(temp_brick_list)
                for brick in brick_list:
                    contour = brick.contour
                    x, y, w, h = cv2.boundingRect(contour)
                    box = np.intp(cv2.boxPoints(cv2.minAreaRect(contour)))
                    cv2.drawContours(self.org_frame, [box], 0, (0,255,0), 1)
                    cv2.putText(self.org_frame, f'#{brick.number} {brick.color_str}', (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255,255,255), 0, cv2.LINE_AA)

                q_image = QtGui.QImage(self.org_frame.data, self.org_frame.shape[1], self.org_frame.shape[0], self.org_frame.shape[1]*3, QtGui.QImage.Format_RGB888).rgbSwapped()
                # QImage in QPixmap umwandeln und in QGraphicsPixmapItem setzen
                pixmap = QtGui.QPixmap.fromImage(q_image)
                self.ui.video_image_label.setPixmap(pixmap)

                if len(brick_list) < 1:
                    self.brick_list = ""
                    self.ui.brick_list_text_area.setPlainText('No bricks')    
                else:
                    self.brick_list = ""
                    for brick in brick_list:
                        self.brick_list = self.brick_list + f'{str(brick)}\n'
                    self.ui.brick_list_text_area.setPlainText(self.brick_list)
                self.detect_flag = False

        elif self.image_mode == ImageMode.live:        
            ret, self.org_frame = self.videoCapture.read()
            if not ret:
                print('Kein Bild')
                return
            self.org_frame = utils.resize_image(self.org_frame)
            self.org_frame_copy = self.org_frame.copy()
            self.processed_frame, _, _ = utils.automatic_brithness_and_contrast(self.org_frame,1)

            for (blur_kernel,morph_kernel,canny_min) in combinations:
                brick_list = brick_list + self.detect_blocks(blur_kernel,morph_kernel,canny_min)
            
            temp_brick_list = []
            for brick in brick_list:
                if brick.type != '-':
                    temp_brick_list.append(brick)

            brick_list = filter_duplicate_coordinates(temp_brick_list)
            for brick in brick_list:
                contour = brick.contour
                x, y, w, h = cv2.boundingRect(contour)
                box = np.intp(cv2.boxPoints(cv2.minAreaRect(contour)))
                cv2.drawContours(self.org_frame, [box], 0, (0,255,0), 1)
                cv2.putText(self.org_frame, f'#{brick.number} {brick.color_str}', (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255,255,255), 0, cv2.LINE_AA)

            q_image = QtGui.QImage(self.org_frame.data, self.org_frame.shape[1], self.org_frame.shape[0], self.org_frame.shape[1]*3, QtGui.QImage.Format_RGB888).rgbSwapped()
            # QImage in QPixmap umwandeln und in QGraphicsPixmapItem setzen
            pixmap = QtGui.QPixmap.fromImage(q_image)
            self.ui.video_image_label.setPixmap(pixmap)
            
            if len(brick_list) < 1 and self.show_brick_list:
                self.brick_list = ""
                self.ui.brick_list_text_area.setPlainText('No bricks')    
            elif self.show_brick_list:            
                self.brick_list = ""
                for brick in brick_list:
                    self.brick_list = self.brick_list + f'{str(brick)}\n'
                self.ui.brick_list_text_area.setPlainText(self.brick_list)
                self.show_brick_list = False

        else:
            print('Fehler, kein image mode ausgewählt')
    
    def set_settings(self): 
        """
        Sets the settings for the video capture.

        This function sets the brightness, contrast, and autofocus settings for the video capture.
        If autofocus is enabled, it sets the autofocus property. If autofocus is disabled, it sets
        the focus level manually.
        """  
        self.videoCapture.set(cv2.CAP_PROP_BRIGHTNESS,self.brightness)
        self.videoCapture.set(cv2.CAP_PROP_CONTRAST,self.contrast)
        if (self.autofocus):
            self.videoCapture.set(cv2.CAP_PROP_AUTOFOCUS,1)
        else:
            self.videoCapture.set(cv2.CAP_PROP_AUTOFOCUS,0)
            self.videoCapture.set(cv2.CAP_PROP_FOCUS,self.focus)



