from bs4 import BeautifulSoup
import os 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from time import sleep
import re

# Read the user and password from environment variable
user = os.environ.get('JSEMAIL')
password = os.environ.get('JSPASSWORD')

if not user or not password:
   print("JSEMAIL and JSPASSWORD are not set as environment variables")
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
driver.get("https://www.jeevansathi.com/")


# Wait for the login hyperlink to become clickable and click on it
login_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[@data-attr="LoginNav"]')))

driver.execute_script("arguments[0].click();", login_link)

#action = ActionChains(driver)
#action.move_to_element(login_link).click().perform()

#login_link.click()

# Need some wait before can feed the email/password
sleep(3)

# Pass email address
email_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//input[@id="email"]')))
email_input.send_keys(user)
# Verify if the entered value matches the expected value
entered_value = email_input.get_attribute('value')
if entered_value != user:
    print("Failed to fill the email input field.")

# Pass password
password_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//input[@id="password"]')))
password_input.send_keys(password)
entered_value = password_input.get_attribute('value')
if entered_value != password:
    print("Failed to fill the password input field.")

sleep(2)
# Find and click the login button
login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "jspcLoginLayerButton")))
login_button.click()
#
sleep(2)
print("login has succeeded")

# now close any pop up, enable this if they create any pop up
#try: 
#   # Find the close button element
#   close_button = driver.find_element(By.CSS_SELECTOR, 'svg[fill="currentColor"]')
#   actions = ActionChains(driver)
#   actions.move_to_element(close_button).click().perform()
#   print("Closed the button")
#except Exception as e:
#   print("Error has occurred " + str(e))
#   pass 
sleep(4)

try:
   # Find the search button element
   search_button = driver.find_element(By.ID, "search-navigation-button")
   
   # Perform a JavaScript click on the search button
   actions = ActionChains(driver)
   actions.move_to_element(search_button).click().perform()
   print("Search tab has clicked")
except Exception as e:
   print("Error has occurred during search " + str(e))
   pass

sleep(4)

try:

    #print(driver.page_source)
    wait = WebDriverWait(driver, 10)  # Adjust the timeout as needed
    show_profiles_button = wait.until(EC.presence_of_element_located((By.ID, "showProfiles")))
    #show_profiles_button = driver.find_element(By.ID, "showProfiles")
    show_profiles_button.click()
    print("Clicked on 'Show Me Profiles' button.")
except NoSuchElementException:
    print("Button element not found.")
except Exception as e:
    print(f"An error occurred: {str(e)}")

sleep(3)

# Wait for the page to load and custom cards to appear
wait = WebDriverWait(driver, 10)
cards = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "custom-searchResult-card")))
print("Total candidates found " +  str(len(cards)))

for card in cards:
    page_source = card.get_attribute("outerHTML")

    send_interest_button = card.find_element(By.ID, "Send Interest")
    send_interest_button.click()
    sleep(2)

    # Find the input field and send the message
    input_field = card.find_element(By.CSS_SELECTOR, 'input[type="text"].relative')
    input_field.send_keys("I liked your profile, feel free to accept the request if you like my profile too. I can be reached out on whatsapp at +1-408-242-9707")
    sleep(2)    

    # Find the send interest button and click on it
    button = driver.find_element(By.CSS_SELECTOR, "button.absolute.right-3.top-1\\/2.h-10.w-10.\\-translate-y-1\\/2.rounded-full.bg-primary-500")
    button.click()

    pattern = r'id="custom-card-(.*?)"'
    match = re.search(pattern, page_source)
    if match:
        card_id = match.group(1)
        s="https://www.jeevansathi.com/profile-detail/" + card_id + "?stype=A"
        print("Request sent to " + s)

