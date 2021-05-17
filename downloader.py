#!/usr/bin/env python3

import praw
from imgurpython import ImgurClient
from urllib import request
import os
import re
import argparse

def descargarcarpeta(urls, nombrecarpeta,path):
    num = 0
    path_completo = path + "/" + nombrecarpeta
    while os.path.exists(path_completo):
        path_completo = path_completo + str(num)
        num += 1
    os.mkdir(path_completo)

    num = 0
    for url in urls:
        image = request.urlopen(url).read()
        filename = url.split("/")[-1]
        filepath = path_completo + "/" + str(num) + "." + filename.split(".")[-1]
        f = open(filepath,"wb")
        f.write(image)
        f.close()
        num += 1


def descargarsueltos(urls,path_sueltas):
    for url in urls:
        filename = url.split("/")[-1]
        filepath = path_sueltas + "/" + filename
        num = 0
        while os.path.exists(filepath):
            filepath = path_sueltas + "/" + str(num) + filename
            num += 1
        image = request.urlopen(url).read()
        f = open(filepath,"wb")
        f.write(image)
        f.close()

def getimgURL(url,imgur):
    try:
        url_img = []
        album_id = url.split("/")[-1]
        element_type = url.split("/")[-2]
        if element_type == "a":
            album = imgur.get_album(album_id)
            for i in album.images:
                url_img.append(i["link"])
        elif "gallery" in url.split("/"):
            gallery = imgur.gallery_item(url.split("/")[-2])
            for i in gallery.images:
                url_img.append(i["link"])
        else:
            image = imgur.get_image(album_id)
            url_img.append(image.link)
    except Exception as e:
        txt = "Error desconocido\nURL:" + url + "\nError msg:" + str(e) + "\n"
        f = open("log.log","a")
        f.write(txt)
        f.close()
    finally:
        return url_img

def loadConfig(cfgfile,cfg):
    try:
        f = open(cfgfile,"r")
        for line in f.readlines():
            if line[0] == "\n" or line[0] == "#":
                continue
            options = line.split(":")
            if options[0] not in  cfg:
                cfg[options[0]] = options[1].strip("\n")
        f.close()
        reddit = praw.Reddit(client_id=cfg["cidr"], client_secret=cfg["csecr"],password=cfg["passwordr"], user_agent=cfg["uagentr"])
        subreddit = reddit.subreddit(cfg["subreddit_name"])
        imgur = ImgurClient(cfg["cidi"], cfg["cseci"])
        cfg["reddit"] = reddit
        cfg["subreddit"] = subreddit
        cfg["imgur"] = imgur
        sueltas_fullpath = cfg["default_output_path"] + "/"  + cfg["path_sueltas"]
        cfg["path_sueltas"] = sueltas_fullpath
        if not os.path.exists(sueltas_fullpath):
            os.mkdir(sueltas_fullpath)
    except Exception as e:
        print("Error al leer el fichero de configuracion comprueba que todos los parametros son correctos")
        print(str(e))
        exit(1)
    finally:
        return cfg

def readparameters():
    config = {}
    config["configfile"] = "redditdownloader.config"
    parser = argparse.ArgumentParser()
    parser.add_argument("-s",help="Indicar a continuacion el subreddit de donde quieres bajar las imagenes")
    parser.add_argument("-c", help="indicar un fichero de configuracion alternativo para la api de reddit, por defecto es redditdownloader.config")
    parser.add_argument("-o", help="indicar la carpeta donde se almacenara la descarga, por defecto sera la carpeta activa")
    parser.add_argument("-l", help="Para indicar el limite de posts de reddit que se miraran[int]")
    parser.add_argument("-g", help="Para indicar el limite de fotografias que van a sueltos[int]")
    args = parser.parse_args()

    if args.s:
        config["subreddit_name"] = str(args.s)
    if args.c:
        config["configfile"] = args.c
    if args.o:
        config["default_output_path"] = args.o
    if args.l:
        config["limit"] = int(args.l)
    if args.g:
        config["agrupacion"] = int(args.g)
    return config


def main():
    cfg = readparameters()
    cfg = loadConfig(cfg["configfile"],cfg)
    all_subrredit_pages = []
    subreddit = cfg['subreddit']
    for submission in subreddit.new(limit=int(cfg["limit"])):
        if "imgur.com" in submission.url:
            title = re.sub(r'\W+','', submission.title)
            all_subrredit_pages.append([submission.url, title])
        else:
            f = open("urls.txt","a")
            f.write(submission.url + "\n")
            f.close()
    for page in all_subrredit_pages:
        if page[0].endswith(".jpg") or page[0].endswith(".jpeg") or page[0].endswith(".png") or page[0].endswith(".gif") :
            descargarsueltos([page[0]],cfg["path_sueltas"])
        else:
            urlimgs = getimgURL(page[0],cfg["imgur"])
            if len(urlimgs) < int(cfg["agrupacion"]):
                descargarsueltos(urlimgs,cfg["path_sueltas"])
            else:
                descargarcarpeta(urlimgs, page[1],cfg["default_output_path"])

if __name__ == "__main__":
    main()