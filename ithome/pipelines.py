# -*- coding: utf-8 -*-

import mysql.connector as mysql_conn
from elasticsearch import Elasticsearch
import time
from datetime import datetime

from settings import MYSQL, Mysql_TableName, ES, ES_INDICES
class IthomePipeline(object):
    def process_item(self, item, spider):
        self.env  = spider.env
        self.conn = mysql_conn.connect(**MYSQL[self.env])
        self.es   = Elasticsearch([ES[self.env]])
        log = item['Log']
        #171220.K.Y.:查看資料庫,確認log需要新增或更新
        if self.should_log_update(log):
            self.update_log(item)
        else:
            self.create_log(item)
        self.add_doc(item)
        return item

    def should_log_update(self, log):
        cursor = self.conn.cursor()
        should_log_update_command = """SELECT COUNT(*) FROM {0} WHERE id = '{1}'"""\
        .format(Mysql_TableName['db_table'], log['Id'])
        cursor.execute(should_log_update_command)
        cam_num = map(lambda x: x[0], cursor.fetchall())[0]
        cursor.close()
        if cam_num == 0:
            return False
        return True

    def create_log(self, item):
        insert_command = \
            """INSERT INTO {0} (id, url, title, crawled_time)
                VALUES ('{1}', '{2}', '{3}', {4});"""\
            .format(Mysql_TableName['db_table'], item['Log']['Id'], item['Url'], item['Title'], item['Log']['Crawled_Time'])
        cursor = self.conn.cursor()
        cursor.execute(insert_command)
        self.conn.commit()
        cursor.close()

    def update_log(self, item):
        update_command = """UPDATE {0} SET url='{1}', title='{2}', crawled_time={3} WHERE id='{4}'"""\
             .format(Mysql_TableName['db_table'], item['Url'], item['Title'], item['Log']['Crawled_Time'], item['Log']['Id'])
        cursor = self.conn.cursor()
        cursor.execute(update_command)
        self.conn.commit()
        cursor.close()

    def add_doc(self, item):
        doc_type = 'Security'
        fb = item['Facebook']
        Id = item['Log']['Id']
        del item['Log']
        del item['Facebook']
        data = {
            'Ithome' : dict(item),
            'Facebook' : dict(fb)
            }
        es_search = self.es.search(
            index=ES_INDICES[self.env], 
            doc_type=doc_type,
            body={"query":  { 'match': { '_id': Id }}})
        #171220.K.Y.:若es中沒有這筆資料進行create,若有查看fb update_time已確認是否需要update
        if es_search['hits']['total'] == 0:
            self.es.create(
                index=ES_INDICES[self.env], 
                doc_type=doc_type,
                body=data, id=Id)
        elif es_search['hits']['hits'][0]['_source']['Facebook']['Update_Time'] != fb['Update_Time']:
            self.es.update(
                index=ES_INDICES[self.env], 
                doc_type=doc_type, 
                body=data, id=Id)