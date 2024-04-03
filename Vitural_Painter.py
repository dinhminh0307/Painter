
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from bs4 import BeautifulSoup
from io import StringIO
import pandas as pd
import time

# Path to your WebDriver
s = Service(r'C:\Users\DELL\Downloads\chromedriver-win32\chromedriver-win32\chromedriver.exe')

# Initialize the Chrome WebDriver
browser = webdriver.Chrome(service=s)

# URL of the webpage
url = 'https://www.hnx.vn/vi-vn/trai-phieu/ket-qua-gd-trong-ngay.html?site=in'

# Navigate to the webpage
browser.get(url)

# Initialize an empty DataFrame to hold all the data
all_data = pd.DataFrame()

# Other imports remain the same
try:
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'divDataTables')))

    while True:
        current_table_html = browser.find_element(By.ID, 'divDataTables').get_attribute('outerHTML')
        current_data = pd.read_html(StringIO(current_table_html))[0]
        all_data = pd.concat([all_data, current_data], ignore_index=True)

        # Re-identify the 'Next' button before each click to avoid StaleElementReferenceException
        try:
            next_button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID, 'next')))
            next_button.click()
            time.sleep(1)  # Adjust based on observed site response time
        except NoSuchElementException:
            break
        except TimeoutException:
            break

    all_data.to_excel('output.xlsx', index=False)
finally:
    browser.quit()

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.service import Service
# from selenium.common.exceptions import NoSuchElementException, TimeoutException
# from bs4 import BeautifulSoup
# import pandas as pd
# import time
#
# # Initialize the WebDriver
# s = Service(r'C:\Users\DELL\Downloads\chromedriver-win32\chromedriver-win32\chromedriver.exe')
# browser = webdriver.Chrome(service=s)
#
# # Navigate to the webpage
# url = 'https://www.hnx.vn/vi-vn/trai-phieu/ket-qua-gd-trong-ngay.html?site=in'
# browser.get(url)
#
# all_rows = []  # List to store all rows of data
#
# try:
#     WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'divDataTables')))
#
#     while True:
#         # Get the current state of the HTML content
#         innerHTML = browser.execute_script("return document.body.innerHTML")
#         soup = BeautifulSoup(innerHTML, 'html.parser')
#
#         # Locate the table by ID or another unique identifier
#         table = soup.find('table', {'id': 'divContainTable'})  # Update with actual table ID or selector
#
#         # Make sure the table was found
#         if table:
#             # Extract table rows
#             for row in table.find_all('tr')[1:]:  # Assuming the first row is the header
#                 cols = [ele.text.strip() for ele in row.find_all(['th', 'td'])]
#                 all_rows.append(cols)
#
#         # Try to find and click the "Next" button, identified by ID 'next' in this case
#         try:
#             next_button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID, 'next')))
#             next_button.click()
#             time.sleep(1)  # Adjust sleep time as needed
#         except NoSuchElementException:
#             break  # No more "Next" button; exit the loop
#         except TimeoutException:
#             break  # Timeout; exit the loop
#     if all_rows:
#         df = pd.DataFrame(all_rows[1:], columns=all_rows[0])
#         df.to_excel('output.xlsx', index=False)
#     else:
#         print("No data was extracted from the table.")
#
#     # # Convert all rows to a DataFrame
#     # df = pd.DataFrame(all_rows[1:], columns=all_rows[0])  # Assuming the first row contains headers
#     #
#     # # Save the DataFrame to an Excel file
#     # df.to_excel('output.xlsx', index=False)
#
# finally:
#     browser.quit()  # Ensure the browser is closed even if an error occurs
