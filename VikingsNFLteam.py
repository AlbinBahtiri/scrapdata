import pandas as pd
import requests
from bs4 import BeautifulSoup
from datahandling import HandlingDataDb
import json


def scrape_vikings_stats(url):
	with open('connect_main.json', 'r') as file:
		db_config = json.load(file)['postgres_sql']

	# Initialize the database handler
	db_interface = HandlingDataDb(
		ip_address=db_config['IPAddress'],
		port=db_config['Port'],
		user=db_config['User'],
		password=db_config['Password']
	)

	try:
		print("Connecting to the database...")
		db_interface.connect_db()
		base_url = "https://www.vikings.com/team/players-roster/"

		# Fetch the main stats page
		print(f"Fetching main stats page: {url}")
		response = requests.get(url)
		if response.status_code == 200:
			print("Successfully fetched the page.")
		else:
			print(f"Failed to fetch the page. Status code: {response.status_code}")
			return

		soup = BeautifulSoup(response.text, 'html.parser')

		# Find all rows in the stats table
		rows = soup.find_all('tr')  # <tr> represents a table row
		if not rows:
			print("No stats found.")
			return []

		stats_data = []

		for row in rows:
			try:
				# Extract Player Name
				name_cell = row.find('span', class_='nfl-o-roster__player-name')
				player_name = name_cell.get_text(strip=True) if name_cell else "Unknown"
				player_slug = player_name.lower().replace(" ", "-")  # Basic slug conversion

				# Extract Player Stats
				stats_cells = row.find_all('td')
				stats = [cell.get_text(strip=True) for cell in stats_cells]

				# Fetch player-specific page for high-quality image and biography
				player_page_url = f"{base_url}{player_slug}/"
				print(f"Fetching player page: {player_page_url}")
				player_response = requests.get(player_page_url)
				if player_response.status_code == 200:
					print(f"Successfully fetched player page for {player_name}.")
				else:
					print(f"Failed to fetch player page for {player_name}. Status code: {player_response.status_code}")
					continue

				player_soup = BeautifulSoup(player_response.text, 'html.parser')

				# Extract High-quality Image
				actionshot_figure = player_soup.find(
					'figure',
					class_='d3-o-media-object__figure nfl-t-person-tile__actionshot'
				)
				high_quality_img = (
					actionshot_figure.find('source', {'data-srcset': True})['data-srcset']
					if actionshot_figure else "No high-quality image available"
				)


				bio_section = player_soup.find('div', class_='d3-o-media-object__body')
				biography = bio_section.get_text(strip=True) if bio_section else "No biography available"


				stats_data.append({
					"name": player_name,
					"stats": stats,
					"photo": high_quality_img,
					"biography": biography
				})

			except Exception as e:
				print(f"Error processing player row: {e}")

		# Convert to DataFrame
		df = pd.DataFrame(stats_data)
		print(f"Fetched {len(df)} players' data.")

		# Push Data to the Database
		table_name = 'viking_players'
		print(f"Pushing data to the {table_name} table.")
		db_interface.push_df_to_db(df, table_name)
		print("Data successfully inserted into the database.")

	except Exception as e:
		print(f"An error occurred: {e}")

	finally:
		db_interface.close_connection()
		print("Database connection closed.")

	return stats_data  # Optional, for further use or testing

if __name__ == "__main__":
    scrape_vikings_stats("https://www.vikings.com/team/players-roster/")
