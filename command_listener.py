import threading
import importlib

def start(driver, observer, module_manager, set_running_flag):
    def listen():
        print("Type a command (type 'help' for available commands):")

        command_map = {}

        # Dynamically load commands (from files like close_session.py, collect_resources.py, etc.)
        modules = module_manager.modules

        # Check if close_session is loaded and register 'quit'
        if "close_session" in modules:
            command_map["quit"] = lambda: modules["close_session"].quit(driver, observer, set_running_flag)

        # Add a help command
        command_map["help"] = lambda: print("Available commands:\n" + "\n".join(f" - {cmd}" for cmd in command_map))

        while True:
            command = input("> ").strip().lower()
            if command in command_map:
                try:
                    command_map[command]()
                except Exception as e:
                    print(f"Error running '{command}': {e}")
            else:
                print("Unknown command. Type 'help' to see available commands.")

    threading.Thread(target=listen, daemon=True).start()