Craigslist price recommendations
===============
- Crawl a category of Blocket.

https://www.blocket.se/stockholm?q=&cg=5060&w=3&st=s&c=&ca=11&is=1&l=0&md=th
- Identify and extract some metadata for the objects (using for example jsoup) including the price.
- Index the information into elasticsearch (or another search engine of your choice).
- Create an interface where you can search for an object and be presented with price statistics (for example using facets in the search engine); lowest, highest, average and mean price. 

## Setup (Python 3.6)
```sh
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Running the blocket crawler
```sh
cd crawlers
scrapy crawl blocket_mobile
```
