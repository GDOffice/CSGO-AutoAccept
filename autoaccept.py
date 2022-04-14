#!/usr/bin/env python3


#### Configuration ####


CONFIG = {

    # PNG image of the accept button
    "screenshot_path":  "button_screenshots/1920x1200.png",
    
    # How many seconds to wait between each scan
    "scan_wait_time":   1,
    
    # How many times to push the accept button after it has been detected
    "push_times":       2,
    
    # Seconds to wait between pushing the accept button
    "push_wait_time":   1,
    
    # Start scanning for the accept button after this many seconds
    "initial_wait_time": 5,

    # Stop scanning if we couldn't find the button after a large number of tries
    "limit_scan_times": 1000

}


#### End of Configuration Section ####


from time import sleep, ctime
import pyautogui
import os

__version__ = "0.0.1"
__author__ = "kropfm"


def pushButton(btn):
    pyautogui.click(btn)


def pushButtonMultipleTimes(button, times, wait):
    for n in range(times):
        if n != times-1:
            print(
                "[{}/{}] Pushing accept button. Pushing again in {}s.".format(n+1, times, wait))
            pushButton(button)
            sleep(wait)
        else:
            pushButton(button)
            print("[{}/{}] Pushing accept button.".format(n+1, times))


def locateButton(wait) -> pyautogui.Point:
    """Loops until the accept button was found,
       or quits if iteration limit exceeded."""
    iteration = 0
    #while iteration < CONFIG["limit_scan_times"]:
    for i in range(CONFIG["limit_scan_times"]):
        #print("{}/{}".format(i, CONFIG["limit_scan_times"]))
        try:
            print("[{}] Looking for accept button...".format(i))
            button = pyautogui.locateCenterOnScreen(CONFIG["screenshot_path"])
            assert button is not None
        except Exception:
            print(" Didn't find accept button on screen. Scanning again in {} seconds.".format(wait))
            sleep(wait)
        else:
            print("=> Found accept button: {}".format(button))
            return button

    print("[!] Timed out after {} tries. Exiting.".format(i))
    exit()


def main():
    print("[{}] Welcome to Gold Diggers AutoAccept for CS:GO!".format(ctime()))
    if os.path.isfile(CONFIG["screenshot_path"]):
        print("Screenshot file exists:", CONFIG["screenshot_path"])
        print("Starting in {} seconds. Press Ctrl+C to stop.".format(CONFIG["initial_wait_time"]))
        sleep(CONFIG["initial_wait_time"])
        pushButtonMultipleTimes(locateButton(CONFIG["scan_wait_time"]),
                                CONFIG["push_times"],
                                CONFIG["push_wait_time"]
        )
        print("[{}] Exiting.".format(ctime()))
    else:
        print("[!] Couldn't load screenshot file. Exiting.")
        exit()



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
