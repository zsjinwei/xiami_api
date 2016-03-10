#-*- coding: UTF-8 -*-
from __future__ import print_function
import sys, json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import urllib2
import re
from urllib import urlencode

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'    
headers = { 'User-Agent' : user_agent }

## 查找歌手和专辑名 ##
artist = '张学友'
album = '醒着做梦'
query =  {
'key': artist+'+'+album,
'pos': '1'
}
url = 'http://www.xiami.com/search' 
req = urllib2.Request(url, urlencode(query), headers)    
response = urllib2.urlopen(req)  
html = response.read()  
#print(html)
flag = False
#<a class="song" href="http://www.xiami.com/album/24075643" title="新的心跳">
#<a class="singer" href="http://www.xiami.com/artist/55712" title="邓紫棋">
album_url = ''
album_name = ''
artist_name = ''
if html != '':
    album_match = re.findall(r'<a\s+class="song"\s+href="(.+?)"\s+title="(.+?)"\s*>', html)
    print(album_match)
    r = re.compile(r'<a\s+class="singer"\s+href=".+?"\s+title=".+?"\s*><b.*?>(.+?)</b>\s*</a>', re.S)
    artist_match = r.findall(html)
    print(artist_match)

    if len(artist_match)>0:
        artist_name = artist_match[0]
    print(artist_name)

    if len(album_match)>0:
        for i in range(0,len(album_match)):
            if album_match[i][1] == album and artist_name == artist:
    	        album_url = album_match[i][0]
                album_name= album_match[i][1]
                break

    print(album_url)
    print(album_name)
    

## 找到专辑后获取专辑细节 ##
if album_url != '':
    #获取专辑细节html
    abd_req = urllib2.Request(album_url, '', headers)
    abd_resp = urllib2.urlopen(abd_req)  
    abd_html = abd_resp.read()
    #print(abd_html)
    #匹配专辑封面url
    abd_cover_url_match = re.findall(r'<a.*?id="cover_lightbox".+?href="(.+?)".*?>.*</a>', abd_html)
    if len(abd_cover_url_match) > 0:
        abd_cover_url = abd_cover_url_match[0]
    else:
        abd_cover_url = ''
    print(abd_cover_url)
    #匹配专辑细节
    #<div id="album_info" rel="v:rating">
    r = re.compile(r'<div\s+id="album_info"[^>]+>(.*?)</table>', re.S)
    table_match = r.findall(abd_html)
    #print(table_match)
    if len(table_match) > 0:
        r = re.compile(r'<tr>(.*?)</tr>', re.S)
        abd_table_match = r.findall(table_match[0])
        #print(abd_table_match)
    for tr_inner_str in abd_table_match:
        tr_inner_str = tr_inner_str.replace('\r','')
        tr_inner_str = tr_inner_str.replace('\n','')
        tr_inner_str = tr_inner_str.replace('\t','')
	tr_inner_str = tr_inner_str.replace(':','')
        tr_inner_str = tr_inner_str.replace('：','')
        #print(tr_inner_str)
        abd_td_match = re.findall(r'<td[^>]*>(.+?)</td>.*?<td[^>]*>(.+?)</td>',tr_inner_str)
        #print(abd_td_match)
        abd_name = ''
        abd_val = ''
        if len(abd_td_match) > 0:
            abd_name = abd_td_match[0][0]
            abd_td_a_match = re.findall(r'<a.*?>(.+?)</a>',abd_td_match[0][1])
            #print(abd_td_a_match)
            if len(abd_td_a_match) > 0:
                abd_val = abd_td_a_match[0]
            else:
                abd_val = abd_td_match[0][1]
        print(abd_name+' = '+abd_val)
    #匹配专辑歌目
    r = re.compile(r'<strong.*?class="trackname".*?>(.*?)</strong>\s*<table.*?class="track_list".*?>(.*?)</table>', re.S)
    track_match = r.findall(abd_html)
    #print(track_match)
    track_match_str = ''
    if len(track_match)>0:
        for disc_item in track_match:
            disc_name = disc_item[0]
            tracks_str = disc_item[1]
            disc_name = disc_name.replace(' ','')
            tracks_str = tracks_str.replace('\r','')
            tracks_str = tracks_str.replace('\n','')
            tracks_str = tracks_str.replace('\t','')
            print(disc_name)
	    #print(tracks_str)

            r = re.compile(r'<td.*?class="trackid".*?>(.*?)</td>.*?<td.*?class="song_name".*?>.*?<a.*?href="/song/.+?".*?>(.*?)</a>(.*?)</td>', re.S)
            single_track_match = r.findall(tracks_str)
            #print(single_track_match)
            for single_track_item in single_track_match:
                track_id = single_track_item[0].rstrip()
                track_name = single_track_item[1].rstrip()
                if single_track_item[2] == '':
                    track_singer = artist_name
                else:
                    r = re.compile(r'<a.*?>(.*?)</a>', re.S)
                    single_track_mv_match = r.findall(single_track_item[2])
                    if len(single_track_mv_match)>0:
                        track_singer = artist_name
                    else:
                        track_singer = single_track_item[2].rstrip()
                print(track_id+'-'+track_name+'-'+track_singer)
#track 名字可能的样式: 
#<td class="trackid">13</td><td class="song_name"><a href="/song/1770411972" title="">手心</a>胡琳;林一峰</td>
#<td class="trackid">02</td><td class="song_name"><a href="/song/1770411975" title="">The Shadow Of Your Smile</a></td>
#<td class="trackid">02</td><td class="song_name"><a href="/song/1775020424" title="">再见</a><a target="_blank" href="/mv/K6YYDH"><b class="icon mv">MV</b></a><a title="" href="/song/1775020424" class="show_zhcn">Goodbye</a></td>



