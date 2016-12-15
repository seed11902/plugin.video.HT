# -*- coding: utf-8 -*- 
import urllib,urllib2,re,xbmcplugin,xbmcgui
from bs4 import BeautifulSoup
import urlparse
import requests
import base64
import json

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'movies')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36'}
def find(pattern, string):
        match = re.search(pattern,string)
        if match:
                ret =  match.group()
        else: 
                ret = "not find"
        return ret
def find2(pattern, string):
    match = re.findall(pattern,string)
    if match: 
        ret =  match
    else: 
        ret = "not find"
    return ret
def jsonXuite(mediumId,passwd):
    a = "http://vlog.xuite.net/_ajax/default/media/ajax?act=checkPasswd&mediumId=%s&passwd=%s"%(mediumId, passwd)
    return a
def subUrl(a):
    resSub = requests.get(a['href'], headers=headers)
    soupSub = BeautifulSoup(resSub.text, "html.parser")
    for hentry in soupSub.select('.hentry'):
        for index,iframe in enumerate(hentry.select('iframe')):
            findxuite = iframe['src'].find('http://vlog.xuite.net')
            if findxuite == -1:
                findxuite = iframe['src'].find('https://vlog.xuite.net');
            if findxuite == 0:
                for content in hentry.select('.entry-content'):
                    str1 = content.text.replace('\n','')
                    str1 = str1.replace(' ', '')
                    pwd = find2(u'密碼\W*：' + r'\d{4}',str1)
                url = urlparse.urlparse(iframe['src'])
                mediumId = base64.b64decode(url.path.split('/')[2]).split('-')[1].split('.')[0]
                for i, passwd in enumerate(pwd):
                    header = {"Referer":"http://vlog.xuite.net"}
                    payload =  {"act":"checkPasswd","mediumId":mediumId,"passwd":pwd[i][-4:]}
                    obj = requests.post('http://vlog.xuite.net/_ajax/default/media/ajax',headers=header,data=payload)
                    jd = json.loads(obj.text)
                    if jd["success"] == True:
                        if index == 0:
                            title = hentry.select('h3')[0].text.replace('\n', '')
                        else:
                            title = hentry.select('h3')[0].text.replace('\n', '') + "_" + str(index)
                        media = jd['media']["html5Url"]
                        image = 'http://vlog.xuite.net' + jd['media']["thumbnailUrl"]
                        addLink(title, media, image)
                        break
def hdx3(url):
        while url:
            res = requests.get(url, headers=headers)   
            soup = BeautifulSoup(res.text, "html.parser")
            for outer in soup.select('.post-outer'):
                for a in outer.find_all('a', href=True):
                    try:
                        subUrl(a)
                    except:
                        print("HTTV　except!!!")
            test = soup.find("a", {"id": "Blog1_blog-pager-older-link"})
            if test:
                url = test['href']
            else:
                break
def gsp(url):
        while url:
            res = requests.get(url, headers=headers)   
            soup = BeautifulSoup(res.text, "html.parser")
            for outer in soup.select('.entry-title'):
                for a in outer.find_all('a', href=True):
                    try:
                	subUrl(a)
                    except:
                        print("HTTV　except!!!")
            test = soup.find("a", {"id": "Blog1_blog-pager-older-link"})
            if test:
                url = test['href']
            else:
                break            
def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=addon_handle,url=url,listitem=liz)
        return ok
def adddir(name,Url,iconimage):
        ok=True
        url = build_url(Url)
        li = xbmcgui.ListItem(name, iconImage='DefaultFolder.png', thumbnailImage=iconimage)
        li.setInfo( type="Video", infoLabels={ "Title": name } )
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,listitem=li, isFolder=True)        
        return ok
def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

mode = args.get('mode', None)

if mode is None:
        adddir('hdx3',{'mode': 'hdx3', 'Url': ''},'http://4.bp.blogspot.com/-WMVj9xTGa8g/VTnWY9VlbWI/AAAAAAAAfkQ/CB80FL8Q2kc/s1600/HD.png')
        #
        adddir('hornydragon',{'mode': 'hornydragon', 'Url': ''},'')
        #
        adddir('45gsp',{'mode': '45gsp', 'Url': ''},'')
        xbmcplugin.addSortMethod(addon_handle, sortMethod=xbmcplugin.SORT_METHOD_TITLE)
        xbmcplugin.endOfDirectory(addon_handle)
elif mode[0] == 'hdx3':
        adddir('Regular Show',{'mode': 'folder','Type': 'hdx3', 'Url': 'http://hdx3.blogspot.com/search/label/Regular%20Show?max-results=200'},'')
        adddir('Adventure Time',{'mode': 'folder','Type': 'hdx3',  'Url': 'http://hdx3.blogspot.com/search/label/Adventure%20Time?max-results=200'},'')
        adddir('Superjail',{'mode': 'folder','Type': 'hdx3',  'Url': 'http://hdx3.blogspot.com/search/label/Superjail?max-results=200'},'')
        adddir('Ugly Americans',{'mode': 'folder','Type': 'hdx3',  'Url': 'http://hdx3.blogspot.com/search/label/Ugly%20Americans?max-results=200'},'')
        adddir('Mr. Pickles',{'mode': 'folder','Type': 'hdx3',  'Url': 'http://hdx3.blogspot.com/search/label/Mr.%20Pickles?max-results=200'},'')
        adddir('My Little Pony',{'mode': 'folder','Type': 'hdx3',  'Url': 'http://hdx3.blogspot.com/search/label/My%20Little%20Pony?max-results=200&m=0'},'')
        adddir('Sonic Boom',{'mode': 'folder','Type': 'hdx3',  'Url': 'http://hdx3.blogspot.com/search/label/Sonic%20Boom?max-results=200&m=0'},'')
        adddir('Bee and PuppyCat',{'mode': 'folder','Type': 'hdx3',  'Url': 'http://hdx3.blogspot.com/search/label/Bee%20and%20PuppyCat?max-results=200'},'')
        adddir('Metalocalypse',{'mode': 'folder','Type': 'hdx3',  'Url': 'http://hdx3.blogspot.com/search/label/Metalocalypse?max-results=200'},'')
        adddir('Rick and Morty',{'mode': 'folder','Type': 'hdx3',  'Url': 'http://hdx3.blogspot.com/search/label/Rick%20and%20Morty?max-results=200'},'')
        adddir('RWBY',{'mode': 'folder','Type': 'hdx3',  'Url': 'http://hdx3.blogspot.com/search/label/RWBY?max-results=200'},'')
        adddir('Dilbert',{'mode': 'folder','Type': 'hdx3',  'Url': 'http://hdx3.blogspot.com/search/label/Dilbert?max-results=200'},'')
        adddir('Dan Vs.',{'mode': 'folder','Type': 'hdx3',  'Url': 'http://hdx3.blogspot.com/search/label/Dan%20Vs.?max-results=200'},'')
        adddir('Bravest Warriors',{'mode': 'folder','Type': 'hdx3',  'Url': 'http://hdx3.blogspot.com/search/label/Bravest%20Warriors?max-results=200'},'')
        xbmcplugin.addSortMethod(addon_handle, sortMethod=xbmcplugin.SORT_METHOD_TITLE)
        xbmcplugin.endOfDirectory(addon_handle)
elif mode[0] == 'hornydragon':
        adddir('Bravest Warriors',{'mode': 'folder','Type': 'hornydragon',  'Url': 'http://hdx3.blogspot.com/search/label/Bravest%20Warriors?max-results=200'},'')
        adddir('Angry Video Game Nerd',{'mode': 'folder','Type': 'hornydragon', 'Url': 'http://hornydragon.blogspot.com/search/label/AVGN?max-results=200'},'')
        adddir('Board James',{'mode': 'folder','Type': 'hornydragon', 'Url': 'http://hornydragon.blogspot.com/search/label/Board%20James?max-results=200'},'')
        adddir('PewDiePie',{'mode': 'folder','Type': 'hornydragon', 'Url': 'http://hornydragon.blogspot.com/search/label/PewDiePie?max-results=200'},'')
        adddir('Henry\'s Kitchen',{'mode': 'folder','Type': 'hornydragon', 'Url': 'http://hornydragon.blogspot.com/search/label/%E5%8F%B2%E4%B8%8A%E6%9C%80%E6%82%B2%E5%93%80%E7%9A%84%E7%83%B9%E9%A3%AA%E6%95%99%E5%AD%B8?max-results=200'},'')
        adddir('Grade A Under A',{'mode': 'folder','Type': 'hornydragon', 'Url': 'http://hornydragon.blogspot.com/search/label/Grade%20A%20Under%20A?&max-results=200'},'')
        adddir(u'電玩驢子',{'mode': 'folder','Type': 'hornydragon', 'Url': 'http://hornydragon.blogspot.com/search/label/%E9%9B%BB%E7%8E%A9%E9%A9%A2%E5%AD%90?&max-results=200'},'')
        adddir('Casually Explained',{'mode': 'folder','Type': 'hornydragon', 'Url': 'http://hornydragon.blogspot.com/search/label/Casually%20Explained?max-results=200'},'')
        xbmcplugin.addSortMethod(addon_handle, sortMethod=xbmcplugin.SORT_METHOD_TITLE)
        xbmcplugin.endOfDirectory(addon_handle)
elif mode[0] == '45gsp':
        adddir('s14',{'mode': 'folder', 'Type': '45gsp', 'Url': 'http://45gsp.blogspot.tw/search/label/s14?max-results=200'},'')
        adddir('s15',{'mode': 'folder', 'Type': '45gsp', 'Url': 'http://45gsp.blogspot.tw/search/label/s15?max-results=200'},'')
        adddir('s16',{'mode': 'folder', 'Type': '45gsp', 'Url': 'http://45gsp.blogspot.tw/search/label/s16?max-results=200'},'')
        adddir('s17',{'mode': 'folder', 'Type': '45gsp', 'Url': 'http://45gsp.blogspot.tw/search/label/s17?max-results=200'},'')
        adddir('s18',{'mode': 'folder', 'Type': '45gsp', 'Url': 'http://45gsp.blogspot.tw/search/label/s18?max-results=200'},'')
        adddir('s19',{'mode': 'folder', 'Type': '45gsp', 'Url': 'http://45gsp.blogspot.tw/search/label/s19?max-results=200'},'')
        adddir('s20',{'mode': 'folder', 'Type': '45gsp', 'Url': 'http://45gsp.blogspot.tw/search/label/s20?max-results=200'},'')
        xbmcplugin.addSortMethod(addon_handle, sortMethod=xbmcplugin.SORT_METHOD_TITLE)
        xbmcplugin.endOfDirectory(addon_handle)        
elif mode[0] == 'folder':
        Url = args['Url'][0]
        Type = args['Type'][0]
        if Type == '45gsp':
        	gsp(Url)
        else:
        	hdx3(Url)
        xbmcplugin.addSortMethod(addon_handle, sortMethod=xbmcplugin.SORT_METHOD_TITLE)
        xbmcplugin.endOfDirectory(addon_handle)
