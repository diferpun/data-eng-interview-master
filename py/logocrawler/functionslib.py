import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import validators
import csv
import sys

# ###### get_data function ###########
# - Retrieve the data inside a url page
# ###### Parameters ##################
# url        => url where the information is searched
# auth_param => activate proxy_url and auth_key from "http://api.proxiesapi.com" in order to avoid restrictions
# tout       => waiting time for a response
# ###### output ######################
# r => information inside the url

def getdata(url,auth_param=False,tout=5):
    proxy_url = "http://api.proxiesapi.com"  # evitar bloqueo de google scholar
    auth_key  = "63643bce54975c4ff8c57a98d1b6804d_sr98766_ooPq87"  # evitar bloqueo de google scholar
    if auth_param:
       print("hola")
       urlf=f"{proxy_url}/?auth_key={auth_key}&url={url}"
       r=requests.get(url=urlf,timeout=tout).text
    else:
       r = requests.get(url=url,timeout=tout).text
    return r

# ##### check_format ################
# - check if a url contains a valid url image
# ##### Parameters ##################
# url_img => possible url image
# ###### output #####################
# final_flag  => a flag that shows if a url is valid (True) or nor (False)

def check_format(url_img):
    img_formats = ['png', 'jpg', 'bmp', 'gif', 'eps', 'svg', 'pdf']
    aux=url_img.split(".")
    format_flag=aux[-1].lower() in img_formats
    if not validators.url(url_img):
        url_flag = False
    else:
        url_flag = True
    final_flag=(url_flag and format_flag)
    return final_flag

# ##### get_icon function ####################
# - get the image url
# ###### Parameters       ####################
# url        => url where the information is searched
# auth_param => activate proxy_url and auth_key from "http://api.proxiesapi.com" in order to avoid restrictions
# tout       => waiting time for a response
# ###### output #############################
# url_img => variable of two possible values url image if it is valid or None if it is not valid

def get_icon(url,auth_param=False,tout=5,verbose=False):
    time.sleep(2)
    url=url.strip()
    try:
        htmldata = getdata(url=url,auth_param=auth_param,tout=tout)
        soup = BeautifulSoup(htmldata,'html.parser')
        for item in soup.find_all('img'):
           flag_im=check_format(item['src'])
           if item['src'] is not None and flag_im:
              flag_emtpy=True
              url_img=item['src']
              break
        if not flag_emtpy:
            print(url, "error")
            return None
        else:
            if verbose:
                print(url,"ok")
            return url_img
    except:
        if verbose:
           print(url, "error")
        return None

# ##### logo_collector function ##############
# read and search logo images from the web pages inside websites.csv
# ###### Parameters   ####################
# file_path => path to websites.csv
# ######  ####################
# wp_im_df => a dataframe whitch contains three columns url, logo_url and status (one for url and zero for no url)


def logo_collector(file_path='files/websites.csv',verbose=False,auth_param=False):
    wp_im_df = pd.DataFrame(columns=["web_page", "url_logo", "status"])
    wps_df = pd.read_csv(file_path, header=None)
    nw= len(wps_df.index)
    wps_df = wps_df.astype({0: 'string'})
    wps_df[0]="http://"+wps_df[0]
    for i,wb in enumerate(wps_df.values.tolist()):
        img_url=get_icon(wb[0],auth_param=auth_param,tout=5,verbose=verbose)
        if img_url is not None:
            wp_im_df = wp_im_df.append({"web_page": str(wb[0]),
                                        "url_logo": str(img_url), "status": 1},ignore_index=True)
        else:
            wp_im_df = wp_im_df.append({"web_page": str(wb[0]),
                                        "url_logo": "error", "status": 0}, ignore_index=True)
    wp_im_df.to_csv("LogoRecovery.csv", sep=';', header=True)
    return wp_im_df