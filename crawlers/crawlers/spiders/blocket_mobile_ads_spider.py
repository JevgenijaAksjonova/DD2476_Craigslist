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
            #$print(row.extract())
            for title in row.css('h1.media-heading'):
                yield {'title': title.css('a ::text').extract_first()}
        #print(response.body)
