#!/usr/bin/python3

import os
import platform

while True:

    print("\n===== SYSTEM INFO =====")

    print("\nKernel Version:")
    print(platform.release())

    print("\nCPU Info:")
    os.system("cat /proc/cpuinfo | grep Model")

    print("\nMemory:")
    os.system("free -h")

    print("\nDisk:")
    os.system("df -h")

    print("\nIP Address:")
    os.system("ip addr show wlan0")

    input("\nPress Enter to refresh...")
