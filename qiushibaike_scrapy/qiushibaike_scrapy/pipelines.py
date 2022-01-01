# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql

class QiushibaikeScrapyPipeline(object):
    def __init__(self) -> None:
        self.conn = pymysql.connect(host="localhost",user="root",passwd="2552053a",db="qiushi")
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        if not self.conn or not item:
            return
        sql = "insert into t_qiushi values(%s,%s,%s)"
        self.cursor.execute(sql,(item["_id"],item["author"],item["content"]))
        self.conn.commit()
        return item
    
    def __del__(self):
        if self.conn:
            self.conn.close()

