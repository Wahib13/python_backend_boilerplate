import os
import urllib

import requests
from bs4 import BeautifulSoup

NPA_BASE_URL = os.environ.get('NPA_BASE_URL')

HYPERLINK_KEYWORDS = ['indicative', 'prices', '-', 'price']


def clean_hyperlink(hyperlink_text: str):
    """
     convert hyperlink to a list of lowercase words for easy comparison with keywords
    :param hyperlink_text:
    :return: cleaned version of hyperlink text
    """
    # remove .xlsx or xls extension
    if len(hyperlink_text.split('.')) > 0:
        if hyperlink_text.split('.')[-1].startswith('xl'):
            hyperlink_text = hyperlink_text.replace(f'.{hyperlink_text.split(".")[-1]}', '')

    hyperlink_text = hyperlink_text.split('/')[-1]
    hyperlink_text = hyperlink_text.replace('_', ' ').replace('%20', ' ').lower()
    hyperlink_list = hyperlink_text.split(' ')
    return hyperlink_list


def get_intersection(text1: list, text2: list):
    return list(set(text1) & set(text2))


def fetch_download_link(html_text):
    """
    scrape from page to get a download link. may return None if no link is not found
    """
    soup = BeautifulSoup(html_text, 'html.parser')
    keyword_count = dict(map(lambda hyperlink:
                             (len(get_intersection(clean_hyperlink(hyperlink.get('href')), HYPERLINK_KEYWORDS)),
                              hyperlink),
                             soup.find_all('a')))
    # keyword_count = {2: '/home/price/download/', 1: '/pre/price/'}
    final_link = keyword_count.get(max(keyword_count))
    return final_link.get('href')


def fetch_latest_link():
    """
    call functions to scrape from both the home and download page and compare which one is more recent and return that
    """
    response = requests.get(NPA_BASE_URL)
    html_text = response.text
    download_link = fetch_download_link(html_text)
    return urllib.parse.urljoin(NPA_BASE_URL, download_link)
