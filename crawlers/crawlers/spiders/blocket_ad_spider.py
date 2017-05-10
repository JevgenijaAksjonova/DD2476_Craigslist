import scrapy
import re


class BlocketSpider(scrapy.Spider):
    name = "blocket_mobile_with_text"
    whitespace = re.compile(r'[^\S ]+')
    parenthesis = re.compile(r'[()]')
    
    def start_requests(self):
        urls = [
            'https://www.blocket.se/stockholm?q=&cg=5060&w=3&st=s&c=&ca=11&is=1&l=0&md=th',
#            'https://www.blocket.se/stockholm/telefoner_tillbehor/telefoner?cg=5060&w=1&st=s&ca=11&is=1&l=0&md=th&c=5061',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        data_application_name = response.xpath('//body/@data-application-name').extract_first()
        # if it is the list view
        if data_application_name == "list_ads":
            for row in response.css('.item_row'):
                try:
                    title_h1 = row.css('h1.media-heading')
                    url = title_h1.css('a::attr(href)').extract_first()
                    if url is not None:
                        yield scrapy.Request(url=url, callback=self.parse)
                except AttributeError:
                    pass

            # Yield the next page of listed ads
            next_page = response.xpath('//ul[@id="all_pages"]/li[contains(.,"Nästa")]/a/@href').extract_first()
            print(next_page)
            if next_page is not None:
                next_page = response.urljoin(next_page)
                print(next_page)
                yield scrapy.Request(next_page, callback=self.parse)

        elif data_application_name == "view_ad":

            uid = int(response.url.split('?')[-2].split('.htm')[-2].split('_')[-1])
            main = response.css('main')

            header = main.xpath('.//header[@class="row"]')
            title = main.css('h1.h3::text').extract_first().strip()
            publish_date = header.xpath('.//time/@datetime').extract_first()
            price = header.xpath('.//div[@id="vi_price"]/text()').extract_first()
            price = int(price.strip()[:-2].replace(" ", "")) # remove all whitespace and :- and convert to integer
            ad_texts = main.xpath('//div[contains(@class,"body")]/text()').extract() # get text fragments
            ad_texts = [self.whitespace.sub(" ", a.strip()) for a in ad_texts] # remove unnecessary whitespace
            ad_texts = [a for a in ad_texts if not a == ""] # filter out empty strings
            ad_text = "\n".join(ad_texts) # join the text fragments with a new line between each
            location = header.xpath('.//span[@class="area_label"]/text()').extract_first()
            location = location.strip()[1:-1] # remove prefix and suffix whitespace and parenthesis around location name
            item = {
                    'uid': uid,
                    'title': title,
                    'price': price,
                    'datetime': publish_date,
                    'ad_text': ad_text,
                    'loc_name':location,
                    }

            yield item




