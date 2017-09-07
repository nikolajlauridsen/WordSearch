# What does that word mean?
Commandline tool for looking up words.

Simply launch the script with your query like so:
#### Definition
```
py wordsearch.py query
```

#### Synonym
```
py wordsearch.py -s query
```

The script will then google it for you and look through supported sites 
for your answer

# Supported sites
## Word definitions
### English
* [en.wikipedia.org](https://en.wikipedia.org/wiki/Main_Page)
* [merriam-webster.com](https://www.merriam-webster.com/)
* [dictionary.com](http://www.dictionary.com/)
* [thefreedictionary.com](http://www.thefreedictionary.com/)
* [vocabulary.com](https://www.vocabulary.com/)


### Danish
* [ordnet.dk](http://ordnet.dk/)
* [da.wikipedia.org](https://da.wikipedia.org/wiki/Forside)
* [sproget.dk](http://sproget.dk/)

## Synonyms
### English
* [thesaurus.com](http://www.thesaurus.com/)
* [synonym.com](http://www.synonym.com/)

# Sorting languages
To only show english results edit line 3 in config.ini to change language sorting like so:

#### before:

```INI
[DEFAULT]
selector = p
lang = all
```

#### after:

```INI
[DEFAULT]
selector = p
lang = en
```

# Output looking weird?
Change your consoles encoding to UTF-8 and it should be solved.
On windows you can change your encoding with the following command:
```
chcp 65001
```

# Requirements
You can install requirements with pip
```
py -m pip install -r requirements.txt
```
* BeautifulSoup4
* Requests
