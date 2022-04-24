from base64 import encode
from tkinter import E
import urllib.request
import requests
import json
import re
import os
import pandas as pd
#定义要爬取的微博大V的微博ID
id = '3170665862'

#设置代理IP
proxy_addr="122.241.72.191:808"

#定义页面打开函数
def use_proxy(url,proxy_addr):
    req=urllib.request.Request(url)
    req.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0")
    proxy=urllib.request.ProxyHandler({'http':proxy_addr})
    opener=urllib.request.build_opener(proxy,urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    data=urllib.request.urlopen(req).read().decode('utf-8','ignore')
    return data

#获取微博主页的containerid，爬取微博内容时需要此id
def get_containerid(url):
    data=use_proxy(url,proxy_addr)
    content=json.loads(data).get('data')
    for data in content.get('tabsInfo').get('tabs'):
        if(data.get('tab_type')=='weibo'):
            containerid=data.get('containerid')
    return containerid

#获取微博大V账号的用户基本信息，如：微博昵称、微博地址、微博头像、关注人数、粉丝数、性别、等级等
def get_userInfo(id):
    url='https://m.weibo.cn/api/container/getIndex?type=uid&value='+id
    data=use_proxy(url,proxy_addr)
    content=json.loads(data).get('data')
    profile_image_url=content.get('userInfo').get('profile_image_url')
    description=content.get('userInfo').get('description')
    profile_url=content.get('userInfo').get('profile_url')
    verified=content.get('userInfo').get('verified')
    guanzhu=content.get('userInfo').get('follow_count')
    name=content.get('userInfo').get('screen_name')
    fensi=content.get('userInfo').get('followers_count')
    gender=content.get('userInfo').get('gender')
    urank=content.get('userInfo').get('urank')
    print("微博昵称："+name+"\n"+"微博主页地址："+profile_url+"\n"+"微博头像地址："+profile_image_url+"\n"+"是否认证："+str(verified)+"\n"+"微博说明："+description+"\n"+"关注人数："+str(guanzhu)+"\n"+"粉丝数："+str(fensi)+"\n"+"性别："+gender+"\n"+"微博等级："+str(urank)+"\n")


#获取微博内容信息,并保存到文本中，内容包括：每条微博的内容、微博详情页面地址、点赞数、评论数、转发数等
def get_weibo(id,file):
    i=1
    flow_data = []
    pic_url_list = []
    while True:
        if len(flow_data) == 60:
            break
        url='https://m.weibo.cn/api/container/getIndex?type=uid&value='+id
        weibo_url='https://m.weibo.cn/api/container/getIndex?type=uid&value='+id+'&containerid='+get_containerid(url)+'&page='+str(i)
        try:
            data=use_proxy(weibo_url,proxy_addr)
            content=json.loads(data).get('data')
            cards=content.get('cards')
            if(len(cards)>0):
                for j in range(len(cards)):
                    print("-----正在爬取第"+str(i)+"页，第"+str(j)+"条微博------")
                    card_type=cards[j].get('card_type')

                    if(card_type==9):
                        mblog = cards[j].get('mblog')
                        pic = mblog.get('pic_ids')
                        text = mblog.get('text')

                        date_re = re.findall('\d+月\d+日', str(text))
                        date = ''

                        if len(date_re) > 0:
                            date = date_re[0]

                        begin_index = str(text).find("客运量")
                        end_index = str(text).find('万乘次')
                        if begin_index > -1 and end_index > -1:
                            print(text[begin_index+3:end_index])
                            flow_data.append([date, text[begin_index+3:end_index]])

                            if len(pic) > 0:
                                pic_url = 'https://wx4.sinaimg.cn/mw2000/' + pic[0] + '.jpg'
                                response = requests.request('get', pic_url)
                                path = os.getcwd() + '\scripts\pic\\' + date + '.jpg'
                                print(response.status_code, pic_url)
                                if response.status_code != 200:
                                    pic_url_list.append([date, pic_url])
                                with open(path, 'wb') as f:
                                    f.write(response.content)
                i+=1
            else:
                break
        except Exception as e:
            print(e)
            pass
    
    flow_df = pd.DataFrame(flow_data, columns=['日期', '客流'])
    pic_df = pd.DataFrame(pic_url_list, columns=['日期', 'url'])
    flow_df.to_csv('./scripts/flow.csv', index=0)
    pic_df.to_csv('./scripts/failed_pic.csv', index=0)
    print(flow_df)

if __name__=="__main__":
    file=id+".txt"
    get_userInfo(id)
    get_weibo(id,file)
