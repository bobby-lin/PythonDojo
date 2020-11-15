import asyncio
import aiohttp
import pandas as pd
import aiofiles
import json
from time import time
from bs4 import BeautifulSoup

directory = "output/"


async def fetch_html(url):
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        html = await response.text()
        return str(html)


# Search the Wikipedia link of a football club using DuckDuckGo API
async def fetch_wiki_url(club_name):
    async with aiohttp.ClientSession() as session:
        url = f'https://api.duckduckgo.com/?q={club_name}+Wikipedia&format=json'
        response = await session.get(url) # Wait for GET request to complete
        club_data = await response.text() # Wait for data to be ready
        club_json = json.loads(club_data)
        return club_json['AbstractURL']


async def write_file(file, data):
    async with aiofiles.open(file, 'w', encoding="utf-8") as f:
        await f.write(data) # Continue on other write tasks while waiting for this write task to complete


# This is a corountine main function that executes all sub-coroutines
async def main(df):
    club_df = pd.DataFrame(columns=['name', 'url'])
    for index, row in df.iterrows():
        try:
            wiki_url = await fetch_wiki_url(row['name']) # Wait for fetch wiki url to be complete before continuing
            file = f'{directory}{row["name"].replace(" ", "_").replace(".", "")}.html'
            wiki_html = await fetch_html(wiki_url)
            await write_file(file, wiki_html) # Write the Wikipedia URL to a text file
            soup = BeautifulSoup(wiki_html, 'lxml')
            info_table = soup.find("table", attrs={"class": "infobox vcard"})
            info_table_data = info_table.tbody.find_all("tr")
            club_info_json = {
                'name': row['name'],
                'url': wiki_url
            }

            for i in range(1, 6):
                club_info_json[info_table_data[i].th.text] = info_table_data[i].td.text

            club_df = club_df.append(club_info_json, ignore_index=True)
        except BaseException:
            print("Error for ", row['name'])


if __name__ == '__main__':
    start = time()
    clubs_list = pd.read_csv("sample_data/football_clubs.txt")
    asyncio.run(main(clubs_list))
    end = time()
    print(f'Execution time for Asyncio : {end - start}')