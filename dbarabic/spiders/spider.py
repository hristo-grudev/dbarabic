import scrapy

from scrapy.loader import ItemLoader

from ..items import DbarabicItem
from itemloaders.processors import TakeFirst


class DbarabicSpider(scrapy.Spider):
	name = 'dbarabic'
	start_urls = ['https://www.db.com/mea/arabic/content/2022.htm']

	def parse(self, response):
		post_links = response.xpath('//a[@class="font5 block"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//*[(@id = "leftNavi")]/ul//ul//a/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h2[@id="newsPageHeadline"]/text()').get()
		description = response.xpath('//div[@class="rdtextfield"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@id="cc_02a_NewsArticle"]/text()').get()

		item = ItemLoader(item=DbarabicItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
