# Kraken Machine for RP2040

The **Kraken Machine** is a simple yet engaging project designed for the RP2040 microcontroller, utilizing a GC9A01 round display. This project showcases how to display text and images on the screen, create dynamic backgrounds, and manage screen transitions. It's an excellent starting point for anyone interested in embedded systems and display management with CircuitPython.

## Table of Contents

- [Features](#features)
- [Hardware Requirements](#hardware-requirements)
- [Software Requirements](#software-requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Code Explanation](#code-explanation)
- [Customization](#customization)
- [License](#license)

## Features

- Displays dynamic background colors.
- Shows custom text messages.
- Loads and displays bitmap images.
- Implements smooth screen transitions.
- Demonstrates power management by shutting down the display and resetting the device.

## Hardware Requirements

- [RP2040-based microcontroller](https://www.raspberrypi.org/products/raspberry-pi-pico/)
- [GC9A01 1.28" Round LCD Display](https://www.waveshare.com/1.28inch-lcd-module.htm)
- USB cable for programming and power.
- Optional: Battery pack if portable operation is desired.

## Software Requirements

- [CircuitPython](https://circuitpython.org/) compatible with the RP2040.
- Required CircuitPython libraries:
  - `adafruit_display_text`
  - `adafruit_bitmap_font` (if custom fonts are used)
  - `gc9a01` driver for the display
- Python 3.x for code editing and uploading.

## Installation

1. **Install CircuitPython on the RP2040:**

   - Download the latest UF2 file for the RP2040 from the [CircuitPython downloads page](https://circuitpython.org/board/raspberry_pi_pico/).
   - Connect the RP2040 to your computer while holding the BOOTSEL button to enter bootloader mode.
   - Drag and drop the UF2 file onto the `RPI-RP2` drive that appears.

2. **Install the Required Libraries:**

   - Download the latest CircuitPython library bundle from the [CircuitPython Libraries](https://circuitpython.org/libraries).
   - Unzip the library bundle.
   - Copy the following libraries from the `lib` folder to the `lib` directory on the RP2040's CIRCUITPY drive:
     - `adafruit_display_text`
     - `adafruit_bitmap_font` (if using custom fonts)
     - `gc9a01.mpy` (might be in `drivers` or need to be added separately)

3. **Copy the Code and Assets:**

   - Create a new file named `code.py` on the CIRCUITPY drive.
   - Paste the Kraken Machine code into `code.py`.
   - Create an `assets` folder on the CIRCUITPY drive.
   - Copy the required bitmap images (`kraken_blue.bmp`, `kraken_ubuntu.bmp`) into the `assets` folder.

4. **Wiring the Hardware:**

   - Connect the GC9A01 display to the RP2040 according to the following pin mapping:

     | Display Pin | RP2040 Pin |
     |-------------|------------|
     | VCC         | 3.3V       |
     | GND         | GND        |
     | SCL (CLK)   | GP10       |
     | SDA (MOSI)  | GP11       |
     | RES (Reset) | GP12       |
     | DC          | GP8        |
     | CS          | GP9        |
     | BL (Backlight) | GP25    |

## Usage

1. **Power Up:**

   - Connect the RP2040 to a power source via USB or battery.

2. **Running the Program:**

   - The code will execute automatically upon power-up.
   - It will display a random background color (seafoam or Ubuntu orange).
   - The text "Kraken Machine" will appear in black or aubergine, depending on the background.
   - After a brief pause, the screen transitions to display the operating system name and version.
   - Finally, a Kraken image is displayed.
   - The program runs for 2 minutes before clearing the screen and resetting the device.

## Code Explanation

- **Imports:**

  - Essential libraries for controlling the display, handling time, and managing hardware components are imported.

- **`GC9A01_Display` Class:**

  - Manages all display-related functions, including initializing the display, drawing text, loading bitmaps, and handling screen transitions.

- **Main Function:**

  - Initializes the display.
  - Randomly selects a background color and adjusts text color accordingly.
  - Displays initial text messages with pauses in between.
  - Loads and displays the appropriate Kraken image based on the background color.
  - Waits for a specified duration before shutting down.

- **Shutdown Procedure:**

  - Clears the screen and resets the microcontroller to prepare for the next cycle.

## Customization

- **Changing Text Messages:**

  - Modify the text strings in the `draw_text` method calls within the `main()` function to display custom messages.

- **Adjusting Display Duration:**

  - Modify the `time.sleep()` values to change how long each screen is displayed.

- **Adding More Images:**

  - Place additional bitmap images in the `assets` folder.
  - Use the `draw_bitmap` method to display them.

- **Changing Colors:**

  - Adjust the color variables (`seafoam_color`, `ubuntu_orange`, `aubergine_text`, etc.) to use different colors.

- **Extending Functionality:**

  - Implement additional methods in the `GC9A01_Display` class for more advanced graphics.
  - Incorporate user inputs or sensors to interact with the display dynamically.

## License

This project is open-source and available under the MIT License. Feel free to modify and distribute the code as per the license terms.
