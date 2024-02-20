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
        self.frame = None
        self.processed_frame = None
        self.autofocus = 1
        self.focus = 0
        self.brithness = 128
        self.contrast = 128
        self.image_mode = ImageMode.live
        self.brick_list = ""
        self.ui = ui
        self.show_brick_list = False
        self.img_path = ""
        pass

    def detect_blocks(self):
        brick_list = []

        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

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
                dominant_color = utils.dominant_color_from_roi(self.processed_frame, contour)
                box = np.intp(cv2.boxPoints(cv2.minAreaRect(contour)))
                brick_list.append(Brick(area=area, circumference=circumfurence, color_code=dominant_color, original_image=self.processed_frame, number=brick_counter + 1))
                cv2.drawContours(self.processed_frame, [box], 0, (0,255,0), 1)
                cv2.putText(self.processed_frame, f'# {brick_counter+1} {brick_list[brick_counter].color_str}', (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255,255,255), 0, cv2.LINE_AA)
                brick_counter = brick_counter + 1
        return brick_list
    
    def loop(self): #rename
        brick_list = []   
        self.set_settings()
        if self.image_mode == ImageMode.static:
            if self.img_path != '':
                self.org_frame = cv2.imread(self.img_path)
            self.frame, _, _ = utils.automatic_brithness_and_contrast(self.org_frame,1)
            self.frame = utils.resize_image(self.frame)
            self.processed_frame = self.frame.copy()
            brick_list = self.detect_blocks()

            q_image = QtGui.QImage(self.processed_frame.data, self.processed_frame.shape[1], self.processed_frame.shape[0], self.processed_frame.shape[1]*3, QtGui.QImage.Format_RGB888).rgbSwapped()
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

        elif self.image_mode == ImageMode.live:        
            ret, self.org_frame = self.videoCapture.read()
            if not ret:
                print('Kein Bild')
                pass
            self.frame, _, _ = utils.automatic_brithness_and_contrast(self.org_frame,1)
            self.frame = utils.resize_image(self.frame)
            self.processed_frame = self.frame.copy()
            brick_list = self.detect_blocks()

            q_image = QtGui.QImage(self.processed_frame.data, self.processed_frame.shape[1], self.processed_frame.shape[0], self.processed_frame.shape[1]*3, QtGui.QImage.Format_RGB888).rgbSwapped()
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
            self.videoCapture.set(cv2.CAP_PROP_BRIGHTNESS,self.brithness)
            self.videoCapture.set(cv2.CAP_PROP_CONTRAST,self.contrast)
            if (self.autofocus):
                self.videoCapture.set(cv2.CAP_PROP_AUTOFOCUS,1)
            else:
                self.videoCapture.set(cv2.CAP_PROP_AUTOFOCUS,0)
                self.videoCapture.set(cv2.CAP_PROP_FOCUS,self.focus)



