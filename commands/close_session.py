import sys

def quit(driver, observer, set_running_flag):
    print("[close_session] Shutting down...")
    driver.quit()
    observer.stop()
    observer.join()
    set_running_flag(False)
    sys.exit(0)

def register(driver, observer, set_running_flag, selenium_lock):
    return {
        "quit": lambda: quit(driver, observer, set_running_flag)
    }