import colorsys
import random

class Plant:
    def __init__(self):
        # Initialize with a random hue (0 to 1)
        self.hue = random.uniform(0, 1)
        self.color = self.hsl_to_rgb(self.hue, 1, 0.5)  # Full saturation and medium lightness
        self.drawn = False
        self.has_empty_neighbours = True

    def clone(self):
        mutation = random.uniform(-0.01, 0.01)  # Hue mutation within a small range
        new_hue = min(1, max(0, self.hue + mutation))  # Ensure hue stays in the range [0, 1]
        cloned_cell = Plant()
        cloned_cell.hue = new_hue
        cloned_cell.color = cloned_cell.hsl_to_rgb(new_hue, 1, 0.5)  # Convert mutated hue to RGB
        return cloned_cell

    def hsl_to_rgb(self, h, s, l):
        return tuple(round(c * 255) for c in colorsys.hls_to_rgb(h, l, s))
