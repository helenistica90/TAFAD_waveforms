from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import shutil
import os
from datetime import datetime
from selenium.common.exceptions import TimeoutException
import re
import glob
import random

# SELECT STATION CODE YOU WANT TO DOWNLOAD

station_code_to_search = '3113'
base_path = "/path/to/downloads"
station_path = os.path.join(base_path, station_code_to_search)  # Create the base station path

# =========================== #
#        FUNCTION DEFINITIONS #
# =========================== #

def restart_web():
   driver = webdriver.Chrome()
   driver.quit()  # Close the browser
   driver = webdriver.Chrome()  # Reopen the browser
   #Clear existing cookies to change session ID
   driver.delete_all_cookies()
   driver.get("https://tadas.afad.gov.tr")  # URL of the main page
   WebDriverWait(driver, 40).until_not(EC.visibility_of_element_located((By.CLASS_NAME, "block-ui-main")))
   # Click on an element to proceed to the desired URL
   first_element = WebDriverWait(driver, 40).until(
       EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Guest')]"))
   )
   print("Locator method used:", By.XPATH)  # Print the locator method
   # Scroll to the element
   ActionChains(driver).move_to_element(first_element).perform()
   # Click the element
   first_element.click()
   # Wait for overlay to disappear
   WebDriverWait(driver, 40).until_not(EC.visibility_of_element_located((By.CLASS_NAME, "block-ui-main")))
  
    
    
# Function to upload the already used numbers for avoiding repitition in case of unexpected failure whilst running
def cargar_numeros_utilizados(nombre_archivo):
    try:
        with open(nombre_archivo, 'r') as archivo:
            numeros_utilizados = set(map(int, archivo.readlines()))
        return numeros_utilizados
    except FileNotFoundError:
        return set()

# Save numbers in a file
def guardar_numeros_utilizados(numeros_utilizados, nombre_archivo):
    with open(nombre_archivo, 'w') as archivo:
        for numero in numeros_utilizados:
            archivo.write(str(numero) + '\n')

# File where used numbers are stored

nombre_archivo = 'used_event_numbers.txt'

# Upload numbers previously used
numeros_utilizados = cargar_numeros_utilizados(nombre_archivo)
# Configure the browser
driver = webdriver.Chrome()  # Change to your preferred browser if necessary

download_folder = "/path/to/downloads/"

# Number of times you want to perform the download process
num_downloads = 1000  # For example, 1000 downloads

# Access the main URL and perform initial click
try:
    restart_web()
    driver.delete_all_cookies()
    driver.get("https://tadas.afad.gov.tr")  # URL of the main page

    # Click on an element to proceed to the desired URL
    first_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Guest')]"))
    )
    print("Locator method used:", By.XPATH)  # Print the locator method
    # Scroll to the element
    ActionChains(driver).move_to_element(first_element).perform()
    # Click the element
    first_element.click()
    # Wait for overlay to disappear
    WebDriverWait(driver, 10).until_not(EC.visibility_of_element_located((By.CLASS_NAME, "block-ui-main")))

except Exception as e:
    print(f"Error during initial click: {e}")

#Remove the already tried numbers and Generate a list of event numbers (from 12406 to 12409 in this case)
# -----------------------------------------------------------------------------
# These numbers are an **arbitrary** choice.
# TAFAD (Turkish National Seismic Network) does NOT follow a logical or sequential numbering system.
# There is no clear pattern in their event IDs, so we cannot simply infer the next event ID.
#
# The range can be increased or decreased based on user needs.

numeritos=list(range(12406,12409))
numeritos = [num for num in numeritos if num not in numeros_utilizados]
if not numeritos:
    numeros_utilizados=set()
    
random.shuffle(numeritos)
for num in numeritos:   
    numeros_utilizados.add(num)
    guardar_numeros_utilizados(numeros_utilizados, nombre_archivo)
    mseed_files = glob.glob(os.path.join(download_folder, "*.mseed"))
    #restart_web()
    # Choose an adequate folder that does not store previous mseed files
    
    # Remove all .mseed files
    for file_path in mseed_files:
        os.remove(file_path)
    
    try:
        driver.delete_all_cookies()
        # Construct URL with the current number
        url = f"https://tadas.afad.gov.tr/event-detail/{num}"

        # Access the URL
        driver.get(url)

        WebDriverWait(driver, 30).until_not(EC.visibility_of_element_located((By.CLASS_NAME, "block-ui-main")))
        
        # Extract the date of the earthquake
        date_element = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@class='col-md-9']"))
        )
        original_date_str = date_element.text.strip()

        # Parse the original date string into a datetime object
        original_date = datetime.strptime(original_date_str, "%d %B %Y %H:%M")

        # Format the date into the desired format
        formatted_date_str = original_date.strftime("%d_%m_%Y")
        # Wait for the MW label to be present
        try:
           mw_label = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//label[contains(text(), 'MW')]"))
         )
        except TimeoutException:
               print("El elemento MW no se encontró dentro del tiempo especificado.")           
       
       


# Print or save the magnitude value
        
        # Click on the "Records" tab
        records_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Records']"))
        )
        records_tab.click()
        
       
         # Enter the station code in the input box
        input_box = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "k-textbox"))
        )
        input_box.clear()
        #input_box.send_keys("3113")
        input_box.send_keys(station_code_to_search)

# Wait for the Search button to be clickable
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Search')]"))
        )
        search_button.click()  # Click the Search button explicitly

        try:
            # Wait for the checkbox to be clickable
            checkbox = WebDriverWait(driver, 10).until(
                #EC.element_to_be_clickable((By.XPATH, "//td[contains(text(), '3113')]/preceding-sibling::td/input[@type='checkbox']"))
                EC.element_to_be_clickable((By.XPATH, f"//td[contains(text(), '{station_code_to_search}')]/preceding-sibling::td/input[@type='checkbox']"))
            )
            # Click the checkbox
            checkbox.click()
            
            # Wait for the MINISEED button to be clickable
            miniseed_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//label[@for='mseed']"))
            )
            time.sleep(5)

            # Click the MINISEED button
            miniseed_button.click()
            
            # Wait for the Download button to be clickable
            download_button = WebDriverWait(driver, 10).until(
                 EC.element_to_be_clickable((By.XPATH, "//button[@class='k-button k-primary' and text()='Download']"))
            )

            # Click the Download button
            download_button.click()

            # Wait for the download process to start
            WebDriverWait(driver, 10).until(
                 EC.visibility_of_element_located((By.CLASS_NAME, "loader"))
            )

            # Wait for the querying process to complete
            WebDriverWait(driver, 600).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "loader"))
            )
            time.sleep(5)
  
            # Find the downloaded file
            files = os.listdir(download_folder)
            for file in files:
                if file.endswith(".mseed"):
                    try:
                # Localizar el elemento <strong> que contiene la magnitud
                       strong_elemento = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//strong[contains(text(),'Earthquake MW') or contains(text(),'Earthquake ML') or contains(text(),'Earthquake MD')]"))
                )

                # Obtener el texto del elemento
                       texto_strong = strong_elemento.text.strip()

                #
                             
                       try:
                             magnitud_coincidencia = re.search(r'MW\s+(\d+\.\d+)', texto_strong)
                             if magnitud_coincidencia is None:
                                raise ValueError("MW pattern not found")
                       except AttributeError as ae:
                             print("AttributeError occurred:", ae)
                             magnitud_coincidencia = None
                       except ValueError as ve:
                             print(ve)
                             try:
                                 magnitud_coincidencia = re.search(r'ML\s+(\d+\.\d+)', texto_strong)
                                 if magnitud_coincidencia is None:
                                     raise ValueError("ML pattern not found")
                             except ValueError as ve2:
                                 print(ve2)
                                 try:
                                    magnitud_coincidencia = re.search(r'MD\s+(\d+\.\d+)', texto_strong)
                                    if magnitud_coincidencia is None:
                                       raise ValueError("MD pattern not found")
                                 except ValueError as ve3:
                                     print(ve3)
                                     magnitud_coincidencia = None      
                             
                             
                             
                             
                             
                             
                             
                             
                             
                             
                             
                                  
                       if magnitud_coincidencia:
                          magnitud = float(magnitud_coincidencia.group(1))
                          print("Magnitud:", magnitud)
                          if magnitud >= 1 and magnitud < 2:
                             destination_directory = os.path.join(station_path, "1")
                          elif magnitud >= 2 and magnitud < 3:
                              destination_directory = os.path.join(station_path, "2")
                          elif magnitud >= 3 and magnitud < 4:
                                destination_directory = os.path.join(station_path, "3")
                          elif magnitud >= 4 and magnitud < 5:
                              destination_directory =  os.path.join(station_path, "4")
                          elif magnitud >= 5 and magnitud < 6:
                              destination_directory = os.path.join(station_path, "5")
                          elif magnitud >= 6 and magnitud < 7:
                              destination_directory = os.path.join(station_path, "6")
                          elif magnitud >= 7 and magnitud < 8:
                              destination_directory = os.path.join(station_path, "7")
                          elif magnitud >= 8 and magnitud < 9:
                              destination_directory = os.path.join(station_path, "8")
                          elif magnitud >= 9:
                              destination_directory =  os.path.join(station_path, "9")
                          else:
                              destination_directory = os.path.join(station_path, "other")
                       else:
                           print("No se encontró la magnitud en el texto:", texto_strong)
                           destination_directory = os.path.join(station_path, "other")

                    except TimeoutException:
                             print("El elemento no se encontró dentro del tiempo especificado.")
                    except Exception as e:
                            print("Se produjo un error:", e)
                      
                      
                      # Determinar el directorio de destino según la magnitud
                   
                    old_file_name = os.path.join(download_folder, file)
                   # Rename the downloaded file with the earthquake date
                    current_timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                    new_file_name = f"{formatted_date_str}_{num}.mseed"
                    new_file_path = os.path.join(download_folder, new_file_name)
                    os.rename(old_file_name, new_file_path)
                    # Ensure the destination directory exists
                    os.makedirs(destination_directory, exist_ok=True)
                    shutil.move(new_file_path, destination_directory)
                    break

        except TimeoutException:
            print(f"No records found for station code {station_code_to_search}. Skipping download for event {num}.")

    except Exception as b:
    
            
        print(f"Error while processing event {num}: {b}")
        try:
            print(f"Error while processing event {num}: {b}")
            #restart_web()
           
        except Exception as c:
                driver.quit()  # Close the browser
                driver = webdriver.Chrome()  # Reopen the browser
                #Clear existing cookies to change session ID
                driver.delete_all_cookies()
                driver.get("https://tadas.afad.gov.tr")  # URL of the main page
                WebDriverWait(driver, 10).until_not(EC.visibility_of_element_located((By.CLASS_NAME, "block-ui-main")))
                # Click on an element to proceed to the desired URL
                first_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Guest')]"))
                )
                print("Locator method used:", By.XPATH)  # Print the locator method
                # Scroll to the element
                ActionChains(driver).move_to_element(first_element).perform()
                # Click the element
                first_element.click()
                # Wait for overlay to disappear
                WebDriverWait(driver, 10).until_not(EC.visibility_of_element_located((By.CLASS_NAME, "block-ui-main")))
                print(f"Error during initial click: {c}")

