# -*- coding: utf-8 -*-
# !/usr/bin/python3

import os
from pyquery import PyQuery as pq
import requests
import urllib
import re
import json

class Song:

    cid = '205361747'
    guid= '4913747390'
    prefix = 'C400'

    mid = ''
    vkey = ''
    url = ''


    name = ''
    albumName = ''
    albumImage = ''
    lyrics = ''

class Parser:
    def searchParser(self, keyword):

        keyword = urllib.parse.quote(keyword)
        url = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.song&searchid=71278113371358828&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=20&g_tk=5381&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&w=" + keyword
        print ("搜索URL\n" + url)

        responseText = requests.get(url).text
        jsonStr = re.match('callback\((.*)\)', responseText).group(1)
        result = json.loads(jsonStr)
        obj = result['data']['song']['list'][0]
        song = Song()
        song.mid = obj['mid']
        song.name = obj['name']
        song.albumName = obj['album']['name']
        print ('\nid\n' + song.mid + '\n歌名\n' + song.name + '\n专辑\n' + song.albumName)

        return song

    def vkeyParser(self, song):
        url = 'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?cid=' + song.cid + '&format=json&uin=0&guid=' + song.guid + '&songmid=' + song.mid + '&filename=' + song.prefix + song.mid + '.m4a'
        # print ('\nvkey url\n' + url)

        result = json.loads(requests.get(url).text)
        vkey = result['data']['items'][0]['vkey']
        return vkey

    def songURL(self, song):
        url = 'http://dl.stream.qqmusic.qq.com/' + song.prefix + song.mid + '.m4a?vkey=' + song.vkey + '&guid=' + song.guid
        print ('\n下载地址\n' + url)
        return url

    def download(self, song):
        result = requests.request('get', song.url, cookies={'qqmusic_fromtag':'66'}).content
        path = 'music/' + song.name + '.mp4'
        dir = os.path.dirname(path)
        if result:
            if not os.path.exists(dir):
                 os.makedirs(dir)
            with open(path, 'wb') as f:
                f.write(result)
            f.close()


    def start(self, name):

        song = self.searchParser(name)
        vkey = self.vkeyParser(song)
        song.vkey = vkey
        url = self.songURL(song)
        song.url = url
        self.download(song)
