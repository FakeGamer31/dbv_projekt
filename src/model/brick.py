from scipy.spatial import KDTree
from webcolors import hex_to_rgb
from constants import HEX_TO_NAMES

class Brick:
    def __init__(self, area, circumference, color_code, original_image, coordinates, contour):
        self.area = area
        self.circumference = circumference
        self.color_code = color_code
        self.original_image = original_image
        self.coordinates = coordinates
        self.contour = contour

        # Setze den Type basierend auf den Werten von area und circumference
        if  576*0.9 <= area <= 576*1.1 and 96*0.9 <= circumference <= 96*1.1:
            self.type = "2x2"
        # elif area == 6.0 and circumference == 10.0:
        #     self.type = "2x3"
        # elif area == 8.0 and circumference == 12.0:
        #     self.type = "2x4"
        else:
            self.type = "-"

        blue, green, red = self.color_code
        # print(f'number: {self.number} and color code: {self.color_code}')
        self.color_str = self.__convert_rgb_to_names((red, green, blue))

    def __str__(self):
        return f"Type: {self.type}, \tColor: {self.color_str}, \tArea: {self.area}, \tCircumference: {self.circumference}, \tCoordinates: {self.coordinates}"
    
    def __convert_rgb_to_names(self, rgb_tuple):
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
            
