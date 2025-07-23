import json
import sys
# import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ..items  import NikeojectItem
from urllib.parse import urljoin
import scrapy
import re

class NikeSpiderSpider(scrapy.Spider):
    name = 'nike_spider'
    allowed_domains = ['www.nike.com.cn']
    # start_urls = ['http://www.nike.com.cn/']
    start_urls = [
        'https://api.nike.com.cn/cic/browse/v2?queryid=filteredProducts&anonymousId=DSWXE013751DFEFE2A6D30F48D28A05124AC&uuids=&language=zh-Hans&country=CN&channel=NIKE&localizedRangeStr=%7BlowestPrice%7D%20%E2%80%94%20%7BhighestPrice%7D&path=/w/&sortBy=newest',
        'https://api.nike.com.cn/cic/browse/v2?queryid=products&anonymousId=DSWXE013751DFEFE2A6D30F48D28A05124AC&country=cn&endpoint=%2Fproduct_feed%2Frollup_threads%2Fv2%3Ffilter%3Dmarketplace(CN)%26filter%3Dlanguage(zh-Hans)%26filter%3DemployeePrice(true)%26anchor%3D24%26consumerChannelId%3Dd9a5bc42-4b9c-4976-858a-f159cf99c647%26count%3D24%26sort%3DeffectiveStartViewDateDesc&language=zh-Hans&localizedRangeStr=%7BlowestPrice%7D%20%E2%80%94%20%7BhighestPrice%7D'
    ]

    def parse(self, response,**kwargs):
        json1=json.loads(response.text)
        # print(json1)

        try:
            products=json1["data"]["products"]["products"]
        except:
            products = json1["data"]["filteredProducts"]["products"]
        for i in products:
            # print(i)
            yield scrapy.Request(
                url=str(i["url"]).replace("{countryLang}","https://www.nike.com.cn"),
                callback=self.parse_details,
                meta=i
            )
            # break
    def parse_details(self,response):
        # print(response.text)
        # print(response.meta)
        sizes_list=re.findall(r'"sizes":(.+?),"sizeSelectError"',response.text)
        sizes_list1=json.loads(sizes_list[0])
        # print("sizes_list",sizes_list)
        item = NikeojectItem()
        item['title'] = response.meta["title"]
        item['price'] = response.meta["price"]["employeePrice"]
        item['color'] = response.meta["colorDescription"]
        item['size'] = "|".join([
            itemsize.get("localizedLabel", "")
            for itemsize in sizes_list1
            if isinstance(itemsize, dict)
        ])
        item['sku'] = response.meta["productType"]
        item['details'] = response.meta["subtitle"]
        item['img_urls'] = response.meta["images"]["portraitURL"]
        yield item
