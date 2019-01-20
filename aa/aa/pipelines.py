# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymysql

from twisted.enterprise import adbapi
import pymysql.cursors

class likesPipeline(object):#处理likes的pipeline
    def process_item(self, item, spider):
        try:
            temp=json.loads(item['likes'][0].replace("\'",'\"'))
            item['likes'] = [str(temp['note']['likes_count'])]
        except KeyError:
            item['likes']=['0']
        print(item)
        return item


class SqlPipeline(object):#构造sql语句并执行即可

    def process_item(self,item,spider):
        '''item={'author': ['城北听雪'],
        'imageurl': ['http://upload-images.jianshu.io/upload_images/14074951-f700da6a9b168924.jpg'],
        'likes': ['33'],
        'noteid': ['https://www.jianshu.com/p/3e652aafb69b'],
        'title': ['5天流浪加德满都，给你看一个不一样的真实尼泊尔']}'''
        a={ k:v[0] for k,v in item.items()}#构造字符串
        str1 = ",".join([i for i in a.keys()])
        str2 = "','".join([i for i in a.values()])
        sql="INSERT INTO jianshu ({0}) VALUES ('{1}')".format(str1,str2)#构造sql
        conn=pymysql.connect(host='127.0.0.1',port=3306,user='root',db='jobol',password='1118',charset='utf8mb4')
        cur=conn.cursor()
        try:
            cur.execute(sql)
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(e)
        finally:
            cur.close()
            conn.close()
        return item


class asyPipeline(object):
    def __init__(self,dbpool):#默认传入一个连接池
        self.dbpool=dbpool

    @classmethod#声明一个类方法
    def from_settings(cls,settings):
    #注意是settings有S这个类方法和实例没有关系,接受一个setting也就是我们的配置文件
    #把变量拿过来，传入adbpool里面定义一个dbpool
        dbpool=adbapi.ConnectionPool('pymysql',
                                     host=settings['MYSQL_HOST'],
                                     db=settings['DB_NAME'],
                                     user=settings['MYSQL_USER'],
                                     password=settings['MYSQL_PASSWOED'],
                                     charset=settings['CHARSET'],
                                     cursorclass=pymysql.cursors.DictCursor,
                                     use_unicode=True)
    #这里可以写死也可以用这个方法读取setting里面的配置信息(建议)
        return cls(dbpool=dbpool)

    def process_item(self,item,spider):

        query=self.dbpool.runInteraction(self.do_insert, item)
        #执行，相当于loop启动，定义一个变量来代表
        query.addErrback(self.handler)
        #制定错误处理函数

    def do_insert(self,cursor,item):
        '''执行查询的函数'''
        a = {k: v[0] for k, v in item.items()}  # 构造字符串
        str1 = ",".join([i for i in a.keys()])
        str2 = "','".join([i for i in a.values()])
        sql = "INSERT INTO jianshu ({0}) VALUES ('{1}')".format(str1, str2)  # 构造sql
        cursor.execute(sql)

        #不能用try异步没有try
    def handler(self,failure):#定义错误处理
        print(failure)#打印错误



class MongoPipeline(object):
    def process_item(self,item,spider):
        print('插入mongo')


class JsonPipeline(object):
    def process_item(self,item,spider):
        a = {k: v[0] for k, v in item.items()}#格式化一下
        with open(r'jianshu.json','a',encoding='utf-8') as f:
            json.dump(a,f,ensure_ascii=False)
            f.write('\n')
