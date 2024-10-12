import requests
import os
from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Define a function to fetch, parse, and save the table to a CSV/Excel file
def fetch_and_save_stats(url, filename_prefix, div_id, table_id):
    driver = webdriver.Chrome()
    driver.get(url)

    # Wait for the page to load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, div_id)))

    # Get the page source and parse it
    page_source = driver.page_source
    soup = bs(page_source, 'html.parser')

    # Extract the relevant table
    div = soup.find('div', {'id': div_id})
    table = div.find('table', {'id': table_id})

   
    # Get the first and second header rows
    headers = []
    thead = table.find('thead')
    first_row = thead.find_all('tr')[0]  # First row of headers (with possible colspans)
    second_row = thead.find_all('tr')[1]  # Second row of headers

    # Prepare a list to store combined headers
    combined_headers = []
    first_row_headers = []

    # Process the first row (for broader categories)
    for th in first_row.find_all('th'):
        colspan = int(th.get('colspan', 1))  # Get the colspan value (default is 1 if not present)
        label = th.text.strip()

        # Add the label as many times as the colspan value (to spread across columns)
        first_row_headers.extend([label] * colspan)

    # Process the second row (for detailed column names)
    for idx, th in enumerate(second_row.find_all('th')):
        aria_label = th.text.strip()  # Only use the text from the second row

        broader_category = first_row_headers[idx]  # Get the broader category from the first row

        # Combine broader category and detailed name, but only if broader category is not empty
        if broader_category:
            combined_header = f"{broader_category} - {aria_label}"
        else:
            combined_header = aria_label  # Use just the second row header if the first row is empty

        combined_headers.append(combined_header)

    # Flatten headers
    flattened_headers = []
    for header in combined_headers:
        # If the header includes " - ", split it into a more detailed format
        if " - " in header:
            category, sub_header = header.split(" - ", 1)
            flattened_headers.append(f"{category}-{sub_header}")
        else:
            flattened_headers.append(header)

    # Get player data as a list of dictionaries
    player_data = []
    tbody = table.find('tbody')
    rows = tbody.find_all('tr')

    # Loop through each row and extract data
    for row in rows:
        first_column = row.find('th').text.strip()  # The first column is usually rank
        columns = [col.text.strip() for col in row.find_all('td')]

        if len(columns) == 0:
            continue

        # Create a dictionary with the headers as keys and data as values
        player_info = {flattened_headers[0]: first_column}  # Rank
        for idx, column in enumerate(columns):
            player_info[flattened_headers[idx+1]] = column  # Use the flattened header for the key

        player_data.append(player_info)


    # Convert to DataFrame and save to CSV and Excel
    df = pd.DataFrame(player_data)

    csv_filename = f"{filename_prefix}.csv"
    excel_filename = f"{filename_prefix}.xlsx"
    
    df.to_csv(csv_filename, index=False, encoding='utf-8')
    # df.to_excel(excel_filename, index=False)

    print(f"Data saved to {csv_filename}")
    # print(f"Data saved to {excel_filename}")
    driver.quit()

# URLs and corresponding div and table IDs for different stats
urls = {
    "standard_stats": {
        "url": "https://fbref.com/en/comps/9/2023-2024/stats/2023-2024-Premier-League-Stats",
        "div_id": "div_stats_standard",  # Specific div ID for the standard stats
        "table_id": "stats_standard"     # Specific table ID for the standard stats
    },
    "goalkeeping_stats": {
        "url": "https://fbref.com/en/comps/9/2023-2024/keepers/2023-2024-Premier-League-Stats",
        "div_id": "div_stats_keeper",
        "table_id": "stats_keeper"
    },
    "shooting_stats": {
        "url": "https://fbref.com/en/comps/9/2023-2024/shooting/2023-2024-Premier-League-Stats",
        "div_id": "div_stats_shooting",
        "table_id": "stats_shooting"
    },
    "passing_stats": {
        "url": "https://fbref.com/en/comps/9/2023-2024/passing/2023-2024-Premier-League-Stats",
        "div_id": "div_stats_passing",
        "table_id": "stats_passing"
    },
    "pass_types_stats": {
        "url": "https://fbref.com/en/comps/9/2023-2024/passing_types/2023-2024-Premier-League-Stats",
        "div_id": "div_stats_passing_types",
        "table_id": "stats_passing_types"
    },
    "goal_and_shot_creation_stats": {
        "url": "https://fbref.com/en/comps/9/2023-2024/gca/2023-2024-Premier-League-Stats",
        "div_id": "div_stats_gca",
        "table_id": "stats_gca"
    },
    "defensive_actions_stats": {
        "url": "https://fbref.com/en/comps/9/2023-2024/defense/2023-2024-Premier-League-Stats",
        "div_id": "div_stats_defense",
        "table_id": "stats_defense"
    },
    "possession_stats": {
        "url": "https://fbref.com/en/comps/9/2023-2024/possession/2023-2024-Premier-League-Stats",
        "div_id": "div_stats_possession",
        "table_id": "stats_possession"
    },
    "playing_time_stats": {
        "url": "https://fbref.com/en/comps/9/2023-2024/playingtime/2023-2024-Premier-League-Stats",
        "div_id": "div_stats_playing_time",
        "table_id": "stats_playing_time"
    },
    "miscellaneous_stats": {
        "url": "https://fbref.com/en/comps/9/2023-2024/misc/2023-2024-Premier-League-Stats",
        "div_id": "div_stats_misc",
        "table_id": "stats_misc"
    }
}

if not os.path.exists('data'):
    os.makedirs('data')

# Loop through each URL and fetch/save the data
for stat_type, info in urls.items():
    fetch_and_save_stats(info['url'], f"./data/premier_league_{stat_type}", info['div_id'], info['table_id'])
