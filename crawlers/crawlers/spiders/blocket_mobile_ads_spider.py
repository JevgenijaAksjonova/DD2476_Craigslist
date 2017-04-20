import scrapy


class BlocketSpider(scrapy.Spider):
    name = "blocket_mobile"

    def start_requests(self):
        urls = [
            'https://www.blocket.se/stockholm?q=&cg=5060&w=3&st=s&c=&ca=11&is=1&l=0&md=th',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for row in response.css('.item_row'):
            try:
                title_h1 = row.css('h1.media-heading')
                title = title_h1.css('a ::text').extract_first()
                price = (row.css('p.list_price ::text').extract_first()).replace(" ", "")[:-2] # Remove whitespaces and :-
                obj = {
                        'title': title,
                        'price': price
                        }
                print(obj) # This should be served to elasticsearch
            except AttributeError:
                pass

        next_page = response.xpath('//ul[@id="all_pages"]/li[contains(.,"Nästa")]/a/@href').extract_first()
        print(next_page)
        if next_page is not None:
            next_page = response.urljoin(next_page)
            print(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
