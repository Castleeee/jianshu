# # import pymysql
# # a ={'author': ['城北听雪'],
# #  'imageurl': ['http://upload-images.jianshu.io/upload_images/14074951-f700da6a9b168924.jpg'],
# #  'likes': ['33'],
# #  'noteid': ['https://www.jianshu.com/p/3e652aafb69b'],
# #  'title': ['5天流浪加德满都，给你看一个不一样的真实尼泊尔']}
# # a={ k:v[0] for k,v in a.items()}
# # str1=",".join([i for i in a.keys()])
# # str2="','".join([i for i in a.values()])
# # print(str1,str2)
# # sql="INSERT INTO jianshu ({0}) VALUES ('{1}')".format(str1,str2)
# # print(sql)
# # conn=pymysql.connect(host='127.0.0.1',port=3306,user='root',db='jobol',password='1118',charset='utf8mb4')
# # cur=conn.cursor()
# # try:
# #     cur.execute(sql)
# # except Exception as e:
# #     conn.rollback()
# #     print(e)
# # finally:
# #     cur.close()
# #     conn.close()
# # import json
# #
# # with open(r'jianshu.json', 'a') as f:
# #     for i in range(2):
# #         json.dump(a,f,ensure_ascii=False)
# import multiprocessing
# from multiprocessing import Queue,Pipe,Manager,Lock,Process
# import time
#
# def putit(q):
#     q['a']='aaa'
#     #q.put([1,2,3])
#     #print(q.qsize())
#
# def getit(q):
#     time.sleep(2)
#     print(q['a'])
#     #print(q.get())
#     #print(q.qsize())
#
# if __name__ == '__main__':
#     Q = Queue()  # 在使用进程池的时候，会出错，使用manage.Queue()
#     P = Pipe(False)  # 设置为False就是单向队列
#     M = Manager()
#     D = M.dict()
#     MQ = M.Queue()
#     # a = Process(target=putit, args=(Q,))
#     # b = Process(target=getit, args=(Q,))
#     a = Process(target=putit, args=(D,))
#     b = Process(target=getit, args=(D,))
#     a.start()
#     b.start()
#     a.join()
#     b.join()
#
#-*-coding:utf-8-*-
#SettingCode here
__author__ = "a_little_rubbish"
__date__ = "2019/1/16 11:07"

#import your model here
import requests
#your class&function here

if __name__ == "__main__":
    header = {'Referer': 'https://www.jianshu.com',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}

    res=requests.get(url='https://www.jianshu.com/p/b3bb4e9c232e',headers=header)
    res.encoding='utf-8'
    print(res.text)
