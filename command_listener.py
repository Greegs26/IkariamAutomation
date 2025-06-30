import threading

command_map = {}

def rebuild_command_map(modules, driver, observer, set_running_flag):
    global command_map
    command_map = {}

    for name, module in modules.items():
        try:
            if hasattr(module, "register"):
                new_cmds = module.register(driver, observer, set_running_flag)
                command_map.update(new_cmds)
                print(f"[command_listener] Loaded from {name}: {list(new_cmds.keys())}")
        except Exception as e:
            print(f"[command_listener] Error loading commands from {name}: {e}")

    print("\nAvailable commands:")
    for cmd in command_map:
        print(f" - {cmd}")
    print()

def start(driver, observer, module_manager, set_running_flag):
    def listen():
        modules = module_manager.modules
        rebuild_command_map(modules, driver, observer, set_running_flag)

        while True:
            command = input("> ").strip().lower()
            if command in command_map:
                try:
                    threading.Thread(target=command_map[command], daemon=True).start()
                except Exception as e:
                    print(f"Error running '{command}': {e}")
            else:
                print("Unknown command.")
                print("Available commands:")
                for cmd in command_map:
                    print(f" - {cmd}")
                print()
    
    threading.Thread(target=listen, daemon=True).start()