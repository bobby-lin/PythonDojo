import requests
import pandas as pd
import json
from time import time
from bs4 import BeautifulSoup

directory = "output/"


def fetch_wiki_url(club_name):
    url = f'https://api.duckduckgo.com/?q={club_name}+Wikipedia&format=json'
    response = requests.get(url)
    club_data_json = json.loads(response.text)
    return club_data_json['AbstractURL']


def fetch_html(url):
    response = requests.get(url)
    return str(response.text)


def write_file(name, data):
    file = f'{directory}{name.replace(" ", "_").replace(".", "")}.html'
    with open(file, 'w', encoding="utf-8") as f:
        f.write(data)


def main(df):
    df['url'] = df.apply(lambda row: fetch_wiki_url(row['name']), axis=1)
    df.apply(lambda row: write_file(row['name'], row['url']), axis=1)
    club_df = pd.DataFrame(columns=['name', 'url'])

    for index, row in df.iterrows():
        try:
            wiki_html = fetch_html(row['url'])
            soup = BeautifulSoup(wiki_html, 'lxml')
            info_table = soup.find("table", attrs={"class": "infobox vcard"})
            info_table_data = info_table.tbody.find_all("tr")
            club_info_json = {
                'name': row['name'],
                'url': row['url']
            }

            for i in range(1, 6):
                club_info_json[info_table_data[i].th.text] = info_table_data[i].td.text

            club_df = club_df.append(club_info_json, ignore_index=True)
        except BaseException:
            print("Error for", row['name'])

    print(club_df)


if __name__ == '__main__':
    start = time()
    clubs_list = pd.read_csv("sample_data/football_clubs.txt")
    main(clubs_list)
    end = time()
    print(f'Execution time for Synchronous: {end - start}')