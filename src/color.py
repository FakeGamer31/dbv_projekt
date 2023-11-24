import numpy as np
import matplotlib.pyplot as plt

# Untere Grenzwerte (lower_bound)
lower_bound = np.array([127, 127, 255])

# Obere Grenzwerte (upper_bound)
upper_bound = np.array([96, 127, 255])

# Erstellen Sie ein Numpy-Array mit nur einer Zeile, die die unteren und oberen Grenzwerte enthält
color_range = np.array([lower_bound, upper_bound])

# Zeigen Sie die Farben an
plt.imshow(color_range.reshape(1, 2, 3) / [180, 255, 255], cmap='gray')
plt.title('Farbpalette')
plt.axis('off')
plt.show()
