Craigslist price recommendations
===============
- Crawl a category of Craigslist.
- Identify and extract some metadata for the objects (using for example jsoup) including the price.
- Index the information into elasticsearch (or another search engine of your choice).
- Create an interface where you can search for an object and be presented with price statistics (for example using facets in the search engine); lowest, highest, average and mean price. 

## Setup (Python 3.6)
```sh
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```
