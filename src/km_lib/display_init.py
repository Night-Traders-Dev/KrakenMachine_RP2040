import math
import displayio
import terminalio
from adafruit_display_text import label
import board
import busio
import gc9a01
import microcontroller

class GC9A01_Display:
    def __init__(self):
        displayio.release_displays()

        self.spi = busio.SPI(clock=board.GP10, MOSI=board.GP11)
        self.display_bus = displayio.FourWire(
            self.spi,
            command=board.GP8,
            chip_select=board.GP9,
            reset=board.GP12
        )
        self.display = gc9a01.GC9A01(
            self.display_bus,
            width=240,
            height=240,
            backlight_pin=board.GP25
        )
        self.root_group = displayio.Group()
        self.display.root_group = self.root_group
        self.text_elements = {}

    def fill_background(self, color):
        bg_bitmap = displayio.Bitmap(240, 240, 1)
        bg_palette = displayio.Palette(1)
        bg_palette[0] = color
        bg_tile = displayio.TileGrid(bg_bitmap, pixel_shader=bg_palette)
        self.root_group.append(bg_tile)

    def draw_text(self, id, x, y, text, color, font):
        text_area = label.Label(font, text=text, color=color)
        text_area.x = x
        text_area.y = y
        self.root_group.append(text_area)
        self.text_elements[id] = text_area

    def draw_curved_text(self, id, center_x, center_y, radius, text, color, font, start_angle=90, total_angle=180):
        group = displayio.Group()
        num_chars = len(text)
        angular_spacing = math.radians(total_angle / (num_chars - 1))
        angle = math.radians(start_angle)

        for char in text:
            char_label = label.Label(font, text=char, color=color)
            char_x = center_x + radius * math.cos(angle)
            char_y = center_y - radius * math.sin(angle)
            rotation_angle = math.degrees(angle) - 90
            char_label.x = int(char_x)
            char_label.y = int(char_y)
            char_label.anchor_point = (0.5, 0.5)
            char_label.anchored_position = (char_label.x, char_label.y)
            char_label.rotation = rotation_angle
            group.append(char_label)
            angle += angular_spacing

        self.root_group.append(group)
        self.text_elements[id] = group

    def remove_text(self, id):
        if id in self.text_elements:
            self.root_group.remove(self.text_elements[id])
            del self.text_elements[id]

    def draw_bitmap(self, x, y, bitmap_path):
        bitmap = displayio.OnDiskBitmap(open(bitmap_path, "rb"))
        tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader, x=x, y=y)
        self.root_group.append(tile_grid)

    def clear_screen(self):
        while len(self.root_group) > 0:
            self.root_group.pop()

    def shutdown(self):
        self.display.brightness = 0
        print("Shutting down display and Resetting device.")
        microcontroller.reset()
