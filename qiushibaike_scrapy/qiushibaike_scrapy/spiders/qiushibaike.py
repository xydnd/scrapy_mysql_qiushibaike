from urllib import parse
from pkg_resources import yield_lines
from pymysql import connect
import scrapy
from qiushibaike_scrapy.items import QiushibaikeScrapyItem

class QiuhsiSpider(scrapy.Spider):
    name = "qiushibaike"
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/73.0.3683.86 Chrome/73.0.3683.86 Safari/537.36'
    # }
    def start_requests(self):
        self.start_urls = [
            "https://www.qiushibaike.com/text/page/1"
        ]
        for url in self.start_urls:
            yield scrapy.Request(url=url,callback=self.parse)

    #解析需要先获取字段---item
    def parse(self, response, **kwargs):
        item = QiushibaikeScrapyItem()      
        #开始解析需要的内容
        article = response.xpath("//div[contains(@class,'col1')]/div[contains(@class,'article')]")
        for cont in article:
            item["author"] = cont.xpath("./div[@class='author clearfix']//a[2]/h2//text()").get().strip()
            item["content"] = ''.join(cont.xpath(".//div[@class='content']//span//text()").getall()).strip()
            item['_id'] = cont.attrib['id']
            yield item

        #获取下一页按钮
        next_page = response.xpath("//ul[@class='pagination']//li[last()]/a").attrib["href"]
        #获取为None时，表示是最后一页
        if next_page is not None:
            yield response.follow(next_page,callback=self.parse)

            

        

        