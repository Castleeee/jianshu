#-*-coding:utf-8-*-
#SettingCode here
__author__ = "a_little_rubbish"
__date__ = "2019/1/13 9:53"

#import your model here
from scrapy import cmdline
#your class&function here

if __name__ == "__main__":
    cmdline.execute(["scrapy", "crawl", "jianshu"])
