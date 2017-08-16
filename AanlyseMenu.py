# -*- coding:utf 8-*-
import urllib2
import re
from bs4 import  BeautifulSoup

from ConfigParser import  ConfigParser
CONFILE = 'config.txt'


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

def replace_file_str(rpstr):
    spstr = rpstr.decode('utf-8')
    # pattern = re.compile(u'[^\u4E00-\u9FA5]')
    pattern = re.compile('\<.*?\>')
    fitstring = pattern.sub(r'\n',spstr)
    ret = fitstring.replace('&nbsp;',' ')
    print ret



def test():
    url =  get_menu_url()
    tex = get_url_text(url)
    replace_file_str(tex)

if __name__ == '__main__':
    test()
