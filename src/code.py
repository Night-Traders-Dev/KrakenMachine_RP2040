import time
import random
from km_lib.display_init import GC9A01_Display
import terminalio
import microcontroller
import gc

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



    free_memory = gc.mem_free()
    allocated_memory = gc.mem_alloc()
    total_memory = free_memory + allocated_memory
    used_memory_percentage = (allocated_memory / total_memory) * 100
    ram_usage = f"Used: {allocated_memory // 1024} KB"
    ram_free = f"Free: {free_memory // 1024} KB"
    ram_total = f"Total: {total_memory // 1024} KB"
    ram_percent = f"Usage: {used_memory_percentage:.2f}%"
    ram_display = f"Ram: {allocated_memory // 1024}/{total_memory // 1024} KB({used_memory_percentage:.2f})%"



    display.draw_text("boot_text", 50, 60, "Booting...", text_color, terminalio.FONT)
    display.draw_text("cpu_text", 50, 80, "Dual-core Arm Cortex-M0+", text_color, terminalio.FONT)
    display.draw_text("ram_usage", 50, 100, ram_usage, text_color, terminalio.FONT)
    display.draw_text("ram_free", 50, 120, ram_free, text_color, terminalio.FONT)
    display.draw_text("ram_total", 50, 140, ram_total, text_color, terminalio.FONT)
    display.draw_text("ram_percent", 50, 160, ram_percent, text_color, terminalio.FONT)
    time.sleep(3)

    display.remove_text("boot_text")
    display.remove_text("cpu_text")
    display.remove_text("ram_usage")
    display.remove_text("ram_free")
    display.remove_text("ram_total")
    display.remove_text("ram_percent")
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
        display.draw_bitmap(70, 25, "/assets/kraken_blue.bmp")
    elif random_color == ubuntu_orange:
        display.draw_bitmap(70, 25, "/assets/kraken_ubuntu.bmp")
    elif random_color == pale_tea:
        display.draw_bitmap(70, 25, "/assets/pale_tea_100x100.bmp")
    else:
        display.draw_bitmap(70, 25, "/assets/revolver_100x100.bmp")

    display.draw_curved_text(
        "curved_text",
        center_x=100,
        center_y=120,
        radius=95,
        text="Kraken",
        color=0x000000,
        font=terminalio.FONT,
        start_angle=120,
        total_angle=95
    )

    reboot_time = 0

    while reboot_time <= 86400:
        uptime = time.monotonic() - start_time
        hours = int(uptime // 3600)
        minutes = int((uptime % 3600) // 60)
        seconds = int(uptime % 60)
        uptime_text = f"Uptime: {hours:02}:{minutes:02}:{seconds:02}"

        cpu_freq0 = microcontroller.cpus[0].frequency / 1_000_000
        cpu_temp0 = microcontroller.cpus[0].temperature
        cpu_freq1 = microcontroller.cpus[1].frequency / 1_000_000
        cpu_temp1 = microcontroller.cpus[1].temperature
        free_memory = gc.mem_free()
        allocated_memory = gc.mem_alloc()
        total_memory = free_memory + allocated_memory
        used_memory_percentage = (allocated_memory / total_memory) * 100


        freq_text0 = f"CPU0/1: {cpu_freq0:.2f}/{cpu_freq1:.2f} MHz"
        temp_text0 = f"Temp0/1: {cpu_temp0:.2f}/{cpu_temp1:.2f} °C"

        display.draw_text("freq_text0", 50, 130, freq_text0, text_color, terminalio.FONT)
        display.draw_text("temp_text0", 50, 150, temp_text0, text_color, terminalio.FONT)
        display.draw_text("ram_disp", 50, 170, ram_display, text_color, terminalio.FONT)
        display.draw_text("uptime_text", 70, 210, uptime_text, text_color, terminalio.FONT)

        time.sleep(1)

        display.remove_text("freq_text0")
        display.remove_text("temp_text0")
        display.remove_text("ram_disp")
        display.remove_text("uptime_text")

        reboot_time += 1

    display.clear_screen()
    display.shutdown()

main()
