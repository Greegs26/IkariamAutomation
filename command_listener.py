import threading
import importlib

def start(driver, observer, module_manager, set_running_flag):
    def listen():
        print("Modules loaded into command_listener:")
        print(list(module_manager.modules.keys()))

        command_map = {}

        # Dynamically load commands from available modules
        modules = module_manager.modules

        # Register known commands
        if "commands.close_session" in modules:
            command_map["quit"] = lambda: modules["commands.close_session"].quit(driver, observer, set_running_flag)

        # Print available commands immediately
        print("\nAvailable commands:")
        for cmd in command_map:
            print(f" - {cmd}")
        print()

        while True:
            command = input("> ").strip().lower()
            if command in command_map:
                try:
                    command_map[command]()
                except Exception as e:
                    print(f"Error running '{command}': {e}")
            else:
                print("Unknown command.")
                print("Available commands:")
                for cmd in command_map:
                    print(f" - {cmd}")
                print()

    threading.Thread(target=listen, daemon=True).start()