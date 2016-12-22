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
* en.wikipedia.org
* merriam-webster.com
* dictionary.com
* thefreedictionary.com
* vocabulary.com


### Danish
* ordnet.dk
* da.wikipedia.org
* sproget.dk

(Language sort function will be added)
## Requirements
You can install requirements with pip
```
py -m pip install -r requirements.txt
```
* BeautifulSoup4
* Requests