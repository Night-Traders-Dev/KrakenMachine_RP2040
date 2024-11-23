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
    text_white = 0xffffff
    text_color = 0x000000
    seafoam_color = 0x93E9BE
    ubuntu_orange = 0xE95420
    revolver_purple = 0x402141
    pale_tea = 0xc1eabe

    random_color = random.choice([seafoam_color, ubuntu_orange, revolver_purple, pale_tea])
    display.fill_background(random_color)
    if random_color == ubuntu_orange:
        text_color = aubergine_text
    elif random_color == revolver_purple:
        text_color = text_white
    else:
        text_color = text_color

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
    elif random_color == ubuntu_orange:
        display.draw_bitmap(70, 70, "/assets/kraken_ubuntu.bmp")
    elif random_color == pale_tea:
        display.draw_bitmap(70, 70, "/assets/pale_tea_100x100.bmp")
    else:
        display.draw_bitmap(70, 70, "/assets/revolver_100x100.bmp")

    reboot_time = 0
    text_color = 0x000000  # Black text color

    while reboot_time <= 120:
        cpu_freq = microcontroller.cpu.frequency / 1_000_000  # Convert to MHz
        cpu_temp = microcontroller.cpu.temperature

        freq_text = f"Freq: {cpu_freq:.2f} MHz"
        temp_text = f"Temp: {cpu_temp:.2f} °C"

        display.draw_text("freq_text", 70, 180, freq_text, text_color, terminalio.FONT)
        display.draw_text("temp_text", 70, 200, temp_text, text_color, terminalio.FONT)

        time.sleep(1)

        display.remove_text("freq_text")
        display.remove_text("temp_text")

        reboot_time += 1



    display.clear_screen()
    display.shutdown()


main()


