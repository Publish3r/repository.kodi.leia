#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import xbmc
import xbmcaddon
import xbmcgui,xbmcvfs
import time
import re
import YDStreamUtils
import YDStreamExtractor

addon = xbmcaddon.Addon()

addonname = addon.getAddonInfo('name')

folder = xbmcaddon.Addon(id='script.module.youtube.dl')

savepath = folder.getSetting('last_download_path').decode('utf-8')
 
path = xbmc.getInfoLabel('ListItem.FileNameAndPath')
title = xbmc.getInfoLabel('ListItem.Title')
listitem = xbmcgui.ListItem(path=path)
listitem.setInfo(type="Video", infoLabels={"Title": title})

kodi_player = xbmc.Player()
kodi_player.play(path,listitem)

time.sleep(10) 
videoda=0

while videoda==0 :
    try:
        file=kodi_player.getPlayingFile()
        if not file=="":
            videoda=1
    except:
        pass 
        
file=file.split("|")[0]

try:
    info = YDStreamExtractor.getVideoInfo(file)
    YDStreamExtractor.handleDownload(info, bg=True)
except:
    pass
