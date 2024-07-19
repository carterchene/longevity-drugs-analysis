import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import duckdb
import time
from .project import longevity_dbt
from dagster import asset, MaterializeResult, AssetExecutionContext
from dagster_dbt import DbtCliResource, dbt_assets
from dagster_gcp import BigQueryResource

@asset(description="Goes to drug age website and scrapes data from html tables.")
def scrape_drug_age() -> MaterializeResult: 
    # Set up the WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    url = 'https://genomics.senescence.info/drugs/browse.php'
    driver.get(url)

    # Give the page some time to load
    time.sleep(3)

    # Find the dropdown element and select the maximum number of entries per page
    dropdown = Select(driver.find_element(By.NAME, 'DataTables_Table_0_length'))  # Adjust this if the element name is different
    dropdown.select_by_value('2000') # 2000 is the max, could make this dynamic

    time.sleep(3)

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
            time.sleep(3)  # Wait for the next page to load
        except:
            break  # Exit the loop if there's no "Next" button

    # Close the WebDriver
    driver.quit()

    with duckdb.connect('duckdb_database/drug_age.db') as con: 
        con.sql('create schema if not exists raw')
        con.sql('create or replace table raw.drug_age as select * from all_data') 

    return MaterializeResult(
        metadata={
            "num_records": len(all_data)
        }
    )

@asset(deps=['datamart__longevity_analysis']) # dbt models can be referenced just as there model name which is sweet
def serve_datamart_gcp(bigquery: BigQueryResource) -> None:
    # get duckdb data
    with duckdb.connect('duckdb_database/drug_age.db') as con:
        longevity_df = con.execute('select * from datamart.longevity_analysis').df()
    
    with bigquery.get_client() as client:
        job = client.load_table_from_dataframe(
            dataframe=longevity_df,
            destination='datamart.longevity_analysis'
        )

        job.result()
    


@dbt_assets(manifest=longevity_dbt.manifest_path)
def my_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()


