#-*- coding: UTF-8 -*-
import time

import requests,sys,os
from threading import Thread, activeCount
import Queue
from gevent import monkey,pool
import gevent
monkey.patch_all()
#github:https://github.com/sulab999/webpathscan

queue = Queue.Queue()

jobs = []
# 读取字典文件
lines=open("dir.txt",'r')
for line in lines:
    line=line.strip()
    queue.put(line)
domain = []
# 读取查询域名
all_domain = open('domain.txt', 'r').readlines()
for line in all_domain:
    domain.append(line)


def scan_target_url_exists(target_url):

    headers={

        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',

        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',

        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',

        'Accept-Encoding': 'gzip, deflate',

        'Referer': 'http://www.google.com'}

    status_codes = [200]
    while not queue.empty():
        try:
            path=queue.get()
            if path.startswith("/"):
                url="%s%s" % (target_url.strip('\n'),path)
                print url
            else:
                url="%s/%s" % (target_url.strip('\n'),path)
                print url

            req=requests.head(url,timeout=1,headers=headers)

            if req.status_code in status_codes:

                print 'CODE:%s,URL:%s\n'%(str(req.status_code),url.strip('\n').strip('\r'))

                open('exists_target_url.txt','a').write(url)

        except:
            # print 'fail'
            pass

def show():
    print u"use: python scandir.py 线程数"
    print u"将域名放到domain.txt文件中"

if __name__ == '__main__':
    if len(sys.argv) < 2:
        show()
        sys.exit()

    print '''
    
   _____ _    _ _               ____  
  / ____| |  | | |        /\   |  _ \ 
 | (___ | |  | | |       /  \  | |_) |
  \___ \| |  | | |      / /\ \ |  _ < 
  ____) | |__| | |____ / ____ \| |_) |
 |_____/ \____/|______/_/    \_\____/


    '''

    p = pool.Pool(int(sys.argv[1]))
    if os.path.exists("exists_target_url.txt"):
        os.remove("exists_target_url.txt")


    for i in domain:
        jobs.append(p.spawn(scan_target_url_exists,i))
    gevent.joinall(jobs)


