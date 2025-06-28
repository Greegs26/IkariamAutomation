import sys

def quit(driver, observer, set_running_flag):
    print("\n[quit] Shutting down browser and exiting...")

    try:
        driver.quit()
    except Exception as e:
        print(f"Error closing browser: {e}")

    try:
        observer.stop()
        observer.join()
    except Exception as e:
        print(f"Error stopping file watcher: {e}")

    set_running_flag(False)
    print("Exited cleanly.")
    sys.exit(0)