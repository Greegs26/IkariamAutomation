def say_hello():
    print("[test_command] Hello from your new command!")

def register(driver, observer, set_running_flag):
    return {
        "hello": say_hello
    }