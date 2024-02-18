from enum import Enum
from model.brick import Brick
from PyQt5 import QtGui

import cv2
import utils
import numpy as np

class ImageMode(Enum):
    live = 1
    static = 2

class BrickDetector(object):
    def __init__(self, ui):
        self.videoCapture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.org_frame = None
        self.processed_frame = None
        self.autofocus = 1
        self.focus = 0
        self.brithness = 0
        self.contrast = 0
        self.image_mode = ImageMode.live
        self.brick_list = []
        self.ui = ui
        pass

    def detect_blocks(self):
        brick_list = []

        gray = cv2.cvtColor(self.processed_frame, cv2.COLOR_BGR2GRAY)

        blurred = cv2.GaussianBlur(gray, (3,3), 2)

        morphed = cv2.morphologyEx(blurred, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (5,5)))

        edges = cv2.Canny(morphed, 50, 150)

        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        brick_counter = 0
        for contour in contours:
            area = cv2.contourArea(contour)
            circumfurence = cv2.arcLength(contour, True)

            if area > 0:
                compatness = circumfurence**2 / (4 * np.pi *area)
            else:
                compatness = 0
            if (576 * 0.9) <= area <= (576 * 1.1):
            # if area > 500 and ((4/np.pi)*0.8) <= compactness <= (((4/np.pi)*1.2)) :  # Beispielgrenze für die Mindestgröße der Kontur
                x, y, w, h =cv2.boundingRect(contour)
                dominant_color = utils.dominant_color_from_roi(self.org_frame, contour)
                box = np.intp(cv2.boxPoints(cv2.minAreaRect(contour)))
                brick_list.append(Brick(area=area, circumference=circumfurence, color_code=dominant_color, original_image=self.org_frame, number=brick_counter + 1))
                cv2.drawContours(self.org_frame, [box], 0, (0,255,0), 1)
                cv2.putText(self.org_frame, f'# {brick_counter+1} {brick_list[brick_counter].color_str}', (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255,255,255), 0, cv2.LINE_AA)
        return brick_list
    
    def loop(self, image_path=""): #rename
        brick_list = []
        if self.image_mode == ImageMode.static:
            self.org_frame = cv2.imread(image_path)
            frame, _, _ = utils.automatic_brithness_and_contrast(self.org_frame,1)
            frame = utils.resize_image(frame)
            self.processed_frame = frame.copy()
            brick_list = self.detect_blocks()

            q_image = QtGui.QImage(self.processed_frame.data, self.processed_frame.shape[1], self.processed_frame.shape[0], self.processed_frame.shape[1]*3, QtGui.QImage.Format_RGB888).rgbSwapped()
            # QImage in QPixmap umwandeln und in QGraphicsPixmapItem setzen
            pixmap = QtGui.QPixmap.fromImage(q_image)
            self.ui.video_image_label.setPixmap(pixmap)

            self.brick_list = brick_list
            return brick_list
        elif self.image_mode == ImageMode.live:
            ret, self.org_frame = self.videoCapture.read()
            if not ret:
                print('Kein Bild')
                pass
            frame, _, _ = utils.automatic_brithness_and_contrast(self.org_frame,1)
            frame = utils.resize_image(frame)
            self.processed_frame = frame.copy()
            brick_list = self.detect_blocks()

            q_image = QtGui.QImage(self.processed_frame.data, self.processed_frame.shape[1], self.processed_frame.shape[0], self.processed_frame.shape[1]*3, QtGui.QImage.Format_RGB888).rgbSwapped()
            # QImage in QPixmap umwandeln und in QGraphicsPixmapItem setzen
            pixmap = QtGui.QPixmap.fromImage(q_image)
            self.ui.video_image_label.setPixmap(pixmap)

            self.brick_list = brick_list
            return brick_list
        else:
            print('Fehler, kein image mode ausgewählt')
            return None