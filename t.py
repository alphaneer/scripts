#!/usr/bin/env python
#-*- coding:utf8 -*-
import os
print ("File Name : t.py")
# Power by RehemanYidiresi2018-11-01 10:38:35
print ("Modified by RehemanYidiresi : "+os.popen("ls -l|grep t.py |awk '{print $6,$7,$8}'").read())


