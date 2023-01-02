import glob, os
import glob
import os
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#funkcja czekajaca az sie sprawdzi warunek albo uplynie czas
def WaitUntilDownloaded(hmFinDir, timeout, period=0.25):         #HowManyFilesinDirectiory
  mustend = time.time() + timeout
  while time.time() < mustend:
    if (hmFinDir + 1) == len(glob.glob("PDF\\*.pdf")): return True
    time.sleep(period)
  return False

#funkcja ktora pomoze mi pobrac pasy z pliku
def get_last_n_lines(file_name, N):
    list_of_lines = []
    with open(file_name, 'rb') as read_obj:
        read_obj.seek(0, os.SEEK_END)
        buffer = bytearray()
        pointer_location = read_obj.tell()
        while pointer_location >= 0:
            read_obj.seek(pointer_location)
            pointer_location = pointer_location -1
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

#Jesli nie ma katalogu PDF tworzy go i sprawdza ile tam jest plikow jesli istnial
howManyFilesInPDFdir = 0
currentPath = os.getcwd() + "\\"
if os.path.isdir(currentPath + "PDF") == False:
    os.mkdir(currentPath + "PDF")
else:
    howManyFilesInPDFdir = len(glob.glob("PDF\\*.pdf"))

#pobieram z pliku txt pasy do logowania
contents = get_last_n_lines("../strona.txt",2)
login = contents[0]
password = contents[1]

downloadPath = currentPath + "PDF\\"

if len(sys.argv) != 1:
    ListOfXML = sys.argv
    ListOfXML.pop(0)
else:
    ListOfXML = glob.glob("*.xml")

#print("----------------------------------")
#print(ListOfXML)
#print("----------------------------------")
#time.sleep(10)

if len(ListOfXML) == 0:
    input("BRAK PLIKOW")
    exit()


#Konfiguruje Chrome, miedzy innymi po to, zeby pobieral pdfy
chrome_options = webdriver.ChromeOptions()
prefs = {
"download.default_directory": downloadPath, #Change default directory for downloads
"download.prompt_for_download": False, #To auto download the file
"download.directory_upgrade": True,
"plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
}
chrome_options.add_experimental_option('prefs', prefs)
CHROMEDRIVER_PATH = './chromedriver'
driver = webdriver.Chrome(options=chrome_options, executable_path=CHROMEDRIVER_PATH)
driver.set_page_load_timeout(20)
driver.maximize_window()

#Wchodze na strone
driver.get("https://rejestrcheb.mrit.gov.pl/")

#po kolei klikam
try:
    element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "sign-in")))
finally:
    driver.find_element_by_id('sign-in').click()

#logowanie
try:
    element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "_58_login")))
finally:
    driver.find_element_by_id('_58_login').send_keys(login)
    driver.find_element_by_id('_58_password').send_keys(password)
    driver.find_element_by_xpath("//input[@value='Zaloguj']").click() 



try:
    element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//a[@href='https://rejestrcheb.mrit.gov.pl/wykaz-swiadectw-charakterystyki-energetycznej-czesci-budynku']")))
    driver.get("https://rejestrcheb.mrit.gov.pl/wykaz-swiadectw-charakterystyki-energetycznej-czesci-budynku")
except:
    driver.close()
    print("ERROR with loading page")
    print("RESTARTING...")
    time.sleep(2)
    os.system("WebsiteMaker.py" + ListOfXML)
    exit()


try:
    element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "ox_bgk-sr_SwiadectwoEnergetyczneCzesciBudynku2__CRUD___new")))
finally:
    driver.find_element_by_id("ox_bgk-sr_SwiadectwoEnergetyczneCzesciBudynku2__CRUD___new").click()

sww = False #something went wrong
emergencyList = "" #tutaj wpisze pliki ktore jeszcze trzeba zrobic jakby cos

#petla dla wszystkich xml w folderze
for file in ListOfXML:
    if sww: #no cos sie zepsulo i zapisujemy do pliku
        emergencyList = emergencyList + " " + file

    else:   #dzialamy
        print("Now making file: ", end = '')
        print(file)
        try:
            element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "ox_bgk-sr_SwiadectwoEnergetyczneCzesciBudynku2__SwiadectwoEnergetyczneCzesciBudynku___importXML")))
        except:        
            sww = True
            emergencyList = emergencyList + " " + file
            continue
        finally:
            driver.find_element_by_id("ox_bgk-sr_SwiadectwoEnergetyczneCzesciBudynku2__SwiadectwoEnergetyczneCzesciBudynku___importXML").click()

        #zalaczenie xml
        try:
            element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//input[@name='xmlFile']")))
        except:        
            sww = True
            emergencyList = emergencyList + " " + file
            continue
        finally:
            driver.find_element_by_xpath("//input[@name='xmlFile']").send_keys(currentPath + file)	

        try:
            element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "ox_bgk-sr_SwiadectwoEnergetyczneCzesciBudynku2__ImportSwiadectwo___importSwiadectwo")))
        except:        
            sww = True
            emergencyList = emergencyList + " " + file
            continue
        finally:
            driver.find_element_by_id("ox_bgk-sr_SwiadectwoEnergetyczneCzesciBudynku2__ImportSwiadectwo___importSwiadectwo").click()	

        #ten przycisk z onclick
        try:
            element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "ox_bgk-sr_SwiadectwoEnergetyczneCzesciBudynku2__SwiadectwoEnergetyczneCzesciBudynku___approve")))
        except:        
            sww = True
            emergencyList = emergencyList + " " + file
            continue
        finally:
            lol = driver.find_element_by_id("ox_bgk-sr_SwiadectwoEnergetyczneCzesciBudynku2__SwiadectwoEnergetyczneCzesciBudynku___approve")
            lol.send_keys(Keys.ENTER)
            alert_obj = driver.switch_to.alert
            alert_obj.accept()

        #to pobiera pdf'a
        try: 
            # Roboczy
            #element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "ox_bgk-sr_SwiadectwoEnergetyczneCzesciBudynku2__SwiadectwoEnergetyczneCzesciBudynku___pdf_roboczy")))
            # Final
            element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "ox_bgk-sr_SwiadectwoEnergetyczneCzesciBudynku2__SwiadectwoEnergetyczneCzesciBudynku___pdf")))
        except:        
            sww = True
            emergencyList = emergencyList + " " + file
            continue
        finally:
            # Roboczy
            #lol = driver.find_element_by_id("ox_bgk-sr_SwiadectwoEnergetyczneCzesciBudynku2__SwiadectwoEnergetyczneCzesciBudynku___pdf_roboczy")
            # Final

            lol = driver.find_element_by_id("ox_bgk-sr_SwiadectwoEnergetyczneCzesciBudynku2__SwiadectwoEnergetyczneCzesciBudynku___pdf")
            lol.send_keys(Keys.ENTER)

    
        #sprawdzamy czy po zapisaniu pliku jest o jeden wiecej plik niz przy poprzednim sprawdzeniu
        fileDownloadedSuccesfuly = WaitUntilDownloaded(howManyFilesInPDFdir, 10)
        if not fileDownloadedSuccesfuly:
            sww = True
            emergencyList = emergencyList + " " + file
            continue

        howManyFilesInPDFdir = howManyFilesInPDFdir + 1

        #dodajemy do nazwy pdf'a co trzeba
        list_of_files = glob.glob(currentPath + "PDF\\*.pdf") # * means all if need specific format then *.csv
        latest_file = max(list_of_files, key=os.path.getctime)
        newName = latest_file[:(len(latest_file) - 4)] + "_" + file[: (len(file) - 4) ] + ".pdf"
        os.rename(latest_file, newName)

driver.close()

if sww:
    print("ERROR")
    print("RESTARTING...")
    time.sleep(2)
    os.system("WebsiteMaker.py" + emergencyList)
else:
    print("SUCCESS")


