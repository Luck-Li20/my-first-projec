# -*- coding: utf-8 -*-
"""
**************************************
*  @Author  ：   李忠科
*  @Time    ：   2025-07-23 19:27
*  @Project :   Python_reptile
*  @FileName:   main.py
**************************************
"""
# -*- coding: utf-8 -*-
# @Time    : 2023-12-20 1:44
# @Author  : AmoXiang
# @File    : main.py
# @Software: PyCharm
# @Blog: https://blog.csdn.net/xw1680
import os.path
import sys

from scrapy.cmdline import execute

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# execute(["scrapy", "crawl", "quotes"])
execute("scrapy crawl nike_spider".split(" "))
