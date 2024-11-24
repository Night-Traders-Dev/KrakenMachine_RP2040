import time
import random
import math

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

    def draw_curved_text(self, id, center_x, center_y, radius, text, color, font, start_angle=90, total_angle=180):
        """
        Draw text along a curved path with rotated letters.

        Args:
            id: Identifier for the text group.
            center_x, center_y: Center of the curve.
            radius: Radius of the curve.
            text: The string to display.
            color: Color of the text.
            font: Font used for the text.
            start_angle: Starting angle in degrees (default is 90 for top-left).
            total_angle: Total angular span for the text in degrees.
        """
        group = displayio.Group()
    
        # Calculate angular spacing based on total_angle and text length
        num_chars = len(text)
        angular_spacing = math.radians(total_angle / (num_chars - 1))
    
        # Start angle in radians
        angle = math.radians(start_angle)

        for char in text:
            # Create a label for each character
            char_label = label.Label(font, text=char, color=color)
        
            # Calculate character position
            char_x = center_x + radius * math.cos(angle)
            char_y = center_y - radius * math.sin(angle)
        
            # Calculate rotation angle (tangent to curve)
            rotation_angle = math.degrees(angle) - 90  # Adjust for readability
        
            # Set position and anchor
            char_label.x = int(char_x)
            char_label.y = int(char_y)
            char_label.anchor_point = (0.5, 0.5)
            char_label.anchored_position = (char_label.x, char_label.y)
        
            # Apply rotation
            char_label.rotation = rotation_angle  # Rotates the character
        
            # Add to group
            group.append(char_label)
        
            # Increment angle for next character
            angle += angular_spacing

        # Add to root group
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


def main():
    display = GC9A01_Display()

    aubergine_text = 0x77216F
    text_white = 0xffffff
    text_color = 0x000000
    seafoam_color = 0x93E9BE
    ubuntu_orange = 0xE95420
    revolver_purple = 0x402141
    pale_tea = 0xc1eabe

    start_time = time.monotonic()
    uptime = 0


    random_color = random.choice([seafoam_color, ubuntu_orange, revolver_purple, pale_tea])
    display.fill_background(random_color)
    if random_color == ubuntu_orange:
        text_color = aubergine_text
    elif random_color == revolver_purple:
        text_color = text_white
    else:
        text_color = text_color

    display.draw_text("boot_text", 50, 60, "Booting...", text_color, terminalio.FONT)
    display.draw_text("cpu_text", 50, 80, "Dual-core Arm Cortex-M0+", text_color, terminalio.FONT)
    display.draw_text("mem_text", 50, 100, "264kB on-chip SRAM", text_color, terminalio.FONT)
    time.sleep(3)


    display.remove_text("boot_text")
    display.remove_text("cpu_text")
    display.remove_text("mem_text")
    time.sleep(1)

    display.draw_text("kraken_text", 60, 60, "Kraken Machine", text_color, terminalio.FONT)
    time.sleep(1)

    display.draw_text("os_text", 60, 80, "vOS RP2040", text_color, terminalio.FONT)    
    display.draw_text("ver_text", 60, 100, "Version 0.0.1", text_color, terminalio.FONT)
    time.sleep(2)

    display.remove_text("kraken_text")
    display.remove_text("os_text")
    display.remove_text("ver_text")


    if random_color == seafoam_color:
        display.draw_bitmap(70, 30, "/assets/kraken_blue.bmp")
    elif random_color == ubuntu_orange:
        display.draw_bitmap(70, 30, "/assets/kraken_ubuntu.bmp")
    elif random_color == pale_tea:
        display.draw_bitmap(70, 30, "/assets/pale_tea_100x100.bmp")
    else:
        display.draw_bitmap(70, 30, "/assets/revolver_100x100.bmp")

    display.draw_curved_text(
        "curved_text",
        center_x=100,          # Shift the curve's center to the left
        center_y=120,          # Vertically center the curve
        radius=95,             # Adjust radius for curvature
        text="Kraken",         # Text to display
        color=0x000000,        # Text color
        font=terminalio.FONT,  # Font
        start_angle=120,       # Start at left-hand side
        total_angle=95        # Span 120 degrees
    )

    reboot_time = 0

    while reboot_time <= 600:
        uptime = time.monotonic() - start_time  # Elapsed time since start
        hours = int(uptime // 3600)
        minutes = int((uptime % 3600) // 60)
        seconds = int(uptime % 60)
    
        # Format uptime string
        uptime_text = f"Uptime: {hours:02}:{minutes:02}:{seconds:02}"
        cpu_freq0 = microcontroller.cpus[0].frequency / 1_000_000
        cpu_temp0 = microcontroller.cpus[0].temperature
        cpu_freq1 = microcontroller.cpus[1].frequency / 1_000_000
        cpu_temp1 = microcontroller.cpus[1].temperature

        freq_text0 = f"CPU0: {cpu_freq0:.2f} MHz"
        temp_text0 = f"Temp0: {cpu_temp0:.2f} °C"
        freq_text1 = f"CPU1: {cpu_freq1:.2f} MHz"
        temp_text1 = f"Temp1: {cpu_temp1:.2f} °C"

        display.draw_text("freq_text0", 70, 140, freq_text0, text_color, terminalio.FONT)
        display.draw_text("temp_text0", 70, 160, temp_text0, text_color, terminalio.FONT)
        display.draw_text("freq_text1", 70, 180, freq_text1, text_color, terminalio.FONT)
        display.draw_text("temp_text1", 70, 200, temp_text1, text_color, terminalio.FONT)
        display.draw_text("uptime_text", 70, 220, uptime_text, text_color, terminalio.FONT)

        time.sleep(1)

        display.remove_text("freq_text0")
        display.remove_text("temp_text0")
        display.remove_text("freq_text1")
        display.remove_text("temp_text1")
        display.remove_text("uptime_text")

        reboot_time += 1



    display.clear_screen()
    display.shutdown()


main()


