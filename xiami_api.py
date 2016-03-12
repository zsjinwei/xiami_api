#-*- coding: UTF-8 -*-
from __future__ import print_function
import sys, json
import urllib2
import re
from urllib import urlencode
reload(sys)
sys.setdefaultencoding('utf8')

class xiami_api: 
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'    
    headers = { 'User-Agent' : user_agent }
    def __init__(self):
    	return
    # 查找制定的专辑是否存在音乐库里
    # 参数:
    #     artist - 歌手名
    #     album - 专辑名
    # 返回:
    # dict对象:
    #     is_exist - 1 or 0 专辑是否存在
    #     artist_name - 歌手名
    #     album_name - 专辑名
    #     album_url - 专辑页面URL
    def find_album(self, artist, album):
        query =  {'key': artist+'+'+album,'pos': '1'}
        url = 'http://www.xiami.com/search' 
        req = urllib2.Request(url, urlencode(query), self.headers)    
        response = urllib2.urlopen(req)  
        html = response.read()  
        #print(html)
        is_exist = '0'
        #<a class="song" href="http://www.xiami.com/album/24075643" title="新的心跳">
        #<a class="singer" href="http://www.xiami.com/artist/55712" title="邓紫棋">
        album_url = ''
        album_name = ''
        artist_name = ''
        if html != '':
            album_match = re.findall(r'<a\s+class="song"\s+href="(.+?)"\s+title="(.+?)"\s*>', html)
            #print(album_match)
            r = re.compile(r'<a\s+class="singer"\s+href=".+?"\s+title=".+?"\s*><b.*?>(.+?)</b>\s*</a>', re.S)
            artist_match = r.findall(html)
            #print(artist_match)

            if len(artist_match)>0:
                artist_name = artist_match[0]
            #print(artist_name)

            if len(album_match)>0:
                for i in range(0,len(album_match)):
                    if True or (album_match[i][1] == album and artist_name == artist):
            	        album_url = album_match[i][0]
                        album_name= album_match[i][1]
                        is_exist = '1'
                        break
            #print(album_url)
            #print(album_name)
        result = {'is_exist':is_exist, 'artist_name':artist_name, 'album_name':album_name, 'album_url':album_url};
        return result

    # 获取专辑细节
    #     artist - 歌手名
    #     album - 专辑名
    # 返回:
    #     'ret' - '1' or '0' 结果
    #     'album_name' = '专辑名'
    #     'album_cover_url' = '专辑封面URL'
    #     'album_detail' = //专辑细节描述(张学友 - <醒着做梦>为例)
    #         '艺人' = '张学友'
    #         '语种' = '国语'
    #         '唱片公司' = '环球唱片'
    #         '发行时间' = '2014年12月23日'
    #         '专辑类别' = '录音室专辑'
    #         '专辑风格' = '国语流行 Mandarin Pop'
    #     'album_tracks' = //专辑曲目
    #         'disc1' = 
    #             '01' = - 歌曲编号
    #                 'track_name' = '曲名'
    #                 'track_artist' = '歌手名'
    #         
    def get_album_detail(self, artist, album):
        ret_album = {}
        ret_album_detail = {}
        ret_album_tracks = {}
        ret_album_disc = {}
        ret_album_single_track = {}
        find_album_ret = self.find_album(artist, album)
        if find_album_ret['is_exist']=='0':
              ret_album['ret'] = '0'
              return ret_album
        ## 找到专辑后获取专辑细节 ##
        album_url = find_album_ret['album_url']
        album_name = find_album_ret['album_name']
        artist_name = find_album_ret['artist_name']
        ret_album['ret'] = '1'
        ret_album['album_name'] = album_name
        if album_url != '':
            #获取专辑细节html
            abd_req = urllib2.Request(album_url, '', self.headers)
            abd_resp = urllib2.urlopen(abd_req)  
            abd_html = abd_resp.read()
            #print(abd_html)
            #匹配专辑封面url
            abd_cover_url_match = re.findall(r'<a.*?id="cover_lightbox".+?href="(.+?)".*?>.*</a>', abd_html)
            if len(abd_cover_url_match) > 0:
                abd_cover_url = abd_cover_url_match[0]
            else:
                abd_cover_url = ''
            #print(abd_cover_url)
            ret_album['album_cover_url'] = abd_cover_url
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
                #print(abd_name+' = '+abd_val)
                ret_album_detail[abd_name] = abd_val
                ret_album['album_detail'] = ret_album_detail
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
                    #print(disc_name)
	            #print(tracks_str)
                    r = re.compile(r'<td.*?class="trackid".*?>(.*?)</td>.*?<td.*?class="song_name".*?>.*?<a.*?href="/song/.+?".*?>(.*?)</a>(.*?)</td>', re.S)
                    single_track_match = r.findall(tracks_str)
                    #print(single_track_match)
                    for single_track_item in single_track_match:
                        track_id = single_track_item[0].rstrip()
                        track_name = single_track_item[1].rstrip()
                        print(track_name)
                        if single_track_item[2] == '':
                            track_singer = artist_name
                        else:
                            r = re.compile(r'<a.*?>(.*?)</a>', re.S)
                            single_track_mv_match = r.findall(single_track_item[2])
                            if len(single_track_mv_match)>0: #这里有问题，有ＭＶ的时候不能取得歌手名
                                track_singer = artist_name
                            else:
                                track_singer = single_track_item[2].rstrip()
                        ret_album_single_track['track_name'] = track_name
                        ret_album_single_track['track_singer'] = track_singer
                        ret_album_disc[track_id] = ret_album_single_track
                        ret_album_single_track = {}
                    ret_album_tracks[disc_name] = ret_album_disc
                    ret_album_disc = {}
            ret_album['album_tracks'] = ret_album_tracks
        return ret_album
        
#track 名字可能的样式: 
#<td class="trackid">13</td><td class="song_name"><a href="/song/1770411972" title="">手心</a>胡琳;林一峰</td>
#<td class="trackid">02</td><td class="song_name"><a href="/song/1770411975" title="">The Shadow Of Your Smile</a></td>
#<td class="trackid">02</td><td class="song_name"><a href="/song/1775020424" title="">再见</a><a target="_blank" href="/mv/K6YYDH"><b class="icon mv">MV</b></a><a title="" href="/song/1775020424" class="show_zhcn">Goodbye</a></td>



