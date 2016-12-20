import requests
import bs4
import re


def parse_ordnet(link):
    res = requests.get('http://www.' + link)
    ordnet = bs4.BeautifulSoup(res.text, 'html.parser')
    definition = ordnet.select('.definition')
    try: 
        print(definition.text)
    except AttributeError:
        print(definition[0].text)


def parse_wiki(link):
    #print('https://' + link)
    res = requests.get('https://' + link)
    print(res.url)
    wiki = bs4.BeautifulSoup(res.text, 'html.parser')
    content = wiki.select('#mw-content-text p')
    print('{}\n{}'.format(content[0].text, content[1].text))


def parse_site(link, selection):
    res = requests.get('http://' + link)
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


#Replace with config object
WHITELIST = ['ordnet.dk', 'da.wikipedia.org', 'en.wikipedia.org', 'sproget.dk', 'denstoredanske.dk']

query = input('Query: ')
payload = {'q':query}
res = requests.get('https://www.google.dk/search?', params=payload)
# print('Status code: ' + str(res.status_code))

soup = bs4.BeautifulSoup(res.text, 'html.parser')

links = soup.select('cite')

for ele in links:
    link = clean_link(ele.text)
    domain = link.split('/')[0]
    # if domain in WHITELIST: print('{}\n{}\n'.format(link, domain))
    if domain == 'ordnet.dk':
        paragraphs = parse_site(link, '.definition')
        print(paragraphs)
    elif domain == 'da.wikipedia.org':
        paragraphs = parse_site(link, "#mw-content-text p")
        print(paragraphs)

print('Elements: ' + str(len(links)))
print(str(res.request.url))



