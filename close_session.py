import sys

def graceful_shutdown(driver, observer, set_running_flag):
    print("\n[close_session] Shutting down session...")
    try:
        driver.quit()
    except Exception as e:
        print(f"Error while closing browser: {e}")

    try:
        observer.stop()
        observer.join()
    except Exception as e:
        print(f"Error while stopping observer: {e}")

    set_running_flag(False)
    print("Program exited cleanly.")
    sys.exit(0)