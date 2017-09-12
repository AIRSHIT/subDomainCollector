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

#Check the domain is reachable 
def check_add(domain):
    cmd = "ping -c 1 " + domain
    args = shlex.split(cmd)

    status = False
    try:
        subprocess.check_call(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        status = True
    except subprocess.CalledProcessError:
        status = False
    return status

#Check the WebService is work
def check_available(domain):
    url = "http://" + domain
    r = requests.get(url)
    urlp = urlparse.urlparse(r.url)
    if urlp.netloc == domain:
        return True
    else:
        return False

#Get the domain list
def get_Domain_list():
    file_path = 'domain_list.txt'
    f = open(file_path, 'r')
    lines = f.readlines()
    f.close()
    return lines
domain_list = get_Domain_list()

#Brute wat 1
def start_wydomainAPI(domain):
    old_pwd = os.getcwd()
    pwd = os.path.join(os.getcwd(), 'wydomain')
    os.chdir(pwd)
    os.system('python wydomain.py -d ' + domain)
    os.chdir(old_pwd)

#Brute wat 2
def start_wydomainbrute(domain):
    old_pwd = os.getcwd()
    pwd = os.path.join(os.getcwd(), 'wydomain')
    os.chdir(pwd)
    os.system('python dnsburte.py -d ' + domain)
    os.chdir(old_pwd)

#Brute wat 3
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
    path = os.path.join(os.getcwd(), 'res')
    path = os.path.join(os.getcwd(), domain)
    os.mkdir(path)
    path = os.path.join(path, domain + '.txt')
    f = open(path, 'w')
    for i in data:
        if check_add(i):
            temp = "%24s + '\tUp + '\n'" % (i)
            f.write(temp)
        else:
            temp = "%24s + '\tDown + '\n'" % (i)
            f.write(temp)
    f.close()

if __name__ == '__main__':
    try:
        for i in domain_list:
            i = i.strip()
            start_wydomainbrute(i)
            start_wydomainAPI(i)
            start_bruteljj(i)
            mergeRes(i)
            whois_query.query(i)
    except KeyboardInterrupt:
        logging.info("Ctrl C - Stopping Client")
        sys.exit(1)
    except Exception, e:
        msg = ''
        msg += 'str(Exception):\t'+ str(Exception) + '\n'
        msg += 'str(e):\t\t' + str(e) + '\n'
        msg += 'repr(e):\t' + repr(e) + '\n'
        msg += 'e.message:\t' + e.message + '\n'
        f = open('errmsg.txt', 'w')
        f.write(msg)
        f.close()