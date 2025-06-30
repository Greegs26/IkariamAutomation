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
from threading import Lock

running = True

def set_running_flag(value):
    global running
    running = value

def discover_modules(folder="commands"):
    return [f"{folder}.{f.stem}" for f in Path(folder).glob("*.py") if f.name != "__init__.py"]

# ===== FILE WATCHER CLASS =====
# TODO: Create class to watch for changes in .py files
# Needed for automatic reloading of newer version of currently edited .py files.
class ReloadHandler(FileSystemEventHandler):
    def __init__(self, module_manager, driver, observer, set_running_flag):
        self.module_manager = module_manager
        self.driver = driver
        self.observer = observer
        self.set_running_flag = set_running_flag

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            filename = Path(event.src_path).stem
            print(f"[DEBUG] File changed: {event.src_path}")

            # Match full module name (e.g., commands.close_session)
            module_name = None
            for full_name in self.module_manager.modules:
                if full_name.endswith(filename):
                    module_name = full_name
                    break

            if module_name:
                logging.info(f"[Watcher] Detected change in: {module_name}")
                self.module_manager.reload_module(module_name)
                logging.info(f"[Watcher] Reloaded: {module_name}")

                # Rebuild command map if command_listener has that function
                if "command_listener" in self.module_manager.modules:
                    import command_listener
                    if hasattr(command_listener, "rebuild_command_map"):
                        command_listener.rebuild_command_map(
                            self.module_manager.modules,
                            self.driver,
                            self.observer,
                            self.set_running_flag
                        )

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
                self.modules[name] = importlib.reload(self.modules[name])
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
        logging.info("Automation controller is running...")

        # Just pass the context to command_listener
        command_listener.start(self.driver, self.observer, self.module_manager, set_running_flag)

#from selenium import webdriver
#from selenium.webdriver.firefox.service import Service
#from selenium.webdriver.firefox.options import Options

# OPTIONAL: specify path to geckodriver if not in PATH
# service = Service(executable_path="/path/to/geckodriver")

import getpass

def main():

    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    selenium_lock = Lock() # going to be needed to queue multiple actions in a row
    
    # Prompt for credentials
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")

    # Setup Firefox options
    options = Options()
    options.set_preference("dom.webnotifications.enabled", False)
    options.set_preference("dom.webdriver.enabled", False)

    # Launch browser
    driver = webdriver.Firefox(options=options)
    driver.get("https://ikariam.org")

    # Click the 'Log in' tab
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//li[contains(text(), 'Log in')]"))
    ).click()

    # Fill in login form
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "email"))
    ).send_keys(username)

    driver.find_element(By.NAME, "password").send_keys(password)

    # Click the login button
    driver.find_element(By.XPATH, "//button[contains(text(), 'Log in')]").click()

    original_tab = driver.current_window_handle
    print("[Info] Waiting for you to click a world...")

    # Wait until a new tab opens
    WebDriverWait(driver, 30).until(lambda d: len(d.window_handles) > 1)

    # Find the new tab and switch to it
    for handle in driver.window_handles:
        if handle != original_tab:
            new_tab_handle = handle
            break

    # Switch to the new tab
    driver.switch_to.window(new_tab_handle)
    print("[Info] Switched to new world tab.")

    # Temporarily skipping original tab close
    # Close the original login tab
    # driver.switch_to.window(original_tab)
    # driver.close()
    # print("[Info] Closed original login tab.")

    # Switch back to the new tab
    # driver.switch_to.window(new_tab_handle)

    #### OTHER CODE REQUIRED ####

    # Logging setup
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    # Load modules
    modules_to_watch = ["command_listener"] + discover_modules("commands")
    print("[DEBUG] Modules to watch:", modules_to_watch)
    module_manager = ModuleManager(modules_to_watch)
    module_manager.load_modules()

    # Create observer BEFORE using it
    observer = Observer()

    # Now pass everything to the event handler
    event_handler = ReloadHandler(module_manager, driver, observer, set_running_flag)

    # Setup file watching
    watch_path = Path.cwd() / "commands"
    observer.schedule(event_handler, path=str(Path.cwd()), recursive=False)  # For root-level files like command_listener.py
    observer.schedule(event_handler, path=str(Path.cwd() / "commands"), recursive=False)  # For your dynamic commands
    observer.start()

    # Start controller
    controller = AutomationController(driver, module_manager, observer)
    print("\nScript is running. Type a command:")

    controller.run()

    while running:
        time.sleep(1)