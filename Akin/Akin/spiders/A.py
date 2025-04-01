import json

import scrapy


class ASpider(scrapy.Spider):
    name = "A"
    start_urls = ["https://www.akingump.com/_site/search?f=0&v=attorney"]

    def parse(self, response):
        data = json.loads(response.text)
        data = data["hits"]["ALL"]['total']
        for i in range(0,int(data), 12):
            each_page = f'https://www.akingump.com/_site/search?f={i}&v=attorney'
            yield response.follow(url=each_page, callback=self.parse_pages)

    def parse_pages(self, response):
        data = json.loads(response.text)
        data = data["hits"]["ALL"]["hits"]
        for i in data:
            name = i["name"]
            try:
                phone =i["offices_info"]#
                phone = phone[0]['repeater_module_office']["phone"]
            except:
                phone = ''
            try:
                email = i["email"]
            except:
                email = ''
            yield {
                'Name': name,
                'Phone': phone,
                'Email': email
            }
            # print(phone)