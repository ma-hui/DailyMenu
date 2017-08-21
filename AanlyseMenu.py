# -*- coding:utf-8 -*-
import urllib2
import re
import requests
import time
# from bs4 import  BeautifulSoup
from ConfigParser import  ConfigParser


CONFILE = 'config.txt'
TIMES= [u'中餐', u'晚餐', u'夜宵']


def get_config_value(case,name):
    '''
    get the config value
    '''
    config = ConfigParser()
    config.read(CONFILE)
    return config.get(case,name)

def get_menu_url():
    url = get_config_value('urls','menu')
    return url

def get_url_text(url):
    ret = False
    try:
        request = urllib2.Request(url)
        f = urllib2.urlopen(request)
    except urllib2.URLError, e:
        print e.message
    else:
        ret = f.read()
        f.close()
    finally:
        return ret

# def get_menu_info(text):
#     soup = BeautifulSoup(text)
#     soup.prettify()
#     str = ''
#     for span in soup.find_all('span'):
#        str += span.string
#     return str

def get_all_meuntex(rpstr):
    spstr = rpstr.decode('utf-8')

    # 网页内容很简单，因此直接去除所有标签获得剩余文字
    pattern = re.compile('\<.*?\>')
    fitstring = pattern.sub(r'\n',spstr)

    # 菜单不统一部分特殊处理
    s = fitstring.replace('&nbsp;',' ')
    pos = s.find(u'阅读')
    ret = s[:pos]
    return ret



def replc_mulines(str):
    pattern = re.compile('\n+')
    ret = pattern.sub('\n', str)
    return ret

def get_netease_menu(tex):
    postart = tex.find(u'网易餐厅')
    posend = tex.find(u'西可餐厅')
    tt = tex[postart:posend]
    # print tt
    menu = get_single_menu(tt)
    # print menu
    return menu

# 西可需要特殊处理，暂时先不弄
def get_xike_menu(tex):
    postart = tex.find(u'西可餐厅')
    tt = tex[postart:]
    get_single_menu(tt)

def get_single_menu(tex):
    ret = {}
    i = 0
    for i in range(0, len(TIMES) -1):
        # print times[i]
        start = tex.find(TIMES[i])
        end = tex.find(TIMES[i+1])
        ss = tex[start:end]
        ss = replc_mulines(ss)
        smenu = trim_menu(ss)
        # print smenu
        ret[TIMES[i]] = smenu
    return ret

def  trim_menu(str):
    '''
    有1F ，2F的menu，将menu整理后返回，如果没有划分1F,2F，直接返回原menu
    '''
    # str = u'1F\n【本帮菜窗口】豉香龙利鱼、野米虾仁炒蛋、海蜇拌黄瓜。\n【家常菜窗口】\n清蒸腊鸡腿、青豆玉米炒虾仁、西芹牛肉\n2F\n【蔬菜】小青菜。'
    ret = []
    firstpos = str.find(u'1F')
    secondpos = str.find(u'2F')

    if firstpos != -1:    # has 1F's menu
        ret.insert(len(ret), str[:firstpos+2])
        if secondpos != -1:
            ret.extend(trim_dish(str[firstpos+2:secondpos]))
        else:
            ret.extend(trim_dish(str[firstpos + 2:]))

    if secondpos != -1:    # has 2F's menu
        ret.insert(len(ret), str[secondpos:secondpos+2])
        ret.extend(trim_dish(str[secondpos+2:]))

    if len(ret) == 0:
        return str
    else:
        return '\n'.join(ret)


def trim_dish(str):
    # str = u'【本帮菜窗口】豉香龙利鱼、野米虾仁炒蛋、海蜇拌黄瓜。\n  \n【jia窗口】\n豉香龙利鱼、\n野米虾仁炒蛋、海蜇拌黄瓜。'

    stpos = str.find(u'【')
    if stpos == -1 :
        ret = str
    else:
        ret = []

    while(stpos != -1):
        endpos = str.find(u'【',stpos+1)
        if endpos != -1:
            dish = delelte_space(str[stpos:endpos])
            ret.insert(len(ret), dish)

        else:
            dish = delelte_space(str[stpos:])
            ret.insert(len(ret), dish)

        stpos = endpos
    return ret

def delelte_space(str):
    '''
    去除所有的空格、换行
    '''
    pattern = re.compile('\s+')
    ret = pattern.sub('', str)
    return ret

def daily_check_time():
    # 1 lunch  2 dinner
    ltime = time.localtime(time.time())
    hrs = int(ltime.tm_hour)
    if   hrs < 12:
        return TIMES[0]
    elif hrs < 18:
        return TIMES[1]
    else:
        return False

def daily_menu():
    ti = daily_check_time()   # 检查是否为就餐时间，及具体的就餐时段
    if  ti:
        url = get_menu_url()
        tex = get_url_text(url)
        allmenu = get_all_meuntex(tex)
        netmenu = get_netease_menu(allmenu)
        cmenu = netmenu[ti]
        return cmenu
    else:
        return "not the meal time"

def send_message(usrs, message):
    pattern = re.compile(';')
    ret = re.split(pattern, usrs)
    popoapi = get_config_value('urls','popoapi')
    # print popoapi
    for usr in ret:
        data = {
            'to': usr,
            'body':message,
            'font_family':'微软雅黑'
        }
        requests.post(popoapi, data = data)

def daily_cron():
    users = get_config_value('Names', 'ne')
    menu = daily_menu()
    send_message(users, menu)

if __name__ == '__main__':
   daily_cron()
