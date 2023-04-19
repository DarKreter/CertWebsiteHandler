#!/usr/bin/python3
import utils

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from glob import glob
import sys
import os, platform

from time import sleep

currentPath = os.getcwd() + "/"
downloadPath = currentPath + "PDF/"
# Jesli nie ma katalogu PDF tworzy go i sprawdza ile tam jest plikow jesli istnial
howManyFilesInPDFdir = utils.PDF_dir_create(currentPath)

# pobieram z pliku txt pasy do logowania
if platform.system() == "Windows":
    contents = utils.get_last_n_lines("../strona.txt", 2)
elif platform.system() == "Linux":
    contents = utils.get_last_n_lines("../strona.txt", 3)
login = contents[0]
password = contents[1]

ListOfXML = glob("*.xml")
# if len(sys.argv) != 1:
#     ListOfXML = sys.argv
#     ListOfXML.pop(0)
# else:
#     ListOfXML = glob.glob("*.xml")

if len(ListOfXML) == 0:
    input("\033[31m BRAK PLIKOW! \033[0m")
    exit()

ListOfXML.sort()

driver = utils.FirefoxDriver(downloadPath)
# Get on the page
driver.get("https://rejestrcheb.mrit.gov.pl/")

# sign in
driver.find_element_by_id('sign-in').click()
driver.find_element_by_id('_58_login').send_keys(login)
driver.find_element_by_id('_58_password').send_keys(password)
driver.find_element_by_xpath("//input[@value='Sign In']").click()
#driver.find_element_by_xpath("//input[@value='Zaloguj']").click()

# Get to adding cert page
driver.get("https://rejestrcheb.mrit.gov.pl/wykaz-swiadectw-charakterystyki-energetycznej-czesci-budynku")
driver.find_element_by_id(
    "ox_bgk-sr_SwiadectwoEnergetyczneCzesciBudynku2__CRUD___new").click()

sww = False  # something went wrong
emergencyList = ""  # tutaj wpisze pliki ktore jeszcze trzeba zrobic jakby cos

# loop for all certs
for file in ListOfXML:

    print("Now making file: ", end='')
    print(file)

    try:
        # Click import XML cert
        element = WebDriverWait(driver, 15).until(EC.presence_of_element_located(
            (By.ID, "ox_bgk-sr_SwiadectwoEnergetyczneCzesciBudynku2__SwiadectwoEnergetyczneCzesciBudynku___importXML")))
        driver.find_element_by_id(
            "ox_bgk-sr_SwiadectwoEnergetyczneCzesciBudynku2__SwiadectwoEnergetyczneCzesciBudynku___importXML").click()

        # input xml file
        element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='xmlFile']")))
        driver.find_element_by_xpath(
            "//input[@name='xmlFile']").send_keys(currentPath + file)

        # Click import cert
        element = WebDriverWait(driver, 15).until(EC.presence_of_element_located(
            (By.ID, "ox_bgk-sr_SwiadectwoEnergetyczneCzesciBudynku2__ImportSwiadectwo___importSwiadectwo")))
        driver.find_element_by_id(
            "ox_bgk-sr_SwiadectwoEnergetyczneCzesciBudynku2__ImportSwiadectwo___importSwiadectwo").click()

        # click on confirm button
        element = WebDriverWait(driver, 15).until(EC.presence_of_element_located(
            (By.ID, "ox_bgk-sr_SwiadectwoEnergetyczneCzesciBudynku2__SwiadectwoEnergetyczneCzesciBudynku___approve")))
        lol = driver.find_element_by_id(
            "ox_bgk-sr_SwiadectwoEnergetyczneCzesciBudynku2__SwiadectwoEnergetyczneCzesciBudynku___approve")
        lol.send_keys(Keys.ENTER)
        # and confirm popup prompt
        alert_obj = driver.switch_to.alert
        alert_obj.accept()

        # Download PDF
        # FINAL:
        element = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
            (By.ID, "ox_bgk-sr_SwiadectwoEnergetyczneCzesciBudynku2__SwiadectwoEnergetyczneCzesciBudynku___pdf")))
        lol = driver.find_element_by_id(
            "ox_bgk-sr_SwiadectwoEnergetyczneCzesciBudynku2__SwiadectwoEnergetyczneCzesciBudynku___pdf")
        # ROBOCZE:
        # element = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
        #     (By.ID, "ox_bgk-sr_SwiadectwoEnergetyczneCzesciBudynku2__SwiadectwoEnergetyczneCzesciBudynku___pdf_roboczy")))
        # lol = driver.find_element_by_id(
        #     "ox_bgk-sr_SwiadectwoEnergetyczneCzesciBudynku2__SwiadectwoEnergetyczneCzesciBudynku___pdf_roboczy")
        lol.send_keys(Keys.ENTER)
    except:
        emergencyList = emergencyList + " " + file
        continue

    # sprawdzamy czy po zapisaniu pliku jest o jeden wiecej plik niz przy poprzednim sprawdzeniu
    fileDownloadedSuccesfuly = utils.WaitUntilDownloaded(downloadPath,
                                                         howManyFilesInPDFdir, 15)
    if not fileDownloadedSuccesfuly:
        emergencyList = emergencyList + " " + file
        print("File not downloaded!!!")
        continue

    howManyFilesInPDFdir = howManyFilesInPDFdir + 1

    sleep(2)  # Make sure its downloaded
    # dodajemy do nazwy pdf'a co trzeba
    # * means all if need specific format then *.csv
    list_of_files = glob(downloadPath + "*.pdf")
    latest_file = max(list_of_files, key=os.path.getctime)
    newName = latest_file[:(len(latest_file) - 4)] + \
        "_" + file[: (len(file) - 4)] + ".pdf"
    os.rename(latest_file, newName)


driver.close()

if sww:
    print("\033[31m ERROR! \033[0m")
    print(emergencyList)
    sleep(2)
else:
    print("\033[32m SUCCESS! \033[0m")
