import requests
import bs4
import re
import os
import argparse
import configparser


def parse_site(url, selection):
    """Request site, select elements define by selection and return it/them
    as a list"""
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
    """Normalize link, this is needed since some link has http, or www.
    and others doesn't"""
    if link.startswith('http') or link.startswith('https'):
        link = re.sub(r'http[s]?\://', '', link)
    if link.startswith('www.'):
        link = re.sub(r'www.', '', link)
    return link


def get_domain(link):
    """Short hand for splitting a cleaned link and returning the domaen
    ie. en.wikipedia.org"""
    return link.split('/')[0]


def search_google(query):
    """Search google, parse the html and return all result links as a list"""
    payload = {'q': query}
    res = requests.get('https://www.google.dk/search?', params=payload)

    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    results = soup.select('cite')
    hits = []
    for hit in results:
        hits.append(clean_link(hit.text))
    return hits


def print_paragraphs(paragraphs, source):
    """Iterate over a list of paragraphs(strings) pausing after
    each paragraph has been displayed, returns true/false determining whether
    the next source should be displayed if any"""
    for page, paragraph in enumerate(paragraphs):
        if len(paragraph) > 10:  # Skip overly short paragraphs
            try:
                os.system('cls')
                print('{}\n\nSource: {}\nPage: {}/{}'.format(paragraph,
                                                             source, page+1,
                                                             len(paragraphs)))
            except UnicodeEncodeError:
                # sometimes the encoding isn't as we'd like, this can be
                # circumvented with .encode('utf-8') but the output is rarely
                # pretty, so we'll skip it instead, relying on multiple sources
                continue
            u_input = input('print next? y/n: ')
            if u_input == 'n':
                return False
            if u_input == 'b':
                return True
        else:
            continue
    return True


def a_parse():
    """Parse commandline arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="Word you need defined")
    return parser.parse_args()


def parse_hits(hits, config):
    """Parse a list of links returning all those with a known selector as a
    dictionary with url, css selector, domain"""
    valid_hits = []
    for hit in hits:
        domain = get_domain(hit)
        if domain in config:
            context = {"url": hit,
                       "selector": config[domain]["selector"],
                       "domain": domain}
            valid_hits.append(context)
    return valid_hits


config = configparser.ConfigParser()
config.read('config.ini')
args = a_parse()

links = search_google(args.query)
links = parse_hits(links, config)


cont = True
for link in links:
    if cont:
        paragraphs = parse_site(link["url"], link["selector"])
        cont = print_paragraphs(paragraphs, link["domain"])
    else:
        break
