#!/usr/bin/env python3
# -*- coding: utf8 -*-

from selenium import webdriver
import urllib.parse
from bs4 import BeautifulSoup
import requests
import sys
import lxml
import urllib.request
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from selenium.webdriver.common.keys import Keys
import json
import os
import time
import simplejson
import time
import logging
import urllib.request
import urllib.error
from urllib.parse import urlparse
import random
from multiprocessing import Pool
from user_agent import generate_user_agent
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
import re
import logging
import multiprocessing
import os
print(os.environ['PORT'])
print(type(os.environ['PORT']))
print(int(os.environ['PORT']))
##############################################################
#dbx = dropbox.Dropbox('f-KAniQltpAAAAAAAAAAJIbsiXs5GHwPExH3wvTg9HyW1TSWv90WITwbAiYWSOmS')
url_host = 'http://www.pixiv.net/'
url_login = 'https://accounts.pixiv.net/login'
url_post = 'https://accounts.pixiv.net/api/login'
headers_default = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'

    #'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24'
}
#########
'''
s = requests.Session()
    # 访问登陆页，获取Cookie和post_key
print('Visiting %s...' % url_login)
r = s.get(url_login, headers=headers_default)

print('Done結束.')
#print('Cookie:', s.cookies)
soup = BeautifulSoup(r.text, "html.parser")
post_key = soup.find(id="old-login").find(attrs={'name': 'post_key'}).get('value')
#print('post_key:', post_key)

# 登陆
data_post = {
        'mode': 'login',
        'pixiv_id': 'a2304101',
        'password': 'johnny782',
        'post_key': post_key
}
print('Logining中...')

r = s.post(url_post, data=data_post, headers=headers_default)
'''
##############################################################
def pixivsearch(string):
    try:   
        url='https://www.pixiv.net/search.php?s_mode=s_tag&order=popular'
        string=(string+'-').lower()
        keyword=(re.findall('p-s(.*?)-', string))[0]
            
        sex=re.findall('-g(.*?)-', string[3+len(keyword):])
        if sex==['b']:
            url=url+'_male'
        if sex==['g']:
            url=url+'_female'
        url=url+'_d'

        r18=re.findall('-r(.*?)-', string[3+len(keyword):])
        if r18==['18']:    
            url=url+'&mode=r18'
        if r18==['n18']:        
            url=url+'&mode=safe'
        url=url+'&word='+keyword+'&p='

        page=re.findall('-p(.*?)-', string[3+len(keyword):])
        if page!=[]: 
            url=url+page[0]
        if page==[]:
            url=url+str(random.choice([1,2,3]))

        item=re.findall('-i(.*?)-', string[3+len(keyword):])
        if item!=[]:
            item=item[0]
        
        #url='https://www.pixiv.net/search.php?s_mode=s_tag&order=popular'+sex+'_d'+r18+'&word='+keyword+'&p='+page
        return [url,item]
    except: 
        return [0,0]    
def itemsellectid(url,item):
    try: 
        r = s.get(url)
        link_list = re.findall('stId&quot;:&quot;(.*?)&quot', r.text)
        
        if item!=[]:
            return link_list[int(item)-1]
        else:
            return random.choice(link_list)
    except:
        return '0'

def resulturl(itemsellect):
    try:
        resulturl=[]
        url2='https://www.pixiv.net/member_illust.php?mode=medium&illust_id='+itemsellect
        r2 = s.get(url2)
        manypage=re.findall('一次性投稿多張作品 (.*?)P', r2.text)
        if manypage==[]:
            resulturl+=['https://pixiv.cat/'+itemsellect+'.jpg']
        if manypage!=[]:
            if int(manypage[0])<3:
                resulturl+=['https://pixiv.cat/'+itemsellect+'-1.jpg','https://pixiv.cat/'+itemsellect+'-2.jpg']
            if int(manypage[0])>=3:
                for i in range(0,3):
                    resulturl+=['https://pixiv.cat/'+itemsellect+'-'+str(i+1)+'.jpg']
        return resulturl
    except:
        return '0'
    
def imageid(string):
    try:
        string=string.lower()
        number=0
        for v in string:
            if v=='-':
                number+=1
        if number==0:
            itemsellect=string
            resulturl=[]
            url2='https://www.pixiv.net/member_illust.php?mode=medium&illust_id='+itemsellect
            r2 = s.get(url2)
            manypage=re.findall('一次性投稿多張作品 (.*?)P', r2.text)
            if manypage==[]:
                resulturl=['https://pixiv.cat/'+itemsellect+'.jpg']
            if manypage!=[]:
                if int(manypage[0])<=4:
                    for i in range(0,int(manypage[0])):
                        resulturl+=['https://pixiv.cat/'+itemsellect+'-'+str(i+1)+'.jpg']
                if int(manypage[0])>4:
                    for i in range(0,4):
                        resulturl+=['https://pixiv.cat/'+itemsellect+'-'+str(i+1)+'.jpg']
            return resulturl
        if number==1:
            return ['https://pixiv.cat/'+string+'.jpg']
    except:
        return '0'

def monthsearch(string4):
    try:
        string4=(string4+'-').lower()
        url='https://www.pixiv.net/ranking.php?mode=monthly&content=illust'
        r = s.get(url)
        link_list = re.findall('"illust"data-click-label="(.*?)"data-type', r.text)
        rank = re.findall('-n(.*?)-', string4)
        if rank!=[]:
            return link_list[int(rank[0])-1]
        if rank==[]:
            return random.choice(link_list)
    except:
        return 0
    
def weelsearch(string):
    try:
        string=(string+'-').lower()
        item=re.findall('-n(.*?)-', string)
        if item!=[]:
            item=item[0] 
        if '-r18g' in string:
            url='https://www.pixiv.net/ranking.php?mode=r18g'
            r = s.get(url)
            link_list = re.findall('"illust"data-click-label="(.*?)"data-type', r.text)
            if item!=[]:
                return link_list[int(item)-1]
            if item==[]:
                return random.choice(link_list)
        r18 = re.findall('-r(.*?)-', string)
        url='https://www.pixiv.net/ranking.php?mode=weekly'
        if r18!=[]:
            if r18[0]=='18':
                r18='_r18'
                url=url+r18 
        r = s.get(url)
        link_list = re.findall('"illust"data-click-label="(.*?)"data-type', r.text)
        if item!=[]:
            return link_list[int(item)-1]
        if item==[]:
            return random.choice(link_list)
    except:
        return 0
    
def todaysearch(string):
    try:
        string=string+'-'
        string=string.lower()
        item=re.findall('-n(.*?)-', string)
        if item!=[]:
            item=item[0]
        r18 = re.findall('-r(.*?)-', string)
        url='https://www.pixiv.net/ranking.php?mode=daily'
        if r18!=[]:
            if r18[0]=='18':
                r18='_r18'
                url=url+r18            
        r = s.get(url)
        link_list = re.findall('"illust"data-click-label="(.*?)"data-type', r.text)
        if item!=[]:
            return link_list[int(item)-1]
        if item==[]:
            return random.choice(link_list)
    except:
        return 0
    
def boysearch(string):
    try:
        string=string+'-'
        string=string.lower()
        item=re.findall('-n(.*?)-', string)
        if item!=[]:
            item=item[0]
        r18 = re.findall('-r(.*?)-', string)
        url='https://www.pixiv.net/ranking.php?mode=male'
        if r18!=[]:
            if r18[0]=='18':
                r18='_r18'
                url=url+r18
        r = s.get(url)
        link_list = re.findall('"illust"data-click-label="(.*?)"data-type', r.text)
        if item!=[]:
            return link_list[int(item)-1]
        if item==[]:
            return random.choice(link_list)
    except:
        return 0
    
def girlsearch(string):
    try:
        string=string+'-'
        string=string.lower()
        item=re.findall('-n(.*?)-', string)
        if item!=[]:
            item=item[0]
        r18 = re.findall('-r(.*?)-', string)
        url='https://www.pixiv.net/ranking.php?mode=female'
        if r18!=[]:
            if r18[0]=='18':
                r18='_r18'
                url=url+r18
        r = s.get(url)
        link_list = re.findall('"illust"data-click-label="(.*?)"data-type', r.text)
        if item!=[]:
            return link_list[int(item)-1]
        if item==[]:
            return random.choice(link_list)
    except:
        return 0
    
def intersearch(string):
    try:
        string=string+'-'
        string=string.lower()
        item=re.findall('-n(.*?)-', string)
        if item!=[]:
            item=item[0]
        url='https://www.pixiv.net/ranking_area.php?type=detail&no=6'
        
        r = s.get(url)
        link_list = re.findall('"illust"data-click-label="(.*?)"data-type', r.text)
        if item!=[]:
            return link_list[int(item)-1]
        if item==[]:
            return random.choice(link_list)
    except:
        return 0
##############################################################
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

line_bot_api = LineBotApi('5FQaDuHO+i1ANMpw6/t4UQDWFsodgnqdkgjNU+yMchj8PL+3nrUy8pb16CiuqOJSBf9Sm1Pz2636PLB4OuxFqxyTmiusaAiG2A1DtEkQMBjm7K6d9zcU4HQFeADuo9sX+0BJ71cDdzqXy2FMuQggaAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('c0b3764f2ced579df9c339f3dc07c4e1')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


def googles(query):
    query2=urllib.parse.quote_plus(query)
    tStart = time.time()
    url = "https://www.google.com.tw/search?hl=zh-TW&q="+query2+"&meta=&aq=f&oq=%22"
    #url = "https://www.google.com/search?q=%E4%BA%9E%E8%8E%89%E4%BA%9E&source=lnms&tbm=isch"
    log_file = 'download.log'
    logging.basicConfig(level=logging.DEBUG, filename=log_file, filemode="a+", format="%(asctime)-15s %(levelname)-8s  %(message)s")


    headers = {}
    headers['User-Agent'] = generate_user_agent()
    headers['Referer'] = 'https://www.google.com'
    req = urllib.request.Request(url, headers = headers)
    resp = urllib.request.urlopen(req)
       
    page_content = str(resp.read())

    L = ['', '', '', '', '', '']
    L2 = ['', '', '', '', '', '']
    L3 = ''
    #a1 = '\xe7\xb7\x8b\xe5\xbd\x88\xe7\x9a\x84\xe4\xba\x9e\xe8\x8e\x89\xe4\xba\x9e- \xe7\xbb\xb4\xe5\x9f\xba\xe7\x99\xbe\xe7\xa7\x91\xef\xbc\x8c\xe8\x87\xaa\xe7\x94\xb1\xe7\x9a\x84\xe7\x99\xbe\xe7\xa7\x91\xe5\x85\xa8\xe4\xb9\xa6'
    s5=0;s3=0;s4=0;
    i = 0
    while i < 5:
        s3 = page_content.index('<h3 class="r"><a href="',0+s5,len(page_content))
        s4 = page_content.index('"', s3+24,len(page_content))
        L2[i]=page_content[s3+23:s4]
    
        s3=page_content.index('</a></h3>', s4,len(page_content))
        s4=page_content.rindex('event)">',s4 ,s3)

        L[i]=page_content[s4+8:s3]
        c = bytearray()
        c.extend(map(ord, L[i]))
        c4=c.decode('unicode_escape')

        b5 = bytearray()
        b5.extend(map(ord, c4))
        L[i]=b5.decode('utf-8')
        
        s5=s4
        i+=1 
    L3=(L[0]+'\n'+L2[0]+'\n'+'\n'+L[1]+'\n'+L2[1]+'\n'+'\n'+L[2]+'\n'+L2[2]+'\n'+'\n'+L[3]+'\n'+L2[3]+'\n'+'\n'+L[4]+'\n'+L2[4])    
    return (L3)

#url = "https://www.google.com.tw/search?hl=zh-TW&q=%E4%BA%9E%E8%8E%89%E4%BA%9E&meta=&aq=f&oq=%22"
def googlei(query,n):

    query2=urllib.parse.quote_plus(query)
    if n==1: 
        url = "https://www.google.com/search?q="+query2+"&source=lnms&tbm=isch"
    if n==2:
        #大於800*600像素
        url = "https://www.google.com/search?q="+query2+"&tbs=isz:lt,islt:svga&tbm=isch&source=lnt"
    if n==3:
        #大於1024*768像素
        url = "https://www.google.com/search?q="+query2+"&tbs=isz:lt,islt:xga&tbm=isch&source=lnt"
    if n==4:
        #大於1600*1200像素
        url = "https://www.google.com/search?q="+query2+"&tbs=isz:lt,islt:2mp&tbm=isch&source=lnt"
    log_file = 'download.log'
    logging.basicConfig(level=logging.DEBUG, filename=log_file, filemode="a+", format="%(asctime)-15s %(levelname)-8s  %(message)s")
    

    headers = {}
    headers['User-Agent'] = generate_user_agent()
    headers['Referer'] = 'https://www.google.com'
    req = urllib.request.Request(url, headers = headers)
    resp = urllib.request.urlopen(req)
       
    page_content = str(resp.read())

    if page_content:
        link_list = re.findall('"ou":"(.*?)"', page_content)
        if len(link_list) == 0:
            print('get 0 links from page {0}'.format(url))
            logging.info('get 0 links from page {0}'.format(url))
            
        else:
             set(link_list)
    else:
          set()

    link_list3= [None] * 100
    link_list4= [None] * 100
    i = 0
    for var in link_list:
        if var.endswith(".jpg",0,len(var)) or var.endswith(".png",0,len(var)) :
            link_list3[i]=var
            i+=1
    link_list3=list(filter(None, link_list3))  
    i = 0
    for var in link_list3:
        if var.startswith("https",0,len(var)):
            link_list4[i]=var
            i+=1

    x=list(filter(None, link_list4))    
    random.shuffle(x)    
    return x


    


def get_sourceid(event):
    if event.source.type == 'user':
        return event.source.user_id
    elif event.source.type == 'group':
        return event.source.group_id
    elif event.source.type == 'room':
        return event.source.room_id
    else:
        raise Exception('event.source.type:%s' % event.source.type)
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    event.source.user_id=get_sourceid(event)
    if event.message.text=='吃屎':  
        sss=['https://pixiv.cat/45068168.jpg','https://pixiv.cat/45068168.jpg']
        image1=[0]*2
        image2=[TextSendMessage(text='吃屎')]
        for i in range(0,len(image1)):
            image1[i]=ImageSendMessage(sss[i],sss[i])
              
        image2+=image1
        line_bot_api.reply_message(event.reply_token,image2)
        
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text='吃屎'))
        
        return 0
    
######################################################################
    if event.message.text.lower().startswith('p-s')==True:
        [url,item]=pixivsearch(event.message.text)  
        itemid=itemsellectid(url,item)
        result=resulturl(itemid)
        if result=='0' or result==0:
            return 0
        image1=[0]*len(result)
        for i in range(0,len(result)):
            image1[i]=ImageSendMessage(result[i],result[i])
             
        if '-sid' in event.message.text:
            image2=[TextSendMessage(text=itemid)]
            image2+=image1
            #line_bot_api.push_message(event.source.user_id,)
            line_bot_api.reply_message(event.reply_token,image2)
            return 0
        line_bot_api.reply_message(event.reply_token,image1)    
        return 0
    
    if event.message.text.lower().startswith('p-id')==True:
        x=imageid(event.message.text.lower()[4:])
        image1=[0]*len(x)
        for i in range(0,len(x)):
            image1[i]=ImageSendMessage(x[i],x[i])
        line_bot_api.reply_message(event.reply_token,image1)    
        return 0    
    
    if event.message.text.lower().startswith('p-mon')==True:
        monthsearchid=monthsearch(event.message.text.lower())
        if monthsearchid==0 or monthsearchid=='0':
            return 0    
        monthresult=imageid(monthsearchid)  
        image1=[0]*len(monthresult)
        for i in range(0,len(monthresult)):
            image1[i]=ImageSendMessage(monthresult[i],monthresult[i])

        if '-sid' in event.message.text.lower():
            image2=[TextSendMessage(text=monthsearchid)]
            image2+=image1
            line_bot_api.reply_message(event.reply_token,image2)
            return 0
        line_bot_api.reply_message(event.reply_token,image1)
        return 0
    
    if event.message.text.lower().startswith('p-wk')==True:
        #number數只有到50個
        weeksearchid=weelsearch(event.message.text.lower()[4:])
        if weeksearchid==0 or weeksearchid=='0':
            return 0
        weekresult=imageid(weeksearchid)
        image1=[0]*len(weekresult)
        for i in range(0,len(weekresult)):
            image1[i]=ImageSendMessage(weekresult[i],weekresult[i])
        if '-sid' in event.message.text.lower():
            image2=[TextSendMessage(text=weeksearchid)]
            image2+=image1
            line_bot_api.reply_message(event.reply_token,image2)
            return 0
        line_bot_api.reply_message(event.reply_token,image1)    
        return 0
   
    if event.message.text.lower().startswith('p-to')==True:
        todaysearchid=todaysearch(event.message.text.lower()[4:])    
        if todaysearchid==0 or todaysearchid=='0':
            return 0
        todayresult=imageid(todaysearchid)
        image1=[0]*len(todayresult)
        for i in range(0,len(todayresult)):
            image1[i]=ImageSendMessage(todayresult[i],todayresult[i])
        if '-sid' in event.message.text.lower():
            image2=[TextSendMessage(text=todaysearchid)]
            image2+=image1
            line_bot_api.reply_message(event.reply_token,image2)
            return 0
        line_bot_api.reply_message(event.reply_token,image1)        
        return 0
    
    if event.message.text.lower().startswith('p-boy')==True:
        boysearchid=boysearch(event.message.text.lower()[5:])    
        if boysearchid==0 or boysearchid=='0':
            return 0
        
        boyresult=imageid(boysearchid)
        image1=[0]*len(boyresult)
        for i in range(0,len(boyresult)):
            image1[i]=ImageSendMessage(boyresult[i],boyresult[i])
        if '-sid' in event.message.text.lower():
            image2=[TextSendMessage(text=boysearchid)]
            image2+=image1
            line_bot_api.reply_message(event.reply_token,image2)
            return 0
        line_bot_api.reply_message(event.reply_token,image1)           
        return 0
    
    if event.message.text.lower().startswith('p-girl')==True:
        girlsearchid=girlsearch(event.message.text.lower()[6:])
        if girlsearchid==0 or girlsearchid=='0':
            return 0
        girlresult=imageid(girlsearchid)
        image1=[0]*len(girlresult)
        for i in range(0,len(girlresult)):
            image1[i]=ImageSendMessage(girlresult[i],girlresult[i])
        if '-sid' in event.message.text.lower():
            image2=[TextSendMessage(text=girlsearchid)]
            image2+=image1
            line_bot_api.reply_message(event.reply_token,image2)
            return 0
        line_bot_api.reply_message(event.reply_token,image1)  
        return 0
    
    if event.message.text.lower().startswith('p-int')==True:
        intersearchid=intersearch(event.message.text.lower()[5:])
        if intersearchid==0 or intersearchid=='0':
            return 0
        interresult=imageid(intersearchid)
        image1=[0]*len(interresult)
        for i in range(0,len(interresult)):
            image1[i]=ImageSendMessage(interresult[i],interresult[i])
        if '-sid' in event.message.text.lower():
            image2=[TextSendMessage(text=intersearchid)]
            image2+=image1
            line_bot_api.reply_message(event.reply_token,image2)
            return 0
        line_bot_api.reply_message(event.reply_token,image1)
        return 0
    
######################################################################
    if event.message.text.lower().startswith('gi-')==True: 
        ss=googlei(event.message.text[3:],1)
        image1=[0]*3
        for i in range(0,3):
            image1[i]=ImageSendMessage(ss[i],ss[i])
        line_bot_api.reply_message(event.reply_token,image1) 
        return 0
    
    if event.message.text.lower().startswith('gil-')==True: 
        ss=googlei(event.message.text[4:],2)
        image1=[0]*3
        for i in range(0,3):
             image1[i]=ImageSendMessage(ss[i],ss[i])
        line_bot_api.reply_message(event.reply_token,image1)         
        return 0
    
    if event.message.text.lower().startswith('gim-')==True: 
        ss=googlei(event.message.text[4:],3)
        #image_message = ImageSendMessage(original_content_url=ss[0],preview_image_url=ss[0])
        image1=[0]*3
        for i in range(0,3):           
            image1[i]=ImageSendMessage(ss[i],ss[i])
        line_bot_api.reply_message(event.reply_token,image1)     
        return 0
    
    if event.message.text.lower().startswith('gih-')==True: 
        ss=googlei(event.message.text[4:],4)
        image1=[0]*3
        for i in range(0,3):           
            image1[i]=ImageSendMessage(ss[i],ss[i])
        line_bot_api.reply_message(event.reply_token,image1)       
        return 0
    
    if event.message.text.lower().startswith('gs-')==True:    
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=googles(event.message.text[4:])))
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=googles(event.message.text[3:])))
        #line_bot_api.push_message(event.source.user_id,TextSendMessage(text=googles(event.message.text[3:])))
        return 0
  

import os
if __name__ == "__main__":
    
    app.run(host='0.0.0.0',port=os.environ['PORT'])
