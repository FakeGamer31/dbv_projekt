from scipy.spatial import KDTree
from webcolors import hex_to_rgb
from constants import HEX_TO_NAMES
from enum import Enum

import numpy as np

class Compactness(Enum):
    """
    Enum representing the compactness of different brick types.
    """
    TwoByTwo    = 4/np.pi
    TwoByThree  = 25/(6*np.pi)
    TwoByFour   = 9/(2*np.pi)
    TwoByFive   = 49/(10*np.pi)
    TwoBySix    = 16/(3*np.pi)

class Brick:
    """
    Class representing a brick.

    Attributes:
        area (float): The area of the brick.
        circumference (float): The circumference of the brick.
        color_code (str): The color code of the brick.
        original_image (np.array): The original image of the brick.
        coordinates (tuple): The coordinates of the brick.
        contour (np.array): The contour of the brick.
        compactness (float): The compactness of the brick.
        number (str): The number of the brick.
    """
    def __init__(self, area, circumference, color_code, original_image, coordinates, contour):
        """
        Initializes a Brick instance.

        Args:
            area (float): The area of the brick.
            circumference (float): The circumference of the brick.
            color_code (str): The color code of the brick.
            original_image (np.array): The original image of the brick.
            coordinates (tuple): The coordinates of the brick.
            contour (np.array): The contour of the brick.
        """
        self.area = area
        self.circumference = circumference
        self.color_code = color_code
        self.original_image = original_image
        self.coordinates = coordinates
        self.contour = contour
        self.compactness = circumference**2 / (4 * np.pi *area)
        self.number = ''

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
        """
        Converts an RGB color code to a color name.

        Args:
            rgb_tuple (tuple): The RGB color code to be converted.

        Returns:
            str: The name of the color.
        """
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
    

            
