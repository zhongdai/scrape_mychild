# -*- coding: utf-8 -*-
import scrapy
import string
from scrapy.http import Request
from childcare.items import ChildcareItem


class MychildcareSpider(scrapy.Spider):
    name = "mychildcare"
    allowed_domains = ["ifp.mychild.gov.au"]
    # remove comment for below line to do a quick run
    # start_urls = ['http://ifp.mychild.gov.au/Search/AZSearch.aspx?Location=Z']

    # if use below line, it takes about 2 hours to complete
    start_urls = ['http://ifp.mychild.gov.au/Search/AZSearch.aspx?Location=' + alpha for alpha in string.ascii_uppercase[:26]]

    def parse(self, response):
        urls = response.xpath('//ul[@id="AZsuburbList"]/li/a/@href').extract()
        for i, url in enumerate(urls):
            yield Request(url=response.urljoin(url),
                          dont_filter=True,
                          meta={'cookiejar': i},
                          callback=self.parse_search_result)

    def parse_search_result(self, response):
        url = '/mvc/PrintResults/PrintChildCareResults'
        yield Request(url=response.urljoin(url),
                      dont_filter=True,
                      meta={'cookiejar': response.meta['cookiejar']},
                      callback=self.parse_item)


    def parse_item(self, response):
        for item in response.xpath('//div[starts-with(@class, "rpMain")]'):
            cc = ChildcareItem()
            cc['name'] = item.xpath(
                './/div[@class="resultItemHeader"]/span/text()').extract_first()

            details = item.xpath(
                './/div[@class="resultItemDetail"]/span[1]/text()').extract()

            addtional = item.xpath(
                './/div[@class="resultItemDetail"]/div[@class="resultItemPadded"]/text()').extract()

            details.extend(addtional)

            if len(details) >= 2:
                # only process items with category and address, they are always
                # in the 1st and 2nd place
                cc['category'] = details[0]
                cc['address'] = details[1]

                # append more if possible
                for info in details:
                    info = info.strip()
                    if info.startswith('Phone'):
                        cc['phone'] = info.split(':')[1].strip()
                    if info.startswith('Email'):
                        cc['email'] = info.split(':')[1].strip()
                    if info.startswith('Web'):
                        cc['web'] = info[info.index('http'):].strip()
            yield cc
