import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
import time


time.sleep(5)

# Load the JSON results
with open('../grant-details.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Define the path to chromedriver.exe in your repository
repo_root = os.path.dirname(os.path.abspath(__file__))
chrome_driver_path = "/workspace/Papaya/boe_grants/boe_grants/chromedriver-linux64/chromedriver"

# Ensure chromedriver.exe has the correct permissions
os.chmod(chrome_driver_path, 0o755)

# Initialize the Chrome WebDriver
service = ChromeService(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service)

# Google Form URL
google_form_url = 'https://docs.google.com/forms/d/e/1FAIpQLSedegi62A74DWhBxb1tk42nt5QdsZuS56owCVH10LISHeTNZQ/viewform?vc=0&c=0&w=1&flr=0'  

# Open the Google Form
driver.get(google_form_url)
driver.implicitly_wait(10)

form_fields = {
    'Identifier': data['identifier'],
    'Department': data['department'],
    'Publication Date': data['publication_date'],
    'Type of grant': data['grant_type'],
    'Grant Amount': data['amount'],
    'Application deadline': data['deadline']
}

for field_name, value in form_fields.items():
    try:
        # Find the input field by its name attribute
        input_field = driver.find_element(By.XPATH, f'//input[@aria-label="{field_name}"]')
        # Enter the value
        input_field.send_keys(value)
    except Exception as e:
        print(f"Error with field {field_name}: {e}")

# Submit the form
submit_button = driver.find_element(By.XPATH, '//span[text()="Submit"]') 
submit_button.click()

# Close the browser
driver.quit()
