A Simple Sub-domina brute
======

A simple sub domain brute tool, it use the lijiejie/subDomainsBrute and ring04h/wydomain this two tool to brute sub domain, and merge two tools result.

这个脚本使用了两个工具来爆破子域名，并且合并去重两个工具的结果。

## Dependencies ##
> pip install dnspython gevent request urlparse


## Usage ##
	put the suDomainsBrute and wydomain in this index. 
	Usage: python main.py domain_list.txt


## Other
	res directory is result directory.
	put the lijiejie/subDomainsBrute and ring04h/wydomain in the this program root directory.
	domain_list.txt is the domain list wait to scanner.