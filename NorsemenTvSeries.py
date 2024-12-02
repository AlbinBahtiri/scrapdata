import pandas as pd
import json
import requests
from bs4 import BeautifulSoup
from datahandling import HandlingDataDb


def main():
    # Step 1: Load database credentials
    with open('connect_main.json', 'r') as file:
        db_config = json.load(file)['postgres_sql']

    # Step 2: Initialize the database handler
    db_interface = HandlingDataDb(
        ip_address=db_config['IPAddress'],
        port=db_config['Port'],
        user=db_config['User'],
        password=db_config['Password']
    )
    db_interface.connect_db()

    # Step 3: Scrape data
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    base_url = "https://en.wikipedia.org"
    main_url = f"{base_url}/wiki/Norsemen_(TV_series)"
    response = requests.get(main_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Locate the Cast and Characters section and get all character names
    cast_section = soup.find('h2', id='Cast_and_characters')
    character_names = []

    if cast_section:
        for a in cast_section.find_next('ul').find_all('a', href=True):
            character_names.append(a.text.strip())

    # Step 4: Prepare data for database
    data = []
    for char_name in character_names:
        char_url = f"{base_url}/wiki/{char_name.replace(' ', '_')}"
        char_response = requests.get(char_url, headers=headers)
        char_soup = BeautifulSoup(char_response.text, 'html.parser')

        # Character name (in <h1>)
        char_name = char_soup.find('h1').text.strip()

        # Description (first paragraph <p>)
        try:
            description = char_soup.find('p').text.strip()
        except AttributeError:
            description = "Description not found"

        # Find the image in the infobox-image column
        img_url = "Image not found"
        infobox_image = char_soup.find('table', class_='infobox biography vcard')
        if infobox_image:
            img_tag = infobox_image.find('img')
            if img_tag:
                img_url = "https:" + img_tag['src']

        data.append({'character_name': char_name, 'description': description, 'image_url': img_url})

    # Step 5: Convert data to a DataFrame
    df = pd.DataFrame(data)

    # Step 6: Push the DataFrame to the database
    table_name = 'norsemen_characters'
    db_interface.push_df_to_db(df, table_name)

    print("Data successfully inserted into the database.")


if __name__ == '__main__':
    main()
