# What does that word mean?
Commandline tool for looking up words.

Simply launch the script with your query like so:

```
py wordsearch.py query
```

The script will then google it for you and look through supported sites 
for your answer

## Supported sites
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

(Language sort function will be added)
## Requirements
You can install requirements with pip
```
py -m pip install -r requirements.txt
```
* BeautifulSoup4
* Requests