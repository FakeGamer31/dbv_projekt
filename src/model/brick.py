from scipy.spatial import KDTree
from webcolors import (hex_to_rgb, CSS21_HEX_TO_NAMES)

HEX_TO_NAMES = {
    "#f0f8ff": "blue",
    "#faebd7": "beige",
    "#00ffff": "cyan",
    "#7fffd4": "green",
    "#f0ffff": "blue",
    "#f5f5dc": "beige",
    "#ffe4c4": "beige",
    "#000000": "black",
    "#ffebcd": "beige",
    "#0000ff": "blue",
    "#8a2be2": "blue",
    "#a52a2a": "brown",
    "#deb887": "brown",
    "#5f9ea0": "blue",
    "#7fff00": "green",
    "#d2691e": "brown",
    "#ff7f50": "orange",
    "#6495ed": "blue",
    "#fff8dc": "beige",
    "#dc143c": "red",
    "#00ffff": "cyan",
    "#00008b": "blue",
    "#008b8b": "cyan",
    "#b8860b": "brown",
    "#a9a9a9": "grey",
    "#006400": "green",
    "#bdb76b": "brown",
    "#8b008b": "purple",
    "#556b2f": "green",
    "#ff8c00": "orange",
    "#9932cc": "purple",
    "#8b0000": "red",
    "#e9967a": "orange",
    "#8fbc8f": "green",
    "#483d8b": "blue",
    "#2f4f4f": "grey",
    "#00ced1": "blue",
    "#9400d3": "purple",
    "#ff1493": "red",
    "#00bfff": "blue",
    "#696969": "grey",
    "#1e90ff": "blue",
    "#b22222": "red",
    "#fffaf0": "white",
    "#228b22": "green",
    "#ff00ff": "magenta",
    "#dcdcdc": "grey",
    "#f8f8ff": "white",
    "#ffd700": "yellow",
    "#daa520": "yellow",
    "#808080": "grey",
    "#008000": "green",
    "#adff2f": "green",
    "#f0fff0": "green",
    "#ff69b4": "red",
    "#cd5c5c": "red",
    "#4b0082": "blue",
    "#fffff0": "yellow",
    "#f0e68c": "yellow",
    "#e6e6fa": "purple",
    "#fff0f5": "red",
    "#7cfc00": "green",
    "#fffacd": "yellow",
    "#add8e6": "blue",
    "#f08080": "red",
    "#e0ffff": "cyan",
    "#fafad2": "yellow",
    "#d3d3d3": "grey",
    "#90ee90": "green",
    "#ffb6c1": "red",
    "#ffa07a": "orange",
    "#20b2aa": "green",
    "#87cefa": "blue",
    "#778899": "grey",
    "#b0c4de": "blue",
    "#ffffe0": "yellow",
    "#00ff00": "green",
    "#32cd32": "green",
    "#faf0e6": "beige",
    "#ff00ff": "magenta",
    "#800000": "red",
    "#66cdaa": "green",
    "#0000cd": "blue",
    "#ba55d3": "purple",
    "#9370db": "purple",
    "#3cb371": "green",
    "#7b68ee": "blue",
    "#00fa9a": "green",
    "#48d1cc": "blue",
    "#c71585": "red",
    "#191970": "blue",
    "#f5fffa": "white",
    "#ffe4e1": "red",
    "#ffe4b5": "orange",
    "#ffdead": "orange",
    "#000080": "blue",
    "#fdf5e6": "beige",
    "#808000": "green",
    "#6b8e23": "green",
    "#ffa500": "orange",
    "#ff4500": "red",
    "#da70d6": "purple",
    "#eee8aa": "yellow",
    "#98fb98": "green",
    "#afeeee": "blue",
    "#db7093": "red",
    "#ffefd5": "yellow",
    "#ffdab9": "orange",
    "#cd853f": "brown",
    "#ffc0cb": "red",
    "#dda0dd": "purple",
    "#b0e0e6": "blue",
    "#800080": "purple",
    "#ff0000": "red",
    "#bc8f8f": "red",
    "#4169e1": "blue",
    "#8b4513": "brown",
    "#fa8072": "orange",
    "#f4a460": "orange",
    "#2e8b57": "green",
    "#fff5ee": "white",
    "#a0522d": "brown",
    "#c0c0c0": "silver",
    "#87ceeb": "blue",
    "#6a5acd": "blue",
    "#708090": "grey",
    "#fffafa": "white",
    "#00ff7f": "green",
    "#4682b4": "blue",
    "#d2b48c": "brown",
    "#008080": "blue",
    "#d8bfd8": "purple",
    "#ff6347": "red",
    "#40e0d0": "blue",
    "#ee82ee": "purple",
    "#f5deb3": "brown",
    "#ffffff": "white",
    "#f5f5f5": "grey",
    "#ffff00": "yellow",
    "#9acd32": "green",
}

class Brick:
    def __init__(self, area, circumference, color_code, original_image, number):
        self.area = area
        self.circumference = circumference
        self.color_code = color_code
        self.original_image = original_image
        self.number = number

        # Setze den Type basierend auf den Werten von area und circumference
        if  576*0.9 <= area <= 576*1.1 and 96*0.9 <= circumference <= 96*1.1:
            self.type = "2x2"
        # elif area == 6.0 and circumference == 10.0:
        #     self.type = "2x3"
        # elif area == 8.0 and circumference == 12.0:
        #     self.type = "2x4"
        else:
            self.type = "Unknown"

        blue, green, red = self.color_code
        # print(f'number: {self.number} and color code: {self.color_code}')
        self.color_str = self.__convert_rgb_to_names((red, green, blue))

    def __str__(self):
        return f"#: {self.number}, \tType: {self.type}, \tColor: {self.color_str}, \tArea: {self.area}, \tCircumference: {self.circumference}"
    
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
            
