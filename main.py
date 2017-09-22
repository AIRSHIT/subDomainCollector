import os
import json
import re
import sys
import traceback
import logging
import subprocess
import shlex
import whois_query
import requests
import urlparse
import traceback
import socket

#Check the domain is resolveable
def check_add(domain):
    try:
        ip = socket.gethostbyname(domain)
    except:
        return {'status': False}
    return {'status': True, 'ip': ip}

#Check the WebService is work
def check_available(domain, hash_m):
    url = "http://" + domain
    res = {}
    try:
        r = requests.get(url, timeout=6)
        urlp = urlparse.urlparse(r.url)
        res = {'status': r.status_code, 'domain': urlp.netloc}
        hash_s = hash(r.content)
        if hash_m == hash_s:
            res['page_sta'] = 'Maybe Same page.'
        else:
            res['page_sta'] = 'All good.'
    except requests.exceptions.TooManyRedirects:
        res = {'status': 'Too many redirect'}
    except requests.exceptions.ConnectTimeout:
        res = {'status': 'Request timeout'}
    except:
        res = {'status': 'Unavailable'}
    try:
        r
    except:
        res['domain'] = domain
        res['page_sta'] = 'PageError'
        
    return res

#Get the domain list
def get_Domain_list():
    file_path = 'domain_list.txt'
    f = open(file_path, 'r')
    lines = f.readlines()
    f.close()
    return lines
domain_list = get_Domain_list()

#Brute way 1
def start_wydomainAPI(domain):
    old_pwd = os.getcwd()
    pwd = os.path.join(os.getcwd(), 'wydomain')
    os.chdir(pwd)
    os.system('python wydomain.py -d ' + domain)
    os.chdir(old_pwd)

#Brute way 2
def start_wydomainbrute(domain):
    old_pwd = os.getcwd()
    pwd = os.path.join(os.getcwd(), 'wydomain')
    os.chdir(pwd)
    os.system('python dnsburte.py -d ' + domain)
    os.chdir(old_pwd)

#Brute way 3
def start_bruteljj(domain):
    old_pwd = os.getcwd()
    pwd = os.path.join(os.getcwd(), 'subDomainsBrute')
    os.chdir(pwd)
    os.system('python subDomainsBrute.py ' + domain)
    os.chdir(old_pwd)

#Merge result
def mergeRes(domain):
    res_1 = os.path.join(os.getcwd(), 'wydomain')
    res_1 = os.path.join(res_1, 'bruteforce.log')

    res_2 = os.path.join(os.getcwd(), 'wydomain')
    res_2 = os.path.join(res_2, 'domains.log')

    res_3 = os.path.join(os.getcwd(), 'subDomainsBrute')
    res_3 = os.path.join(res_3, domain + '.txt')

    data = []

    f = open(res_1, 'r')
    data_1 = json.load(f)
    data.extend(data_1)
    f.close()

    f = open(res_2, 'r')
    data_2 = json.load(f)
    data.extend(data_2)
    f.close()

    f = open(res_3, 'r')
    lines = f.readlines()
    f.close()
    data_3 = []
    for i in lines:
        match = re.findall(r'\A.*?\s', i)
        if match:
            data_3 += match
    data.extend(data_3)

    #unitary the resulr
    temp = []
    for i in data:
        i = i.encode(sys.getdefaultencoding())
        i = i.strip()
        temp.append(i)
    data = temp
    data = list(set(data))

    #Write result into file
    logging.info("Write result into file.")
    path = os.path.join(os.getcwd(), 'res')
    try:
        os.mkdir(path)
    except OSError:
        logging.info("Directory already exist.")
    path = os.path.join(path, domain)
    try:
        os.mkdir(path)
    except OSError:
        logging.info("Directory already exist.")
        
    r = requests.get("http://"+domain)
    hash_m = hash(r.content)
    path = os.path.join(path, domain + '.txt')
    f = open(path, 'w')
    for i in data:
        res = check_add(i)
        if res['status']:
            temp = "%40s\t%s\t" % (i, res['ip'])
        else:
            temp = "%40s\tCan't resolved.\t" % (i)
        
        res = check_available(i, hash_m)
        temp = temp + "%20s\t%20s\t%20s\n" % (res['status'], res['domain'], res['page_sta'])
        f.write(temp)
    f.close()

if __name__ == '__main__':
    try:
        for i in domain_list:
            print 'Bruting %s...' % (i)
            i = i.strip()
            start_wydomainbrute(i)
            start_wydomainAPI(i)
            start_bruteljj(i)
            print "Merging result..."
            mergeRes(i)
            whois_query.query(i)
    except KeyboardInterrupt:
        logging.info("Ctrl C - Stopping Client")
        sys.exit(1)
    except Exception, e:
        f = open('errmsg.txt', 'w')
        #f.write(msg)
        traceback.print_exc(file=f)
        f.flush()
        f.close()