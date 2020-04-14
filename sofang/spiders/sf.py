# -*- coding: utf-8 -*-
import re

import scrapy
# from scrapy_redis.spiders import RedisSpider

from sofang.items import NewHouseItem


class SfSpider(scrapy.Spider):
    name = 'sf'
    allowed_domains = ['fang.com']
    start_urls = ['https://www.fang.com/SoufunFamily.htm']

    # redis_key = 'sofang:start_urls'

    def parse(self, response):
        trs = response.xpath('//tr[contains(@id, "sffamily_B03")]')
        province = ''
        for tr in trs:

            province = tr.xpath('./td[2]//text()').get().strip()
            if province:
                province_name = province
            if province_name == '其它' or province_name == '台湾':
                continue
            citys = tr.xpath('./td[3]/a')
            for city in citys:
                city_name = city.xpath('./text()').get()
                if city_name == '北京':
                    continue
                city_url = city.xpath('./@href').get().strip()

                city_short = re.search(r'^.*://(.*?).fang.com/?$', city_url).group(1)
                city_url_new = 'https://{}.newhouse.fang.com/house/s/'.format(city_short)
                city_url_esf = 'https://{}.esf.fang.com/'.format(city_short)
                # 发送新房链接
                yield scrapy.Request(url=city_url_new, callback=self.parse_new,
                                     meta={'info': (province_name, city_name)})

    def parse_new(self, response):
        province, city = response.meta.get('info')
        lis = response.xpath('.//div[contains(@class, "nl_con")]/ul/li')
        for li in lis:
            if not li.xpath('.//div[contains(@class, "nlcd_name")]/a//text()').get():
                continue
            name = li.xpath('.//div[contains(@class, "nlcd_name")]/a//text()').get().strip()
            price = li.xpath('.//div[@class="nhouse_price"]//text()').getall()
            price = list(map(lambda x: x.strip(), price))
            price = ''.join(price)
            origin_url = response.url
            item = NewHouseItem(
                province=province,
                city=city,
                name=name,
                price=price,
                origin_url=origin_url
            )
            yield item
        # 判断是否有下一页
        next_page = response.xpath('//*[@id="sjina_C01_47"]//a[@class="next"]')
        if next_page:
            next_page_url = next_page.xpath('./@href').get()
            next_page_url = response.urljoin(next_page_url)
            # 发送新房链接
            yield scrapy.Request(url=next_page_url, callback=self.parse_new,
                                 meta={'info': (province, city)})
