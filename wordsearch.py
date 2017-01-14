import requests
import bs4
import re
import os
import argparse
import configparser
import sys


def parse_site(url, selection):
    """Request site, select elements define by selection and return it/them
    as a list"""
    try:
        res = requests.get('http://' + url)
        res.raise_for_status()
    except:
        print('Can\'t connect to source')
        return []
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
    """Normalize source, this is needed since some source has http, or www.
    and others doesn't"""
    if link.startswith('http') or link.startswith('https'):
        link = re.sub(r'http[s]?://', '', link)
    if link.startswith('www.'):
        link = re.sub(r'www\.', '', link)
    return link


def get_domain(link):
    """Short hand for splitting a cleaned source and returning the domaen
    ie. en.wikipedia.org"""
    return link.split('/')[0]


def search_google(query):
    """Search google, parse the html and return all result links as a list"""
    payload = {'q': query, 'num':'25'}
    try:
        res = requests.get('https://www.google.dk/search?', params=payload)
        res.raise_for_status()
    except:
        sys.exit('Google not responding, check your internet')

    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    results = soup.select('cite')
    hits = []
    for hit in results:
        hits.append(clean_link(hit.text))
    return hits


def clear_screen():
    """Clears the commandline window"""
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def print_pages(pages, source, n, n_sources):
    """Iterate over a list of pages(strings) pausing after
    each paragraph has been displayed, returns true/false determining whether
    the next source should be displayed if any"""
    page_n = 0
    while page_n < len(pages):
        if len(pages[page_n]) > 10:  # Skip overly short pages
            try:
                clear_screen()
                print('{}\n'.format(pages[page_n]))
                print('Page: {}/{}'.format(page_n + 1, len(pages)))
                print('Source {}/{}: {}'.format(n, n_sources, source))
            except UnicodeEncodeError:
                # sometimes the encoding isn't as we'd like, this can be
                # circumvented with .encode('utf-8') but the output is rarely
                # pretty, so we'll skip it instead, relying on multiple sources
                page_n += 1
                continue
            u_input = input('\ne: end script | n: next source | b: back\n:> ')
            if u_input.lower() == 'e':
                return False
            if u_input.lower() == 'n':
                return True
            elif u_input.lower() == 'b':
                if page_n > 0:
                    page_n -= 1
                else:
                    page_n = 0
            else:
                if page_n < len(pages)-1:
                    page_n += 1
                else:
                    return True
        else:
            page_n += 1
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
config.read('D:\Github\WordSearcher\config.ini')
args = a_parse()

print('Googling that for you...')
links = search_google(args.query)  # Search google and extract result links
links = parse_hits(links, config)  # Sort out all domains not in config.ini

if len(links) < 1:
    sys.exit('No definition found')

cont = True
for n, source in enumerate(links):
    if config[source["domain"]]["lang"] == config["DEFAULT"]["lang"] \
            or config["DEFAULT"]["lang"] == "all":
        if cont:
            print('Looking up source...')
            # Request site and extract word definiton from it using
            # the selector in config.ini, one definition element is a pages
            pages = parse_site(source["url"], source["selector"])
            if len(pages) > 0:
                # If any definition was found enter the print pages loop
                cont = print_pages(pages, source["domain"], n + 1, len(links))
            else:
                continue
        else:
            break
    else:
        continue
