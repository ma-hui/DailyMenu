# -*- coding:utf-8 -*-
import urllib2
import re
import time
from bs4 import  BeautifulSoup
import requests


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
#
def get_menu_info(text):
    soup = BeautifulSoup(text)
    soup.prettify()
    str = ''
    for span in soup.find_all('span'):
       str += span.string
    return str

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

def delelte_space(str):
    '''
    u'去除所有的空格，
    '''
    pattern = re.compile('\s+')
    ret = pattern.sub('', str)
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
        smenu = replc_mulines(ss)
        # print smenu
        ret[TIMES[i]] = smenu
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
    ti = daily_check_time()
    if  ti:
        url = get_menu_url()
        tex = get_url_text(url)
        allmenu = get_all_meuntex(tex)
        netmenu = get_netease_menu(allmenu)
        cmenu = netmenu[ti]
        return cmenu
    else:
        print("not the time to eat")

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

if __name__ == '__main__':
   menu = daily_menu()
   users = get_config_value('Names','usrs')
   send_message(users,menu)

