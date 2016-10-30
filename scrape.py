import re
import requests
from bs4 import BeautifulSoup

arrowURL = "http://www.arrow.nl/acties/actie/42/Arrow_Rock_500_lijst"
PATH = "top500.txt"


def crawl(url):
    urls = get_list_per_day_urls(url)
    print(urls)
    tracks = get_list(urls)
    top500 = clean(tracks)
    print_to_file(top500)


def get_list_per_day_urls(url):
    list_per_day_urls = []
    soup = parse(url)

    for u_item in soup.find_all("u"):
        a_item = u_item.find("a")
        if a_item is not None:
            list_per_day_urls.append(a_item.get('href'))

    return list_per_day_urls


def get_list(urls):
    track_list = []

    for url in urls:
        print(url)
        soup = parse(url)
        news_content = soup.find("div", {"class": "newsContent"})

        for div in news_content.find_all("strong"):
            track_list.append(div.get_text())

    return track_list


def clean(tracks):
    clean_tracks = []
    for track in tracks:
        clean_tracks.append(remove_non_tracks(remove_front_numbers(remove_enters(remove_hex_characters(track.strip())))).strip())

    return clean_tracks


def remove_front_numbers(track):
    return re.sub(r"", "", track)


def remove_hex_characters(track):
    return track[3:]


def remove_enters(track):
    return re.sub(r'\n', "", track)


def remove_non_tracks(track):
    if "PLAYLIST" not in track:
        return track
    else:
        return ""


def parse(url):
    source = requests.get(url).text
    return BeautifulSoup(source, "html.parser")


def print_to_file(tracks):
    file = open(PATH, 'w')
    for track in tracks:
        file.writelines(track + "\n")
    file.close()


crawl(arrowURL)
