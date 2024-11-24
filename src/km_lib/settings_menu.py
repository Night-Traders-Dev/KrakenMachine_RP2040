import displayio
from adafruit_display_text import label
import terminalio

class SettingsMenu:
    def __init__(self, display):
        """
        Initializes the settings menu.

        Args:
            display: Instance of the GC9A01_Display class for rendering.
        """
        self.display = display
        self.menu_items = [
            "Brightness",
            "Volume",
            "WiFi",
            "Bluetooth",
            "Back"
        ]
        self.selected_index = 0
        self.menu_group = displayio.Group()

    def show(self):
        """Displays the settings menu."""
        self.display.clear_screen()

        # Create menu items
        y_position = 60
        for i, item in enumerate(self.menu_items):
            color = 0xFFFFFF if i == self.selected_index else 0x888888
            menu_label = label.Label(
                terminalio.FONT,
                text=item,
                color=color,
                x=50,
                y=y_position
            )
            self.menu_group.append(menu_label)
            y_position += 20

        self.display.root_group.append(self.menu_group)

    def update_selection(self, direction):
        """
        Updates the menu selection.

        Args:
            direction: -1 for up, 1 for down.
        """
        self.menu_group.pop()  # Remove the old menu group
        self.selected_index += direction

        # Ensure the selection wraps around
        self.selected_index %= len(self.menu_items)

        # Redisplay the menu
        self.show()

    def clear(self):
        """Clears the menu from the display."""
        self.display.clear_screen()
