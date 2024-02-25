from scipy.spatial import KDTree
from webcolors import hex_to_rgb
from constants import HEX_TO_NAMES
from enum import Enum

import numpy as np
import cv2

class Compactness(Enum):
    TwoByTwo    = 4/np.pi
    TwoByThree  = 25/(6*np.pi)
    TwoByFour   = 9/(2*np.pi)
    TwoByFive   = 49/(10*np.pi)
    TwoBySix    = 16/(3*np.pi)

class Brick:
    def __init__(self, area, circumference, color_code, original_image, coordinates, contour):
        self.area = area
        self.circumference = circumference
        self.color_code = color_code
        self.original_image = original_image
        self.coordinates = coordinates
        self.contour = contour
        self.compactness = circumference**2 / (4 * np.pi *area)
        self.number = ''
        self.edges = np.sqrt(np.sum(np.diff(np.vstack((np.intp(cv2.boxPoints(cv2.minAreaRect(contour))), np.intp(cv2.boxPoints(cv2.minAreaRect(self.contour)))[0])), axis=0)**2,axis=1))

        # Setze den Type basierend auf den Werten von area und circumference
        # if  576*0.9 <= area <= 576*1.1 and 96*0.9 <= circumference <= 96*1.1:
        if ((Compactness.TwoByTwo.value*0.95) <= self.compactness < Compactness.TwoByThree.value):
            self.type = "2x2"
        elif Compactness.TwoByThree.value <= self.compactness < Compactness.TwoByFour.value:
            self.type = "2x3"
        elif Compactness.TwoByFour.value <= self.compactness < Compactness.TwoByFive.value:
            self.type = "2x4"
        elif Compactness.TwoByFive.value <= self.compactness < Compactness.TwoBySix.value:
            self.type = "2x5"
        elif Compactness.TwoBySix.value <= self.compactness <= Compactness.TwoBySix.value*1.1:
            self.type = "2x6"
        else:
            self.type = "-"

        blue, green, red = self.color_code
        # print(f'number: {self.number} and color code: {self.color_code}')
        self.color_str = self.__convert_rgb_to_names__((red, green, blue))

    def __str__(self):
        return f"#: {self.number}, Type: {self.type}, \tColor: {self.color_str}, \tArea: {self.area}, \tCircumference: {self.circumference}, \tCompacntess: {self.compactness}"
    
    def __convert_rgb_to_names__(self, rgb_tuple):
        # a dictionary of all the hex and their respective names in css3
        css3_db = HEX_TO_NAMES
        names = []
        rgb_values = []
        for color_hex, color_name in css3_db.items():
            names.append(color_name)
            rgb_values.append(hex_to_rgb(color_hex))
        
        kdt_db = KDTree(rgb_values)
        distance, index = kdt_db.query(rgb_tuple)
        return names[index]
    
    def __is_box_squared__(self, numbers, tolerance=1):
        """
        Check if all numbers in the given list are roughly the same within a certain tolerance.

        Parameters:
        - numbers: List of numbers to be checked.
        - tolerance: Tolerance level for considering numbers as roughly the same.

        Returns:
        - True if all numbers are roughly the same, False otherwise.
        """
        # Check if the difference between each pair of consecutive numbers is within the tolerance
        wurp = all(abs(numbers[i] - numbers[i+1]) <= tolerance for i in range(len(numbers)-1))
        print(wurp)
        return wurp

            
