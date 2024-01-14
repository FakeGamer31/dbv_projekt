class Brick:
    def __init__(self, area, circumference, color, original_image, number):
        self.area = area
        self.circumference = circumference
        self.color = color
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

    def __str__(self):
        return f"#: {self.number}, \tType: {self.type}, \tColor: {self.color}, \tArea: {self.area}, \tCircumference: {self.circumference}"
            
