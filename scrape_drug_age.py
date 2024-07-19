import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import duckdb
import time

# Set up the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the webpage
url = 'https://genomics.senescence.info/drugs/browse.php'
driver.get(url)

# Give the page some time to load
time.sleep(5)

# Find the dropdown element and select the maximum number of entries per page
dropdown = Select(driver.find_element(By.NAME, 'DataTables_Table_0_length'))  # Adjust this if the element name is different
dropdown.select_by_value('2000')

# Give the page some time to load the table
time.sleep(5)

# Initialize an empty DataFrame to store all entries
all_data = pd.DataFrame()

while True:
    # Find the table element
    table = driver.find_element(By.TAG_NAME, 'table')

    # Read the table with pandas
    df = pd.read_html(table.get_attribute('outerHTML'))[0]

    # Append the current page's data to the all_data DataFrame
    all_data = pd.concat([all_data, df], ignore_index=True)

    # Try to find the "Next" button to go to the next page
    try:
        next_button = driver.find_element(By.ID, 'DataTables_Table_0_next')
        if 'disabled' in next_button.get_attribute('class'):
            break  # Exit the loop if the "Next" button is disabled
        next_button.click()
        time.sleep(5)  # Wait for the next page to load
    except:
        break  # Exit the loop if there's no "Next" button

# Close the WebDriver
driver.quit()

with duckdb.connect('duckdb_database/drug_age.db') as con: 
    con.sql('create schema if not exists raw')
    con.sql('create table raw.drug_age as select * from all_data')

# Display the DataFrame
#all_data.to_csv('drug_age.csv')
#print(all_data)