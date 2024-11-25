import terminalio
import usb_cdc
def process_command(command, display):
    """
    Processes a command received over USB.

    Args:
        command: The command string received from the USB terminal.
        display: The GC9A01_Display instance.
    """
    if command == "status":
        # Respond with memory usage
        free_memory = gc.mem_free()
        allocated_memory = gc.mem_alloc()
        total_memory = free_memory + allocated_memory
        used_memory_percentage = (allocated_memory / total_memory) * 100

        response = (
            f"RAM Status:\n"
            f"  Used: {allocated_memory // 1024} KB\n"
            f"  Free: {free_memory // 1024} KB\n"
            f"  Total: {total_memory // 1024} KB\n"
            f"  Usage: {used_memory_percentage:.2f}%\n"
        )
        usb_cdc.data.write(response.encode())

    elif command.startswith("text "):
        # Display custom text
        custom_text = command[5:]  # Extract text after "text "
        display.clear_screen()
        display.draw_text("custom_text", 50, 100, custom_text, 0xFFFFFF, terminalio.FONT)
        usb_cdc.data.write(f"Displayed: {custom_text}\n".encode())

    elif command == "clear":
        # Clear the display
        display.clear_screen()
        usb_cdc.data.write(b"Screen cleared.\n")

    else:
        # Unknown command
        usb_cdc.data.write(b"Unknown command. Try 'status', 'text <message>', or 'clear'.\n")

