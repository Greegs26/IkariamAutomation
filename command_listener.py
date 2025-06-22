def start_command_listener(drivers):
    print("\nType a command (e.g., 'quit'):")
    while True:
        cmd = input(">>> ").strip().lower()
        if cmd == "quit":
            print("Exiting and closing all drivers...")
            for d in drivers.values():
                d.quit()
            break
        elif cmd == "help":
            print("Available commands: quit, help")
        else:
            print(f"Unknown command: {cmd}")