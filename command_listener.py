import threading

def start(driver, observer, module_manager, set_running_flag):
    def listen():
        command_map = {}
        modules = module_manager.modules

        # Auto-register commands from any module that defines a `register()` function
        for name, module in modules.items():
            try:
                if hasattr(module, "register"):
                    new_commands = module.register(driver, observer, set_running_flag)
                    command_map.update(new_commands)
                    print(f"[command_listener] Loaded from {name}: {list(new_commands.keys())}")
            except Exception as e:
                print(f"Error loading commands from {name}: {e}")

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