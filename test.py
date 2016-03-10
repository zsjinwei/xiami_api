#-*- coding: UTF-8 -*-
from __future__ import print_function
import sys, json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import xiami_api

artist = '张学友'
album = '醒着做梦'
xiami = xiami_api.xiami_api()
ret = xiami.get_album_detail(artist, album)
print(ret)
