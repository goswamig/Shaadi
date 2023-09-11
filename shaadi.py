from bs4 import BeautifulSoup
import os 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from bs4 import BeautifulSoup
import time
import random
import re


# Read the user and password from environment variable
user = os.environ.get('EMAIL') 
password = os.environ.get('PASSWORD')
shaadiFile="retry_id"

if not user or not password:
   print("EMAIL and PASSWORD are not set as environment variables")
   exit(0)

# Specify the path to chromedriver.exe (download and save on your computer)
chromedriver_path = '/usr/local/bin/chromedriver'

# Set the ChromeDriver options
chrome_options = webdriver.ChromeOptions()

# If you want the browser to be launched just comment the line below
chrome_options.add_argument("--headless")  # Run Chrome in headless mode

# Set the ChromeDriver service
service = Service(chromedriver_path)

# Create a new ChromeDriver instance
driver = webdriver.Chrome(service=service, options=chrome_options)

# Navigate to Shaadi.com
driver.get("https://www.shaadi.com/")

# Wait for the login hyperlink to become clickable and click on it
login_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[@data-testid="login_link"]')))
login_link.click()


# Wait for the email input field to appear and enter email address
email_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@data-testid="login_email"]')))
email_input.send_keys(user)

# Enter password
password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@data-testid="login_password"]')))
password_input.send_keys(password)

# Click on the login button
login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="sign_in"]')))
login_button.click()

print("Login has succeeded")

# Go to the website
driver.get("https://www.shaadi.com/search/partner")

#html_code = driver.page_source
#shm = "shaadi.html"
#with open(shm, 'a') as file:
#      file.write(html_code)

try:
    # Check if the random pop-up exists and close it
    pop_up = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class,'modal-close-btn')]")))
    pop_up.click()
except Exception as e:
    print("Most likely there are new pop" + str(e))
    pass

try:
    # Find all candidates with id starting with 'true_view'
    candidates = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[id^='true_view']")))
except Exception as e:
    print("Error has occurred during getting the candidate list " + str(e))
    raise 

try:
    # Check if random pop-up exists and close it
    pop_up = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class,'campaignClose')]")))
    pop_up.click()
except:
    pass

# To filter candidate if include more matches enabled
def grep_for_software(html):
    pattern = re.compile(r'software', re.IGNORECASE)
    if re.search(pattern, html):
        return True
    else:
        return False

# locate a candidate and send the request


print("total candidates found ", len(candidates))
i = 1
# Loop through each candidate and try to connect with them
for candidate in candidates:
    candidate_html = candidate.get_attribute('outerHTML')
    soup = BeautifulSoup(candidate_html, 'html.parser')
    first_div = soup.find('div')
    first_div_id = first_div.get('id') # true_view_4SH77170379
    shaadi_id = first_div_id[11:]
    print("Processing " + str(i) + " id " + shaadi_id) 
    try: 
       if 'title="Connect"' in candidate_html:
              connect_button = WebDriverWait(candidate, 5).until(EC.element_to_be_clickable((By.XPATH, ".//button[@title='Connect']")))
       else:
              button = soup.find('button')
              if button:
                 class_name = button.get('class')
                 button_class_name = " ".join(class_name)
                 connect_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, ".//button[contains(@class, '"+button_class_name+"')]")))
       
       driver.execute_script("arguments[0].click();", connect_button)
       #connect_button.click()

       # Switch to the pop-up window
       driver.switch_to.window(driver.window_handles[-1])

       # Wait for pop-up to appear
       WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test-selector='send_connect']")))

       # Find and Click on the 'Connect' button in the pop-up
       popup = driver.find_element(By.CSS_SELECTOR, "[data-test-selector='send_connect']")

       # Find the class name of `Connect` button so that we can identify them later 
       popup_html = popup.get_attribute('outerHTML')
       soup = BeautifulSoup(popup_html, 'html.parser')
       connect_button = soup.find('button', text='Connect')
       connect_button_class = " ".join(connect_button.get('class'))

       # Find the Connect button and click on it
       connect_button_popup = popup.find_element(By.XPATH, f"//button[contains(text(), 'Connect') and contains(@class, '{connect_button_class}')]")
       connect_button_popup.click()

       # Wait for pop-up to disappear
       WebDriverWait(driver, 10).until_not(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test-selector='send_connect']")))

       # Switch back to the main window
       driver.switch_to.window(driver.window_handles[0])
       print("Successfully sent the request to candidate " + str(i) + " shaadi id " + shaadi_id)
       time.sleep(random.randint(1, 5))

    except Exception as e:
       print("An  error has occurred " + str(e))
       with open(shaadiFile, 'a') as file:
           file.write(shaadi_id + '\n')
       pass
    i += 1

