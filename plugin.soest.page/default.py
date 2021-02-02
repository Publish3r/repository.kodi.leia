#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys,xbmcaddon,os,requests,xbmc,xbmcgui,urllib,urllib2,re,xbmcplugin,time,datetime,random

from xml.dom import minidom
from dateutil import parser
from bs4 import BeautifulSoup
import json
import HTMLParser

soest = xbmcaddon.Addon('plugin.soest.page')

addon = xbmcaddon.Addon()

addonname = addon.getAddonInfo('name')
addonicon = addon.getAddonInfo('icon')

script_file = os.path.realpath(__file__)
addondir = os.path.dirname(script_file)

path = 'special://home/addons/plugin.soest.page/resources/'

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'

def MENU():
    addDir('Lokalnachrichten','-',2,path+'rss_orange.png','','')
    addDir('Weltnachrichten','-',13,path+'rss_blau.png','','')
    addDir2('Wetterbericht','-',4,path+'wetter.png','','')
    addDir2('Verkehrsmeldungen','-',5,path+'verkehr.png','','')
    addDir('Veranstaltungen','-',9,path+'events.png','','')
    addDir('Jahres-Highlights','-',11,path+'highlights.png','','')
    addDir('Webcams','-',6,path+'webcams.png','','')
    
def LOKALNACHRICHTEN():
    # https://www.soester-anzeiger.de/lokales/rssfeed.rdf
    # https://www.hellwegradio.de/thema/lokalnachrichten-392.rss
    try:
        RSS_RESOURCE = requests.get('https://www.soester-anzeiger.de/lokales/rssfeed.rdf', headers={'USER-AGENT': USER_AGENT}).text.encode('utf-8')
        xml = minidom.parseString(RSS_RESOURCE).getElementsByTagName('rss')
        channel = xml[0].getElementsByTagName('channel')
        items = channel[0].getElementsByTagName('item')
        rss_items = list()
        for item in items:
            title = item.getElementsByTagName('title')[0].firstChild.wholeText
            desc = item.getElementsByTagName('description')[0].firstChild.wholeText
            link = item.getElementsByTagName('guid')[0].firstChild.wholeText
            pub = item.getElementsByTagName('pubDate')[0].firstChild.wholeText
            do = parser.parse(pub)
            now = do.strftime("%d.%m.%Y - %H:%M")
            title = title.replace('  ', ' ')
            name = title+' [COLOR blue]'+now+' Uhr[/COLOR]'
            addLinkLokalnachrichten1(link,name,desc,'','')
    except:
        RSS_RESOURCE = requests.get('https://www.hellwegradio.de/thema/lokalnachrichten-392.rss', headers={'USER-AGENT': USER_AGENT}).text.encode('utf-8')
        xml = minidom.parseString(RSS_RESOURCE).getElementsByTagName('rss')
        channel = xml[0].getElementsByTagName('channel')
        items = channel[0].getElementsByTagName('item')
        rss_items = list()
        for item in items:
            title = item.getElementsByTagName('title')[0].firstChild.wholeText
            desc = item.getElementsByTagName('description')[0].firstChild.wholeText
            link = item.getElementsByTagName('guid')[0].firstChild.wholeText
            pub = item.getElementsByTagName('pubDate')[0].firstChild.wholeText
            do = parser.parse(pub)
            now = do.strftime("%d.%m.%Y - %H:%M")
            title = title.replace('  ', ' ')
            name = title+' [COLOR blue]'+now+' Uhr[/COLOR]'
            addLinkLokalnachrichten2(link,name,desc,'','')

def addLinkLokalnachrichten1(link,name,desc,urlType,fanart):
    ok=True
    liz=xbmcgui.ListItem(name)
    image = path+'rss_orange.png'
    u=sys.argv[0]+"?url="+link+"&mode=3&name="+name+"&description="+desc
    liz.setProperty('IsPlayable','false')
    liz.setInfo( type="Video", infoLabels={ "Title": name, "plot": desc } )
    liz.setArt({'icon': image, 'thumb': image, 'poster': image, 'fanart': soest.getAddonInfo('fanart')})
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)

def addLinkLokalnachrichten2(link,name,desc,urlType,fanart):
    ok=True
    liz=xbmcgui.ListItem(name)
    image = path+'rss_orange.png'
    u=sys.argv[0]+"?url="+link+"&mode=33&name="+name+"&description="+desc
    liz.setProperty('IsPlayable','false')
    liz.setInfo( type="Video", infoLabels={ "Title": name, "plot": desc } )
    liz.setArt({'icon': image, 'thumb': image, 'poster': image, 'fanart': soest.getAddonInfo('fanart')})
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)

def WELTNACHRICHTEN():
    try:
        RSS_RESOURCE = requests.get('https://www.hellwegradio.de/thema/weltnachrichten-391.rss', headers={'USER-AGENT': USER_AGENT}).text.encode('utf-8')
        xml = minidom.parseString(RSS_RESOURCE).getElementsByTagName('rss')
        channel = xml[0].getElementsByTagName('channel')
        items = channel[0].getElementsByTagName('item')
        rss_items = list()
        for item in items:
            title = item.getElementsByTagName('title')[0].firstChild.wholeText
            desc = item.getElementsByTagName('description')[0].firstChild.wholeText
            link = item.getElementsByTagName('guid')[0].firstChild.wholeText
            pub = item.getElementsByTagName('pubDate')[0].firstChild.wholeText
            do = parser.parse(pub)
            now = do.strftime("%d.%m.%Y - %H:%M")
            title = title.replace('  ', ' ')
            name = title+' [COLOR blue]'+now+' Uhr[/COLOR]'
            addLinkWeltnachrichten(link,name,desc,'','')
    except:
        pass

def addLinkWeltnachrichten(link,name,desc,urlType,fanart):
    ok=True
    liz=xbmcgui.ListItem(name)
    image = path+'rss_blau.png'
    u=sys.argv[0]+"?url="+link+"&mode=14&name="+name+"&description="+desc
    liz.setProperty('IsPlayable','false')
    liz.setInfo( type="Video", infoLabels={ "Title": name, "plot": desc } )
    liz.setArt({'icon': image, 'thumb': image, 'poster': image, 'fanart': soest.getAddonInfo('fanart')})
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)

def KALENDER():
    r = requests.get("https://www.wms-soest.de/aktivitaeten/veranstaltungskalender/")
    soup = BeautifulSoup(r.content, 'html.parser')
    datum = soup.find_all(class_="eventDate")
    beschreibung = soup.find_all(class_="eventListInfos")
    i = 0
    for date,desc in zip(datum, beschreibung):
        date = date.get_text()
        date = date.lstrip()
        date = date.rstrip()
        date = date.replace(' )', ')')
        date = ' [COLOR blue]'+date+'[/COLOR]'
        name = re.compile('<h4><a href="(.+?)</a></h4>').findall(r.content)[i]
        name = name.decode('utf-8')
        name = name.split('>')[-1]
        name = name+date
        desc = desc.get_text()
        desc = desc.replace(' )', ')')
        desc = desc.replace('Details', '')
        desc = desc.lstrip()
        desc = desc.rstrip()
        desc = desc.replace('\n', ' ').replace('\r', '')
        addLinkKalender(name,desc,'','')
        i = i + 1

def HIGHLIGHTS():
    r = requests.get("https://www.wms-soest.de/stadtfeste/unsere-jahres-highlights/")
    html = re.compile('data-small="(.+?)" alt="(.+?)"').findall(r.content)
    for image,name in html:
        image = 'https://www.wms-soest.de/'+image
        name = name.replace('  ', ' ')
        addLinkEvents(name,image,'','')

def WEBCAMS():
    webcamname = ["Blick auf den Markt"]
    webcamurls = ["https://www.wms-soest.de/uploads/webcam/1/webcam.jpg"]
    for name,url in zip(webcamname, webcamurls):
       addLinkWebcams(name,url,'','')

def addLinkWebcams(name,url,urlType,fanart):
    ok=True
    liz=xbmcgui.ListItem(name)
    num = random.randint(10000, 99999999)
    image = url+'?rnd='+str(num)
    u=sys.argv[0]+"?url="+url+"&mode=7"
    liz.setProperty('IsPlayable','false')
    liz.setInfo( type="Video", infoLabels={ "Title": name, "plot": name } )
    liz.setArt({'icon': image, 'thumb': image, 'poster': image, 'fanart': soest.getAddonInfo('fanart')})
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)

def addLinkEvents(name,image,urlType,fanart):
    ok=True
    desc = name
    u=sys.argv[0]+"?url="+image+"&mode=12"    
    liz=xbmcgui.ListItem(name)
    liz.setInfo( type="video", infoLabels={ "Title": name, "plot": name } )
    liz.setProperty('IsPlayable','false')
    liz.setArt({'icon': image, 'thumb': image, 'poster': image, 'fanart': soest.getAddonInfo('fanart')})
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)

def addLinkKalender(name,desc,urlType,fanart):
    ok=True
    liz=xbmcgui.ListItem(name)
    image = path+'events.png'
    u=sys.argv[0]+"?url="+image+"&mode=12"
    liz.setProperty('IsPlayable','false')
    liz.setInfo( type="Video", infoLabels={ "Title": name, "plot": desc } )
    liz.setArt({'icon': image, 'thumb': image, 'poster': image, 'fanart': soest.getAddonInfo('fanart')})
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)

def addDir(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setArt({'fanart': soest.getAddonInfo('fanart')})
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addDir2(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setArt({'fanart': soest.getAddonInfo('fanart')})
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param                   

def setView(content, viewType):
    # set content type so library shows more views and info
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if ADDON.getSetting('auto-view')=='true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % viewType )
            
params=get_params()
url=None
name=None
mode=None
iconimage=None
fanart=None
description=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:        
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass
   
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
    print("")
    MENU()
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==1:
    OPEN_URL(url)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==2:
    print("")
    LOKALNACHRICHTEN()
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==3:
    print("")
    r = requests.get(url, headers={'USER-AGENT': USER_AGENT})
    text = re.findall('<p class="id-Article-content-item id-Article-content-item-summary"(.*?)<aside class="id-Article-margin">',r.content,re.DOTALL|re.MULTILINE)[0]
    text = text.replace('<h3','[CR][CR]<h3')
    text = text.replace('</h3>','[CR][CR]')
    tags = re.findall("<[^>]+>",text)
    for tag in tags:
        text=text.replace(tag,'')
    text = text[1:]
    text = text.lstrip()
    text = text.rstrip()    
    try:
        text = text.decode('utf-8').encode('utf-8')
    except:
        pass
    try:
        text = text.replace('&Auml;','Ä')
        text = text.replace('&auml;','ä')
        text = text.replace('&Uuml;','Ü')
        text = text.replace('&uuml;','ü')
        text = text.replace('&Ouml;','Ö')
        text = text.replace('&ouml;','ö')
        text = text.replace('&szlig;','ß')
        text = text.replace('&amp;','&')
        text = text.replace('&bdquo;','"')
        text = text.replace('&ldquo;','"')
        text = text.replace('&sect;','§')
        text = text.replace('&ndash','-')
        text = text.replace('&eacute;','é')
    except:
        pass
    dialog = xbmcgui.Dialog()
    dialog.textviewer('Lokalnachrichten', name+'[CR][CR]'+text)
    sys.exit(0)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==33:
    print("")
    r = requests.get(url, headers={'USER-AGENT': USER_AGENT})
    text = re.findall('<div class="col s12"><p>(.*?)</article>',r.content,re.DOTALL|re.MULTILINE)[0]
    tags = re.findall("<[^>]+>",text)
    for tag in tags:
        text=text.replace(tag,'')
    text = text.lstrip()
    text = text.rstrip()
    try:
        text = text.decode('utf-8').encode('utf-8')
    except:
        pass
    try:
        text = text.replace('&#xC4;','Ä')
        text = text.replace('&#xE4;','ä')
        text = text.replace('&#xDC;;','Ü')
        text = text.replace('&#xFC;','ü')
        text = text.replace('&#xD6;','Ö')
        text = text.replace('&#xF6;','ö')
        text = text.replace('&#xDF;','ß')
        text = text.replace('&#x26','&')
        text = text.replace('&#xA7;','§')
        text = text.replace('&#xAB;','"')
        text = text.replace('&#xBB;','"')
        text = text.replace('&#xA9;','©')
        text = text.replace('&#x2013;','-')
        text = text.replace('&#xE9;','é')
        text = text.replace('&#xA0;',' ')
        text = text.replace('&quot;','"')
    except:
        pass
    dialog = xbmcgui.Dialog()
    dialog.textviewer('Lokalnachrichten', name+'[CR][CR]'+text)
    sys.exit(0)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==4:
    print("")
    try:
        r = requests.get('https://www.dwd.de/DWD/warnungen/warnapp_gemeinden/json/warnings_gemeinde_nrw.html', headers={'USER-AGENT': USER_AGENT})
        wetter = re.compile('<h2 id="Stadt Soest">Stadt Soest</h2>(.+?)</table>').findall(r.content.decode('utf-8'))[0]
        wetter = wetter.replace('Schlagzeile','')
        wetter = wetter.replace('G&uuml;ltig von','')
        wetter = wetter.replace('G&uuml;ltig bis','')
        wetter = wetter.replace('Beschreibung','')
        wetter = wetter.replace('</td><td>',' - ')
        wetter = wetter.replace('</tr><tr>','[CR]')
        h = HTMLParser.HTMLParser()
        txt = h.unescape(wetter)
        tags = re.findall("<[^>]+>",wetter)
        for tag in tags:
            txt=txt.replace(tag,'')
        wetter = txt
        wetter = wetter.lstrip()
        wetter = wetter.rstrip()
        wetter1 = "[COLOR blue][B]Unwetterwarnungen:[/B][/COLOR][CR]"+wetter+"[CR][CR]"
    except:
        wetter1 = ''
    try:
        r = requests.get('https://www.wetter.com/deutschland/soest/DE0009935.html', headers={'USER-AGENT': USER_AGENT})
        wetter = re.findall('<p class="json-ld-answer">(.*?)</p>',r.content.decode('utf-8'),re.DOTALL|re.MULTILINE)[0]
        wetter = wetter.lstrip()
        wetter = wetter.rstrip()
        wetter2 = "[COLOR blue][B]Heute:[/B][/COLOR][CR]"+wetter+"[CR][CR]"
    except:
        wetter2 = ''
    try:
        r = requests.get('https://www.wetterdienst.de/Deutschlandwetter/Soest_Westfalen/', headers={'USER-AGENT': USER_AGENT})
        wetter = re.findall('<h3>Wettervorhersage für Soest, Westfalen</h3>(.*?)</p></div>',r.content,re.DOTALL|re.MULTILINE)[0]
        wetter = wetter.decode('utf-8')
        wetter = wetter.replace('<div class="clear"></div>','')
        wetter = wetter.replace('<p>','')
        wetter = wetter.replace('</p>','')
        wetter = wetter.lstrip()
        wetter = wetter.rstrip()
        wetter3 = "[COLOR blue][B]Verlauf:[/B][/COLOR][CR]"+wetter+"[CR][CR]"
    except:
        wetter3 = ''  
    dialog = xbmcgui.Dialog()
    dialog.textviewer('Wettervorhersage für den Kreis Soest', wetter1+wetter2+wetter3)
    # Optional
    xbmc.executebuiltin('xbmc.activatewindow(home)')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==5:
    print("")
    r = requests.get('https://api-prod.nrwlokalradios.com/traffic/detail?station=40')
    json_data = json.loads(r.content)
    try:
        stud_list = json_data['local']['accident']
        unfalle = ''
        for i in stud_list:
            do = parser.parse(i['datecreated'])
            zeit = do.strftime("%d.%m.%Y - %H:%M")
            zeit = '[COLOR aqua]'+zeit+' Uhr[/COLOR]'
            wo = '[COLOR red]'+i['autobahn']+'[/COLOR]'
            richtung = '[COLOR yellow]'+i['direction']+'[/COLOR]'
            unfalle += zeit+' '+wo+' '+richtung+' '+i['message']+'\n\n'
        unfalle = unfalle[:-2]
        unfalle = unfalle.replace('  ', ' ')
        if not unfalle:
            unfalle = '[COLOR blue][B]Unfälle:[/B][/COLOR][CR]Es liegen keine aktuellen Meldungen über Unfälle vor.'
        else:
            unfalle = '[COLOR blue][B]Unfälle:[/B][/COLOR][CR]'+unfalle.encode('utf-8')
    except:
        unfalle = '[COLOR blue][B]Unfälle:[/B][/COLOR][CR]Es liegen keine aktuellen Meldungen über Unfälle vor.'
    try:
        stud_list = json_data['local']['trafficjam']
        staus = ''
        for i in stud_list:
            do = parser.parse(i['datecreated'])
            zeit = do.strftime("%d.%m.%Y - %H:%M")
            zeit = '[COLOR aqua]'+zeit+' Uhr[/COLOR]'
            wo = '[COLOR red]'+i['autobahn']+'[/COLOR]'
            richtung = '[COLOR yellow]'+i['direction']+'[/COLOR]'
            staus += zeit+' '+wo+' '+richtung+' '+i['message']+'\n\n'
        staus = staus[:-2]
        staus = staus.replace('  ', ' ')
        if not staus:
            staus = '[COLOR blue][B]Staus:[/B][/COLOR][CR]Es liegen keine aktuellen Meldungen über Staus vor.'
        else:
            staus = '[COLOR blue][B]Staus:[/B][/COLOR][CR]'+staus.encode('utf-8')
    except:
        staus = '[COLOR blue][B]Staus:[/B][/COLOR][CR]Es liegen keine aktuellen Meldungen über Staus vor.'
    try:
        stud_list = json_data['local']['construction']
        baustellen = ''
        for i in stud_list:
            do = parser.parse(i['datecreated'])
            zeit = do.strftime("%d.%m.%Y - %H:%M")
            zeit = '[COLOR aqua]'+zeit+' Uhr[/COLOR]'
            wo = '[COLOR red]'+i['autobahn']+'[/COLOR]'
            richtung = '[COLOR yellow]'+i['direction']+'[/COLOR]'
            baustellen += zeit+' '+wo+' '+richtung+' '+i['message']+'\n\n'
        baustellen = baustellen[:-2]
        baustellen = baustellen.replace('  ', ' ')
        if not baustellen:
            baustellen = '[COLOR blue][B]Baustellen:[/B][/COLOR][CR]Es liegen keine aktuellen Meldungen über Baustellen vor.'
        else:
            baustellen = '[COLOR blue][B]Baustellen:[/B][/COLOR][CR]'+baustellen.encode('utf-8')
    except:
        baustellen = '[COLOR blue][B]Baustellen:[/B][/COLOR][CR]Es liegen keine aktuellen Meldungen über Baustellen vor.'
    try:
        stud_list = json_data['local']['warning']
        warnungen = ''
        for i in stud_list:
            do = parser.parse(i['datecreated'])
            zeit = do.strftime("%d.%m.%Y - %H:%M")
            zeit = '[COLOR aqua]'+zeit+' Uhr[/COLOR]'
            wo = '[COLOR red]'+i['autobahn']+'[/COLOR]'
            richtung = '[COLOR yellow]'+i['direction']+'[/COLOR]'
            warnungen += zeit+' '+wo+' '+richtung+' '+i['message']+'\n\n'
        warnungen = warnungen[:-2]
        warnungen = warnungen.replace('  ', ' ')
        if not warnungen:
            warnungen = '[COLOR blue][B]Warnungen:[/B][/COLOR][CR]Es liegen keine aktuellen Meldungen über Warnungen vor.'
        else:
            warnungen = '[COLOR blue][B]Warnungen:[/B][/COLOR][CR]'+warnungen.encode('utf-8')
    except:
        warnungen = '[COLOR blue][B]Warnungen:[/B][/COLOR][CR]Es liegen keine aktuellen Meldungen über Warnungen vor.'       
    try:
        stud_list = json_data['radars']
        radar = ''
        for i in stud_list:
            radar += i['message']+'\n\n'
        radar = radar[:-2]
        radar = radar.replace('  ', ' ')
        radar = radar.replace('<br />', '[CR]')
        if not radar:
            radar = '[COLOR blue][B]Blitermeldungen:[/B][/COLOR][CR]Es liegen keine aktuellen Meldungen über Blitzer vor.'
        else:
            radar = '[COLOR blue][B]Blitermeldungen:[/B][/COLOR][CR]'+radar.encode('utf-8')
    except:
        radar = '[COLOR blue][B]Blitermeldungen:[/B][/COLOR][CR]Es liegen keine aktuellen Meldungen über Blitzer vor.'
    
    r = requests.get('https://soest.polizei.nrw/artikel/radar-messstellen/', headers={'USER-AGENT': USER_AGENT})
    messstellen = re.findall('<div property="schema:text" class="field__item">(.*?)</div>',r.content.decode('utf-8'),re.DOTALL|re.MULTILINE)[0]
    messstellen = messstellen.replace('<b>','[CR]')
    messstellen = messstellen.replace('<br />','[CR]')
    messstellen = messstellen.replace('</p>','[CR]')
    messstellen = messstellen.replace('<span style="font-size: 12pt;"><span style="font-family: &quot;Arial&quot;,sans-serif;">','')
    h = HTMLParser.HTMLParser()
    txt = h.unescape(messstellen)
    tags = re.findall("<[^>]+>",messstellen)
    for tag in tags:
        txt=txt.replace(tag,'')
    messstellen = txt
    messstellen = "".join(messstellen.splitlines())
    messstellen = messstellen[17:]
    messstellen = messstellen[:-16] 
    messstellen = messstellen.lstrip()
    messstellen = messstellen.rstrip()
    messstellen = '[COLOR blue][B]Radar-Messstellen:[/B][/COLOR][CR]'+messstellen.encode('utf-8')
    text = unfalle+'[CR][CR]'+staus+'[CR][CR]'+baustellen+'[CR][CR]'+warnungen+'[CR][CR]'+radar+'[CR][CR]'+messstellen
    text = text.replace('<br />', ' ') 
    dialog = xbmcgui.Dialog()
    dialog.textviewer('Verkehrsmeldungen für den Kreis Soest', text)
    # Optional
    xbmc.executebuiltin('xbmc.activatewindow(home)')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==6:
    print("")
    WEBCAMS()
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==7:
    print("")
    num = random.randint(10000, 99999999)
    snap = str(url)+'?rnd='+str(num)
    xbmc.executebuiltin('ShowPicture('+snap+')')

elif mode==9:
    print("")
    KALENDER()
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==11:
    print("")
    HIGHLIGHTS()
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==12:
    print("")
    xbmc.executebuiltin("Container.Refresh")
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==13:
    print("")
    WELTNACHRICHTEN()
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==14:
    print("")
    r = requests.get(url, headers={'USER-AGENT': USER_AGENT})
    text = re.findall('<div class="row"><div class="col s12">(.*?)</article>',r.content,re.DOTALL|re.MULTILINE)[0]
    text = text.replace('<p','[CR]<p')
    text = text.replace('</p>','[CR]')
    tags = re.findall("<[^>]+>",text)
    for tag in tags:
        text=text.replace(tag,'')
    text = text.lstrip()
    text = text.rstrip()
    try:
        text = text.decode('utf-8').encode('utf-8')
    except:
        pass
    try:
        text = text.replace('&#xC4;','Ä')
        text = text.replace('&#xE4;','ä')
        text = text.replace('&#xDC;;','Ü')
        text = text.replace('&#xFC;','ü')
        text = text.replace('&#xD6;','Ö')
        text = text.replace('&#xF6;','ö')
        text = text.replace('&#xDF;','ß')
        text = text.replace('&#x26','&')
        text = text.replace('&#xA7;','§')
        text = text.replace('&#xAB;','"')
        text = text.replace('&#xBB;','"')
        text = text.replace('&#xA9;','©')
        text = text.replace('&#x2013;','-')
        text = text.replace('&#xE9;','é')
        text = text.replace('&#xA0;',' ')
        text = text.replace('&quot;','"')
    except:
        pass
    dialog = xbmcgui.Dialog()
    dialog.textviewer('NRW, Deutschland und die Welt', name+'[CR][CR]'+text)
    sys.exit(0)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))