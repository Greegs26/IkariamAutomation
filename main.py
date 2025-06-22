"""
Main program for game automation with hot-reloadable modules
"""

# ===== IMPORTS =====
import time
import importlib # Built-in module for loading/reloading other Python files
import sys
import os
import logging # Better than just print()
from pathlib import Path # Modern way to work with file paths
from watchdog.observers import Observer # Third-party library that watches for file changes (like when you save a .py file)
from watchdog.events import FileSystemEventHandler

from command_listener import start_command_listener

# ===== LOGGING SETUP =====
# TODO: Set up logging configuration
# Needed for automatic reloading of newer version of currently edited .py files.

# ===== FILE WATCHER CLASS =====
# TODO: Create class to watch for changes in .py files
# Needed for automatic reloading of newer version of currently edited .py files.

# ===== MODULE MANAGER CLASS =====
# TODO: Create class to load/reload modules and manage functions

# ===== MAIN CONTROLLER CLASS =====
# TODO: Create main controller that runs the automation

# ===== CONFIGURATION =====
# TODO: Define what modules to load and what functions to run

# ===== MAIN EXECUTION =====
# TODO: Create main() function to start everything

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

# OPTIONAL: specify path to geckodriver if not in PATH
# service = Service(executable_path="/path/to/geckodriver")

# Setup Firefox options
options = Options()
options.set_preference("dom.webnotifications.enabled", False)  # Disable popups
options.set_preference("dom.webdriver.enabled", False) # Hides navigator.webdriver

# Ask user how many drivers to open
try:
    num_sessions = int(input("How many browser sessions would you like to open? (1 to 6): ").strip())
    if not (1 <= num_sessions <= 6):
        raise ValueError
except ValueError:
    print("Invalid input. Defaulting to 1 session.")
    num_sessions = 1

# Launch only the requested number of drivers
drivers = {}

for i in range(1, num_sessions + 1):
    print(f"\nLaunching session {i}...")
    driver = webdriver.Firefox(options=options)
    driver.get("https://ikariam.org")

    drivers[str(i)] = driver
    print(f"Session {i} is ready.")

start_command_listener(drivers)
