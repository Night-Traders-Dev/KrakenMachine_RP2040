import time
import random
import board
import busio
import displayio
import terminalio
import gc9a01
import microcontroller
from adafruit_display_text import label


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


def main():
    display = GC9A01_Display()
    
    aubergine_text = 0x77216F
    text_color = 0x000000
    seafoam_color = 0x93E9BE
    ubuntu_orange = 0xE95420
    random_color = random.choice([seafoam_color, ubuntu_orange])
    display.fill_background(random_color)
    if random_color == ubuntu_orange:
        text_color = aubergine_text

    display.draw_text("kraken_text", 80, 120, "Kraken Machine", text_color, terminalio.FONT)
    time.sleep(2)

    display.remove_text("kraken_text")
    time.sleep(1)

    display.draw_text("os_text", 90, 100, "vOS RP2040", text_color, terminalio.FONT)    
    display.draw_text("ver_text", 80, 120, "Version 0.0.1", text_color, terminalio.FONT)
    time.sleep(2)

    display.remove_text("os_text")
    display.remove_text("ver_text")
    time.sleep(1)

    if random_color == seafoam_color:
        display.draw_bitmap(70, 50, "/assets/kraken_blue.bmp")
    else:
        display.draw_bitmap(70, 70, "/assets/kraken_ubuntu.bmp")  
    time.sleep(120)

    display.clear_screen()
    display.shutdown()


main()

