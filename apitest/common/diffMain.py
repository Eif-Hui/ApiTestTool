# -*- coding: utf-8 -*-
# @Time    : 2021/6/20 7:47 上午
# @Author  : Hui
# @File    : diffMain.py


import difflib
hd = difflib.HtmlDiff()
loads = ''
with open('D:\difflib\guihuatxt.txt','r') as load:
    loads = load.readlines()
    load.close()

mems = ''
with open('D:\difflib\zichan.txt', 'r') as mem:
    mems = mem.readlines()
    mem.close()

with open('diffout.html','a+') as fo:
    fo.write(hd.make_file(loads,mems))
    fo.close()