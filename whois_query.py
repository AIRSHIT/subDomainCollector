import requests
import json
import os
import time
from bs4 import BeautifulSoup

whois_url = 'http://whois.chinaz.com/'

#Reverse query by name
def r_query_by_name(name):
    url = whois_url + "reverse?host=" + name + "&ddlSearchMode=2"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    match_domain = soup.find_all(attrs={"class":"w13-0 domain"})
    del match_domain[0]
    match_postbox = soup.find_all(attrs={"class":"w13-0 postbox"})
    del match_postbox[0]
    res = []
    for i in xrange(len(match_domain)):
        dict = {"domain": match_domain[i].div.string, "mail": match_postbox[i].div.string}
        res.append(dict)
    return res

#Reverse query by mail
def r_query_by_mail(mail):
    url = whois_url + "reverse?host=" + mail + "&ddlSearchMode=1"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    match_domain = soup.find_all(attrs={"class":"w13-0 domain"})
    del match_domain[0]
    match_name = soup.find_all(attrs={"class":"w13-0 man"})
    del match_name[0]
    res = []
    for i in xrange(len(match_domain)):
        dict = {"domain": match_domain[i].div.string, "name": match_name[i].div.string}
        res.append(dict)
    return res

def name_main_query(domain):
    url = whois_url + domain
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    match = soup.find_all(attrs={"class":"fr WhLeList-right block ball lh24"})

    if len(match) == 2:
        name = match[0].span.string
        mail = match[1].span.string
    else:
        name = ''
        mail = ''
    
    res = {}
    res['name'] = name
    res['mail'] = mail
    return res

def query(domain):
    res = name_main_query(domain)

    if res['name']:
        res1 = r_query_by_name(res['name'])
    else:
        res1 = {}

    if res['mail']:
        res2 = r_query_by_mail(res['mail'])
    else:
        res2 = {}

    path = os.path.join(os.getcwd(), 'res')
    path = os.path.join(os.getcwd(), domain)
    path = os.path.join(path, domain + '_reverse_query.txt')
    f = open(path, 'w')
    f.write("Reverse_query_by_name" +'\n')
    f.write(json.dumps(res1) +'\n')
    f.write("Reverse_query_by_mail" +'\n')
    f.write(json.dumps(res2) +'\n')
    f.close()

    time.sleep(3)