import urllib
import urlparse
import xbmcgui
import sys
import os
import xbmc
import xbmcplugin
import xbmcaddon
import YDStreamUtils
import YDStreamExtractor
YDStreamExtractor.disableDASHVideo(True)

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

addon = xbmcaddon.Addon()

addonname = addon.getAddonInfo('name')
icon = addon.getAddonInfo('icon')
infoicon = 'special://home/addons/plugin.youtube.dl.starter/info.png'

folder = xbmcaddon.Addon(id='script.module.youtube.dl')

savepath = folder.getSetting('last_download_path')

menu0 = addon.getLocalizedString(30001)
menu1 = addon.getLocalizedString(30002)
menu2 = addon.getLocalizedString(30003)
menu3 = addon.getLocalizedString(30004)

enter0 = addon.getLocalizedString(30010)

errorline1 = addon.getLocalizedString(30101)
errorline2 = addon.getLocalizedString(30102)

time = 5000

def start_addon():
    xbmc.executebuiltin('RunAddon("script.module.youtube.dl")')

def start_download():
    kb = xbmc.Keyboard ('default', 'heading', False)
    kb.setDefault('')
    kb.setHeading(enter0)
    kb.setHiddenInput(False)
    kb.doModal()
    if (kb.isConfirmed()):
        try:
            url = kb.getText(kb)
            info = YDStreamExtractor.getVideoInfo(url)
            YDStreamExtractor.handleDownload(info, bg=True)
        except:
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, errorline2, time, infoicon))
            start_menu()
    else:
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, errorline1, time, infoicon))
        start_menu()
    xbmc.executebuiltin('xbmc.activatewindow(home)')
    sys.exit(0)

def start_play():
    kb = xbmc.Keyboard ('default', 'heading', False)
    kb.setDefault('')
    kb.setHeading(enter0)
    kb.setHiddenInput(False)
    kb.doModal()
    if (kb.isConfirmed()):
        try:
            url = kb.getText(kb)
            vid = YDStreamExtractor.getVideoInfo(url,quality=1)
            stream_url = vid.streamURL()
            title = vid.selectedStream()['title']
            thumbnail = vid.selectedStream()['thumbnail']
            listitem = xbmcgui.ListItem (title)
            listitem.setInfo('video', {'Title': title})
            listitem.setArt({'thumb': thumbnail, 'icon': thumbnail})
            xbmc.Player().play(stream_url, listitem)
        except:
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, errorline2, time, infoicon))
            start_menu()
    else:
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, errorline1, time, infoicon))
        start_menu()

def play_video(path):
    url = final_link
    vid = YDStreamExtractor.getVideoInfo(url,quality=1)
    play_item = xbmcgui.ListItem(path=path)
    stream_url = vid.streamURL()
    if stream_url:
        play_item.setPath(stream_url)
        xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)

def start_menu():
    dialog = xbmcgui.Dialog()
    entries = [menu0, menu1, menu2, menu3]
    nr = dialog.select('YouTube-DL Starter', entries)
    if nr==0:
        start_addon()
        xbmc.executebuiltin('xbmc.activatewindow(home)')
        sys.exit(0)
    if nr==1:
        start_download()
    if nr==2:
        start_play()
        xbmc.executebuiltin('xbmc.activatewindow(home)')
        sys.exit(0)
    if nr==3:
        xbmc.executebuiltin('xbmc.activatewindow(home)')
        sys.exit(0)
    else:
        xbmc.executebuiltin('xbmc.activatewindow(home)')
        sys.exit(0)

mode = args.get('mode', None)

if mode is None:        
    start_menu()
    xbmc.executebuiltin('xbmc.activatewindow(home)')
    sys.exit(0)

elif mode[0] == 'play':
   final_link = args['url'][0]
   play_video(final_link)