import requests
import bs4
import re
import os


def parse_site(url, selection):
    res = requests.get('http://' + url)
    site = bs4.BeautifulSoup(res.text, 'html.parser')
    content = site.select(selection)
    elements = []
    if type(content) == list:
        for item in content:
            elements.append(item.text)
    else:
        elements.append(content.text)
    return elements


def clean_link(link):
    if link.startswith('http') or link.startswith('https'):
        link = re.sub(r'http[s]?\://', '', link)
    if link.startswith('www.'):
        link = re.sub(r'www.', '', link)
    return link


def get_domain(link):
    return link.split('/')[0]


def search_google(query):
    payload = {'q': query}
    res = requests.get('https://www.google.dk/search?', params=payload)
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    results = soup.select('cite')
    hits = []
    for hit in results:
        hits.append(clean_link(hit.text))
    return hits


def print_paragraphs(paragraphs):
    for paragraph in paragraphs:
        if len(paragraph) > 10:
            try:
                os.system('cls')
                print(paragraph)
            except UnicodeEncodeError:
                continue
            u_input = input('print next?: ')
            if u_input == 'n':
                return False
        else:
            continue
    return True


query = input('Query: ')

links = search_google(query)

cont = True
for link in links:
    if get_domain(link) == 'ordnet.dk' and cont:
        paragraphs = parse_site(link, '.definition')
        cont = print_paragraphs(paragraphs)

    elif (get_domain(link) == 'da.wikipedia.org' or get_domain(link) == 'en.wikipedia.org') and cont:
        paragraphs = parse_site(link, "#mw-content-text p")
        cont = print_paragraphs(paragraphs)

