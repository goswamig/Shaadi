from bs4 import BeautifulSoup
import os 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from time import sleep
from bs4 import BeautifulSoup
import time
import random
import re



# Read the user and password from environment variable
user = os.environ.get('HMEMAIL')
password = os.environ.get('HMPASSWORD')
shaadiFile="retry_id"

if not user or not password:
   print("EMAIL and PASSWORD are not set as environment variables")
   exit(0)

# Specify the path to chromedriver.exe (download and save on your computer)
chromedriver_path = '/usr/local/bin/chromedriver'

# Set the ChromeDriver options
chrome_options = webdriver.ChromeOptions()

# If you want the browser to be launched just comment the line below
#chrome_options.add_argument("--headless")  # Run Chrome in headless mode

# Set the ChromeDriver service
service = Service(chromedriver_path)

# Create a new ChromeDriver instance
driver = webdriver.Chrome(service=service, options=chrome_options)

# Navigate to Shaadi.com
driver.get("https://www.hindimatrimony.com/")

# Wait for the login button to be clickable
login_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "open_loginpp"))
)

# Click on the login button
login_button.click()

# Wait for the login pop-up to appear
login_popup = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "loginpopup"))
)

# Find the email and password fields in the pop-up
email_field = login_popup.find_element(By.ID, "ID")

# Fill in the email field
email_field.send_keys(user)

# Find the visible text input field for password
password_field_dummy = login_popup.find_element(By.ID, "TEMPPASSWD1")

# Click on the dummy password field to trigger the onfocus event
password_field_dummy.click()

# Now find the actual password field which should be visible now
password_field = login_popup.find_element(By.ID, "PASSWORD")

# Fill in the password field
password_field.send_keys(password)

# Click on the login button in the pop-up
login_button_popup = login_popup.find_element(By.CSS_SELECTOR, "input[value='LOGIN']")
login_button_popup.click()

time.sleep(5)

print("Login Succceeded")

# Navigate to the matches
driver.get("https://matches.bharatmatrimony.com/listing/matches")

# Wait until the candidate cards are loaded
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "divScroll")))

# Get all the candidate cards
candidate_cards = driver.find_elements(By.CSS_SELECTOR, 'div[id="matchCard"]')

print("Total candidates found " + str(len(candidate_cards)))

for i, candidate in enumerate(candidate_cards, 1):
    candidate_html = candidate.get_attribute("outerHTML")

    soup = BeautifulSoup(candidate_html, "html.parser")
    link = soup.find("a", href=True)

    if link:
        href = link['href']

        match = re.search(r"/matches/viewprofile/(\w+)", href)
        if match:
            profile_id = match.group(1)
            print("Processing " + str(i) + " id " + profile_id)

            print("Found profile ID:", profile_id)

            # Find the "Message" button and click on it

            # Define a function for clicking the Message button
            def click_message_button():
                try:
                    message_button = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.XPATH, '//button[contains(.,"Message")]'))
                    )
                    print("Found Message button")
                    message_button.click()
                    print("Clicked on Message button")
                    return True
                except Exception as e:
                    print("Error while finding or clicking Message button:", str(e))
                    return False

            # Retry clicking the Message button up to 3 times
            for attempt in range(3):
                if click_message_button():
                    break
                else:
                    print(f"Retry {attempt+1}...")
                    time.sleep(random.randint(2, 5))
            
            try: 
                print("switching to new window")
                # Switch to the pop-up window
                driver.switch_to.window(driver.window_handles[-1])
                print("successfully switched to new window")
               
                # Wait for pop-up-2 to appear
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "sendMail")))
                print("waiting for pop up to appear")

                popup = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "sendMail")))
                popup_html = popup.get_attribute('outerHTML')
                print(popup_html)

                soup = BeautifulSoup(popup_html, 'html.parser')
                connect_button = soup.find('button', class_='btn-primary')
                connect_button_class = " ".join(connect_button.get('class'))
                print(connect_button_class)            


                # Define a function for clicking the Message button
                def click_send_message_button():
                    try:
                        # Find the Send Message button in pop-up-2
                        connect_button_popup = WebDriverWait(popup, 20).until(
                            EC.element_to_be_clickable((By.XPATH, f"//button[contains(@class, '{connect_button_class}')]"))
                        )
                        print("Found connect button pop up")
                        connect_button_popup.click()
                        print("Clicked on Send Message button")
                        return True
                    except Exception as e:
                        print("Error while finding or clicking Send Message button:", str(e))
                        return False

                # Retry clicking the Message button up to 3 times
                for attempt in range(3):
                    if click_send_message_button():
                        break
                    else:
                        print(f"Retry {attempt+1}...")
                        time.sleep(random.randint(2, 5))

                sleep(random.randint(1,2))
            
                # Switch back to the main window
                driver.switch_to.window(driver.window_handles[0])

                print("Successfully sent the request to candidate " + str(i) + " shaadi id " + profile_id)

                time.sleep(random.randint(1, 5))
            
            except Exception as e:
               print("An error has occurred: " + str(e))
               pass
            #break
