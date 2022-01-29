import requests
import json
from PIL import Image
from os import remove
from urllib.request import getproxies

def get_qualitys(jsond):
    qualitys = []
    items = jsond["links"]["mp4"]
    for key, values in items.items():
        string = "mp4: " + "size: " + items[key]["size"] + " " + "q: " + items[key]["q"] + " " + "k: " + items[key]["k"]
        if items[key]["size"] == "" or items[key]["size"] == None:
            pass
        else:
            qualitys.append(string)
    items = jsond["links"]["mp3"]
    for key, values in items.items():
        string = "mp3: " + "size: " + items[key]["size"] + " " + "q: " + items[key]["q"] + " " + "k: " + items[key]["k"]
        if items[key]["size"] == "" or items[key]["size"] == None:
            pass
        else:
            qualitys.append(string)
    return qualitys

def check_url(link):
    try:
        dic = {"q" : link, "vt" : "home"}
        global proxies
        proxies=""
        res = requests.post("https://yt1s.com/api/ajaxSearch/index", dic, proxies=proxies)
        jsond = json.loads(res.text)
        d = jsond["vid"]
        return jsond
    except requests.exceptions.ProxyError:
        try:
            proxies = {'http': getproxies()['http'], 'https': getproxies()['http']}
            res = requests.post("https://yt1s.com/api/ajaxSearch/index", dic, proxies=proxies)
            jsond = json.loads(res.text)
            d = jsond["vid"]
            return jsond
        except KeyError:
            return False
    except KeyError:
            return False
        
def get_dlink(k, vid):
    dic = {"vid" : vid, "k" : k}
    res = requests.post("https://yt1s.com/api/ajaxConvert/convert", dic, proxies=proxies)
    jsond = json.loads(res.text)
    global ftype
    ftype = jsond["ftype"]
    return jsond["dlink"]
    
def get_title(jsond):
    return jsond["title"]

def get_vid(jsond):
    return jsond["vid"]

def get_jpg(vid):
    try:
        link = "https://i.ytimg.com/vi/" + vid + "/0.jpg"
        res = requests.get(link, proxies=proxies)
        name = vid + ".jpg"
        with open(name, "wb") as file:
            file.write(res.content)
        image = Image.open(name)
        new_image = image.resize((150, 150))
        remove(name)
        return new_image
    except requests.exceptions.ConnectionError:
        return False

def get_format():
    return ftype