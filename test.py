#!/usr/bin/python
#-*- coding: UTF-8 -*-
from __future__ import print_function
import sys, json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import xiami_api
import os, fnmatch
import difflib
from collections import Counter

def get_tag_val(tag_name, file_path):
    command = 'metaflac --show-tag='+tag_name+' "'+ file_path +'"'
    r = os.popen(command) #执行该命令
    info = r.readlines()  #读取命令行的输出到一个list
    if len(info) > 0:
        flac_tag_val = info[0].split('=')[1].strip()
    else:
        flac_tag_val = ''
    return flac_tag_val

def set_tag_val(tag_name, tag_val, file_path):
    command = 'metaflac --remove-tag='+tag_name+' "'+ file_path +'"'
    r = os.popen(command) #执行该命令
    command = 'metaflac --set-tag="'+tag_name+'='+tag_val+'" "'+ file_path +'"'
    r = os.popen(command) #执行该命令

def all_files(root, patterns = '*', single_level = False, yield_folders=False):
    patterns = patterns.split(';')
    for path, subdirs, files in os.walk(root):
        if yield_folders:
            files.extend(subdirs)
        files.sort()
        for name in files:
            for pattern in patterns:
                if fnmatch.fnmatch(name, pattern):
                    yield os.path.join(path,name)
                    break
        if single_level:
            break
#DISCTOTAL=1
#DISCNUMBER=1
#DATE=2015-01-01T00:00:00Z
#GENRE=测试　Pop
#COMMENT=还是电话电视
#ALBUMARTIST=卓文萱
#ARTIST=卓文萱
#ALBUM=灼乐感
#TITLE=心爱的
#TRACKNUMBER=3
#TRACKTOTAL=10

#artist = '张学友'
#album = '醒着做梦'
xiami = xiami_api.xiami_api()
#ret = xiami.get_album_detail(artist, album)
#print(ret)

root_path = '/home/jayvee/zyg'
file_name = '卓文萱-心爱的.flac'

paths = all_files(root_path, '*.flac;*.FLAC', True)
flacFiles = list(paths)
paths_without_ext = []
abd_all = {}
abd_tracks = {}
abd_album_cover_url = ''
abd_album = ''
abd_artist = ''
abd_lang = ''
abd_dist = ''
abd_date = ''
abd_category = ''
abd_genre = ''

for path in flacFiles:
    file_path = path
    print('=== '+file_path+' ===')
    #获取歌名
    flac_title_name = get_tag_val('TITLE', file_path)
    #print(flac_title_name)
    #获取专辑名
    flac_album_name = get_tag_val('ALBUM', file_path)
    #print(flac_album_name)
    #获取歌手名
    flac_artist_name = get_tag_val('ARTIST', file_path)
    #print(flac_artist_name)
    #获取注释
    flac_comment = get_tag_val('COMMENT', file_path)

#查询专辑信息
#艺人 = 卓文萱
#语种 = 国语
#唱片公司 = 滚石唱片
#发行时间 = 2014年09月26日
#专辑类别 = 录音室专辑
#专辑风格 = 国语流行 Mandarin Pop

    if flac_artist_name!='' and flac_album_name!='' and not abd_all.has_key('ret'):
        abd_all = xiami.get_album_detail(flac_artist_name, flac_album_name)
        #print(abd_all)
        #break
        if abd_all['ret']=='1':
            abd_album_cover_url = abd_all['album_cover_url']
            print('abd_album_cover_url = '+ abd_album_cover_url)
            abd = abd_all['album_detail']
            abd_album = abd_all['album_name']
            abd_tracks = abd_all['album_tracks']
            print(abd_album)
            if abd.has_key('艺人'):
                abd_artist = abd['艺人']
            if abd.has_key('语种'):
                abd_lang = abd['语种']
            if abd.has_key('唱片公司'):
                abd_dist = abd['唱片公司']
            if abd.has_key('发行时间'):
                abd_date = abd['发行时间']
            if abd.has_key('专辑类别'):
                abd_category = abd['专辑类别']
            if abd.has_key('专辑风格'):
                abd_genre = abd['专辑风格']
        else:
            print('Artist or Album is not in Music Library!')
    abd_disctotal = str(len(abd_tracks))
    abd_comment = 'lang=' + abd_lang + ';category=' + abd_category + ';distribution=' + abd_dist
    #print(abd_tracks['disc1'])
    pair_tracknum = 0
    pair_singer = ''
    pair_disc = ''
    pair_title = ''
    for disc in abd_tracks.items():
        #print(len(disc[1]))    
        for track in disc[1].items():
            #print(track)
            if difflib.SequenceMatcher(None, flac_title_name, track[1]['track_name']).ratio() > 0.6:
                pair_title = track[1]['track_name']
                pair_disc = disc[0]
                if pair_disc == 'disc2':
                    pair_discnum = '2'
                else:
                    pair_discnum = '1'
                pair_singer = track[1]['track_singer']
                pair_tracknum = track[0]
                pair_tracktotal = str(len(disc[1]))
                #print(pair_title)
                break

    print('TITLE = ' + pair_title)
    print('ARTIST = ' + pair_singer)
    print('TRACKNUMBER = ' + pair_tracknum)
    print('TRACKTOTAL = ' + pair_tracktotal)
    print('TITLE = ' + pair_title)
    print('ALBUM = ' + abd_album)
    print('ALBUMARTIST = ' + abd_artist)
    print('DATE = ' + abd_date)
    print('GENRE = ' + abd_genre)
    print('DISCNUMBER = ' + pair_discnum)
    print('DISCTOTAL = ' + abd_disctotal)
    print('COMMENT = ' + abd_comment)


































