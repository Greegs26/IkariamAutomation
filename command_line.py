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

running = True

def set_running_flag(value):
    global running
    running = value

# ===== FILE WATCHER CLASS =====
# TODO: Create class to watch for changes in .py files
# Needed for automatic reloading of newer version of currently edited .py files.
class ReloadHandler(FileSystemEventHandler):
    def __init__(self, module_manager):
        self.module_manager = module_manager

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            filename = Path(event.src_path).stem  # Extracts filename without extension
            logging.info(f"Detected change in: {filename}")
            self.module_manager.reload_module(filename)

# ===== MODULE MANAGER CLASS =====
# TODO: Create class to load/reload modules and manage functions
class ModuleManager:
    def __init__(self, module_names):
        self.module_names = module_names
        self.modules = {}

    def load_modules(self):
        for name in self.module_names:
            self.modules[name] = importlib.import_module(name)
            logging.info(f"Loaded module: {name}")

    def reload_all_modules(self):
        for name in self.modules:
            try:
                importlib.reload(self.modules[name])
                logging.info(f"Reloaded module: {name}")
            except Exception as e:
                logging.error(f"Failed to reload {name}: {e}")
                
    def reload_module(self, name):
        if name in self.modules:
            try:
                importlib.reload(self.modules[name])
                logging.info(f"Reloaded module: {name}")
            except Exception as e:
                logging.error(f"Failed to reload {name}: {e}")
        else:
            logging.warning(f"Module {name} not managed, skipping reload.")

# ===== MAIN CONTROLLER CLASS =====
# TODO: Create main controller that runs the automation
class AutomationController:
    def __init__(self, driver, module_manager, observer):
        self.driver = driver
        self.module_manager = module_manager
        self.observer = observer

    def run(self):
        import command_listener
        import close_session

        logging.info("Automation controller is running...")

        command_map = {
            "quit": lambda: close_session.quit(self.driver, self.observer, set_running_flag),
        }

        print("\nAvailable commands:")
        for cmd in command_map:
            print(f" - {cmd}")

        command_listener.start(command_map)

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

# OPTIONAL: specify path to geckodriver if not in PATH
# service = Service(executable_path="/path/to/geckodriver")

# Setup Firefox options
options = Options()
options.set_preference("dom.webnotifications.enabled", False)  # Disable popups
options.set_preference("dom.webdriver.enabled", False) # Hides navigator.webdriver

# Launch dirver
print(f"\nLaunching session...")
driver = webdriver.Firefox(options=options)
driver.get("https://ikariam.org")
print(f"Session is ready.")

# ===== CONFIGURATION =====
# TODO: Define what modules to load and what functions to run
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

modules_to_watch = ["command_listener"]  # Add other modules here

module_manager = ModuleManager(modules_to_watch)
module_manager.load_modules()

event_handler = ReloadHandler(module_manager)
observer = Observer()
observer.schedule(event_handler, path=str(Path.cwd()), recursive=False)
observer.start()

controller = AutomationController(driver, module_manager, observer)

print("\nScript is running. Type 'help' for commands.")
controller.run()

# Keep the main loop alive until 'quit' sets running = False
while running:
    time.sleep(1)