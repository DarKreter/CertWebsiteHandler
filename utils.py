import os
from glob import glob
from selenium import webdriver
from time import time, sleep


# HowManyFilesinDirectiory
def WaitUntilDownloaded(downloadPath, hmFinDir, timeout, period=0.25):
    mustend = time() + timeout
    while time() < mustend:
        if (hmFinDir + 1) == len(glob(downloadPath + "*.pdf")):
            return True
        sleep(period)
    return False


def PDF_dir_create(path):
    hmfiPDFd = 0
    # Check is PDF dir exists
    if os.path.isdir(path + "PDF") == False:
        os.mkdir(path + "PDF")  # Create it if neccessary
    else:
        hmfiPDFd = len(glob("PDF/*.pdf"))

    return hmfiPDFd


def get_last_n_lines(file_name, N):
    list_of_lines = []
    with open(file_name, 'rb') as read_obj:
        read_obj.seek(0, os.SEEK_END)
        buffer = bytearray()
        pointer_location = read_obj.tell()
        while pointer_location >= 0:
            read_obj.seek(pointer_location)
            pointer_location = pointer_location - 1
            new_byte = read_obj.read(1)
            if new_byte == b'\n':
                list_of_lines.append(buffer.decode()[::-1])
                if len(list_of_lines) == N:
                    return list(reversed(list_of_lines))
                buffer = bytearray()
            else:
                buffer.extend(new_byte)

        if len(buffer) > 0:
            list_of_lines.append(buffer.decode()[::-1])

    return list(reversed(list_of_lines))


def FirefoxDriver(downloadPath):
    # Setup autodownload pdfs
    firefoxProfile = webdriver.FirefoxProfile()
    firefoxProfile.set_preference("browser.download.folderList", 2)
    firefoxProfile.set_preference(
        "browser.download.manager.showWhenStarting", False)
    firefoxProfile.set_preference("browser.download.dir", downloadPath)
    firefoxProfile.set_preference(
        "browser.helperApps.neverAsk.saveToDisk", "application/pdf")
    firefoxProfile.set_preference("pdfjs.disabled", True)

    return webdriver.Firefox(firefoxProfile)
