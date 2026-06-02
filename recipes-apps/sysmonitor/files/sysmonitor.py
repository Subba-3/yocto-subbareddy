#!/usr/bin/python3

import os
import time

VERSION = "1.0"

def get_cpu_usage():
    with open("/proc/stat") as f:
        line = f.readline()
    fields = list(map(int, line.strip().split()[1:]))
    idle = fields[3]
    total = sum(fields)
    return idle, total

def get_memory():
    mem = {}
    with open("/proc/meminfo") as f:
        for line in f:
            parts = line.split()
            mem[parts[0].rstrip(":")] = int(parts[1])
    total = mem["MemTotal"]
    available = mem["MemAvailable"]
    used = total - available
    percent = (used / total) * 100
    return total // 1024, used // 1024, percent

def get_temperature():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp") as f:
            temp = int(f.read().strip()) / 1000
        return round(temp, 1)
    except Exception:
        return "N/A"

def get_uptime():
    with open("/proc/uptime") as f:
        seconds = float(f.readline().split()[0])
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours}h {minutes}m {secs}s"

def get_cpu_percent(prev_idle, prev_total):
    idle, total = get_cpu_usage()
    diff_idle = idle - prev_idle
    diff_total = total - prev_total
    if diff_total == 0:
        return 0.0, idle, total
    percent = (1 - diff_idle / diff_total) * 100
    return round(percent, 1), idle, total

def draw_bar(percent, width=20):
    if isinstance(percent, str):
        return "[" + "?" * width + "]"
    filled = int((percent / 100) * width)
    empty = width - filled
    return "[" + "█" * filled + "░" * empty + "]"

def clear():
    os.system("clear")

# ── Main ──────────────────────────────────────────

print("Starting CPU/Memory Monitor...")
print("Press Ctrl+C to exit")
time.sleep(1)

prev_idle, prev_total = get_cpu_usage()
time.sleep(1)

try:
    while True:
        clear()

        cpu_percent, prev_idle, prev_total = get_cpu_percent(prev_idle, prev_total)
        mem_total, mem_used, mem_percent = get_memory()
        temp = get_temperature()
        uptime = get_uptime()

        print("=================================")
        print(f"   SUBBU OS - System Monitor v{VERSION}")
        print("=================================")
        print()

        print(f"  CPU Usage   : {draw_bar(cpu_percent)} {cpu_percent}%")
        print()

        print(f"  Memory      : {draw_bar(mem_percent)} {mem_percent:.1f}%")
        print(f"  Used        : {mem_used} MB / {mem_total} MB")
        print()

        print(f"  Temperature : {temp}°C")
        print()

        print(f"  Uptime      : {uptime}")
        print()

        print("=================================")
        print("  Refreshing every 1 second...")
        print("  Press Ctrl+C to exit")
        print("=================================")

        time.sleep(1)

except KeyboardInterrupt:
    clear()
    print("Monitor stopped. Bye!")
