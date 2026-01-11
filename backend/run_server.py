#!/usr/bin/env python3
"""Run server and keep it running"""
import time
import subprocess
import sys

print("Starting backend server...")
proc = subprocess.Popen([sys.executable, "main.py"], cwd=r"C:\Users\cheeh\Desktop\webservice ramadan\backend")

# Keep the subprocess running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    proc.terminate()
    proc.wait()
    print("Server stopped")
