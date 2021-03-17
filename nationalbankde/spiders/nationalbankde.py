import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from nationalbankde.items import Article


class NationalbankdeSpider(scrapy.Spider):
    allowed_domains = ['national-bank.de']
    name = 'nationalbankde'
    start_urls = ['https://www.national-bank.de/news']

    def parse(self, response):
        links = response.xpath('//a[@class="button minibutton ellipse"]/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        if 'pdf' in response.url:
            return

        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1/text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//span[@class="date"]/text()').get()
        if date:
            date = date.strip()

        content = response.xpath('//div[@class="col-lg-9 col-md-10 col-sm-11 col-xs-12"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
