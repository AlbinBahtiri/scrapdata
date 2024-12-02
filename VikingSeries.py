import requests
from bs4 import BeautifulSoup
import pandas as pd
from datahandling import HandlingDataDb
import json

# Load database configuration
with open('connect_main.json', 'r') as file:
    config = json.load(file)
db_config = config['postgres_sql']

# Scraping function
def scrape_vikings_cast(url):
    try:
        # Send a GET request to the website
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the cast section
        cast_section = soup.find('div', class_='content content-with-sidebar')
        if not cast_section:
            print("Could not find the cast section on the page.")
            return []

        # Extract cast information
        cast_list = []
        tile_list = cast_section.find('ul')  # The <ul> containing cast details
        for tile in tile_list.find_all('li'):  # Iterate through each <li>
            name_element = tile.find('strong')
            actor_element = tile.find('small')
            img_element = tile.find('img')

            if name_element and actor_element and img_element:
                name = name_element.get_text(strip=True)
                # Remove "Played by" from the actor text
                actor = actor_element.get_text(strip=True).replace("Played by ", "")
                img_url = img_element['src']
                cast_list.append({
                    'character': name,
                    'name': actor,
                    'img': img_url
                })

        return cast_list

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return []

# Main function
if __name__ == "__main__":
    # URL for scraping
    url = "https://www.history.com/shows/vikings/cast"

    # Scrape data
    cast = scrape_vikings_cast(url)

    # Convert cast data into DataFrame
    df = pd.DataFrame(cast)

    # Database operations
    db_interface = HandlingDataDb(
        ip_address=db_config['IPAddress'],
        port=db_config['Port'],
        user=db_config['User'],
        password=db_config['Password']
    )
    db_interface.connect_db()

    # Specify table name
    table_name = "characters"

    # Push DataFrame to the database
    db_interface.push_df_to_db(df, table_name,additional_columns={"biography":""})
    print(f"Data successfully pushed to table: {table_name}")
