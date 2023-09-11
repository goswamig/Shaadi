from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep
# Path to the ChromeDriver executable
chromedriver_path = "/usr/local/bin/chromedriver"  # Replace with the actual path to the ChromeDriver executable

# Set the ChromeDriver options
chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument("--headless")  # Run Chrome in headless mode

# Set the ChromeDriver service
service = Service(chromedriver_path)

# Create a new ChromeDriver instance
driver = webdriver.Chrome(service=service, options=chrome_options)

# Navigate to www.facebook.com
driver.get("https://www.facebook.com")

# Perform further actions on the webpage as needed
sleep(5)
# Close the browser
driver.quit()
