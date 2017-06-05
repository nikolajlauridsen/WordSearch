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
        return {"encoding": "NA",
                "content": []}

    site = bs4.BeautifulSoup(res.text, 'html.parser')
    content = site.select(selection)

    if type(content) == list:
        elements = {"encoding": res.encoding,
                    "content": [item.text for item in content]}
    else:
        elements = {"encoding": res.encoding,
                    "content": [content.text]}
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


def search_google(args):
    """Search google, parse the html and return all result links as a list"""
    if args.synonym:
        query = args.query + " synonyms"
    else:
        query = "define " + args.query

    payload = {'q': query, 'num': '25'}
    try:
        res = requests.get('https://www.google.dk/search?', params=payload)
        res.raise_for_status()
    except:
        sys.exit('Google not responding, check your internet')

    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    results = soup.select('cite')

    return [clean_link(hit.text) for hit in results]


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
    while page_n < len(pages["content"]):
        if len(pages["content"][page_n]) > 10:  # Skip overly short pages
            clear_screen()
            try:
                print('{}\n'.format(pages["content"][page_n]))
            except UnicodeEncodeError:
                print('{}\n'.format(
                    str(pages["content"][page_n].encode(pages["encoding"],
                                                        "replace"))))

            print('Page: {}/{}'.format(page_n + 1, len(pages["content"])))
            print('Source {}/{}: {}'.format(n, n_sources, source))

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
                if page_n < len(pages["content"])-1:
                    page_n += 1
                else:
                    return True
        else:
            page_n += 1
    return True


def create_list(word_list, divider="- ", space=4):
    """Convert at list of words to a neatly formatted string"""
    max_width = 0
    # Find the width of the largest element in the word_list + the divider
    for entry in word_list["content"]:
        entry = entry.strip("\n").strip("\t").strip(" ")
        total_length = len(entry) + len(divider)
        if total_length > max_width:
            max_width = total_length

    if max_width > 15:
        columns = 3
    else:
        columns = 4

    string_list = []

    for entry in word_list["content"]:
        list_element = ""
        list_element += divider + entry
        while len(list_element) < max_width:
            list_element += " "
        string_list.append(list_element)

    return_string = ""
    for i, entry in enumerate(string_list, start=1):
        return_string += entry + " "*space
        if i % columns == 0:
            return_string += "\n"

    return return_string


def print_list(elements, source, word, place, total):
    """Print a list of scraped definitions"""
    clear_screen()
    try:
        print(create_list(elements))
    except UnicodeEncodeError:
        print(str(create_list(elements).encode(elements["encoding"],
                                               'replace')))

    print("\nSynonyms for " + word)
    print("Source {}/{}: {}".format(place, total, source))

    u_input = input("\ne: end script\n")
    if u_input == "e":
        return False
    else:
        return True


def a_parse():
    """Parse commandline arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="Word you need defined")
    parser.add_argument("-s", "--synonym", help="Look up synonyms",
                        action="store_true", default=False)
    return parser.parse_args()


def parse_hits(hits, config, synonym=False):
    """Parse a list of links returning all those with a known selector as a
    dictionary with url, css selector, domain"""
    valid_hits = []
    for hit in hits:
        domain = get_domain(hit)
        if domain in config:
            if config[domain]["syn"] == "false" and not synonym:
                context = {"url": hit,
                           "selector": config[domain]["selector"],
                           "domain": domain}
                valid_hits.append(context)
            elif config[domain]["syn"] == "true" and synonym:
                context = {"url": hit,
                           "selector": config[domain]["selector"],
                           "domain": domain}
                valid_hits.append(context)
    return valid_hits


def main():
    # Read config and commandline args
    config = configparser.ConfigParser()
    config.read('config.ini')
    args = a_parse()

    print('Googling that for you...')
    # Search google and extract result links
    # Sort out all domains not in config.ini
    links = parse_hits(search_google(args), config, synonym=args.synonym)

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
                if len(pages) > 0 and args.synonym:
                    cont = print_list(pages, source["domain"], args.query,
                                      n + 1, len(links))
                elif len(pages) > 0 and not args.synonym:
                    # If any definition was found enter the print pages loop
                    cont = print_pages(pages, source["domain"],
                                       n + 1, len(links))
                else:  # Source depleted, fetch next source if any
                    continue
            else:  # User stopped the script
                break
        else:  # Wrong language, fetch next source if any
            continue

if __name__ == '__main__':
    main()
