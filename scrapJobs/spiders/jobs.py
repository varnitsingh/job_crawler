import scrapy
from ..items import ScrapJob
import csv
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class JobSpider(CrawlSpider):
    name = 'jobs'
    allowed_domains = ["jobs.mahindracareers.com"]
    start_urls = [
        'https://jobs.mahindracareers.com/'
    ]

    rules = (Rule(LinkExtractor(allow=(r'go/.*',)), callback='parse_job',follow=True), )

    def parse_job(self, response):
        item = ScrapJob()
        item['data'] = response.css('title::text').extract()
        rows = response.css('tr').get()
        if rows is not None:
            self.parse_tables(response.css('tr'))
        yield item

    def parse_tables(self, rows):
        with open('jobs.csv','a',newline='') as outfile:
            writer= csv.writer(outfile)
            for row in rows:
                cols = row.css('span::text').extract()
                data=[]
                for col in cols:
                    col = col.replace('\t','')
                    col = col.replace('\n','')
                    col = col.replace(' ','')
                    if col == '':
                        continue
                    data.append(col)
                writer.writerow(data)
