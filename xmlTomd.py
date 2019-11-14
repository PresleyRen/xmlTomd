# -*- coding: utf-8 -*-
# @Author: Mehaei
# @Date:   2019-11-13 10:21:20
# @Last Modified by:   Mehaei
# @Last Modified time: 2019-11-14 14:06:04

import os
import re
import sys
import time
import random
import datetime
import logging
import logging.handlers

import tomd

AUTHOR = "Mehaei"

MD_HEAD = """
---
layout:     post
title:      {title}
subtitle:   {subtitle}
date:       {date}
author:     {author}
header-img: {header_img}
catalog: true
tags:
    - python
---
"""

HEADER_IMG_LIST = ["post-sample-image.jpg", "post-bg-digital-native.jpg", "post-bg-kuaidi.jpg", "post-bg-miui6.jpg", "post-bg-universe.jpg", "post-bg-ios9-web.jpg", "post-bg-cook.jpg", "post-bg-miui-ux.jpg", "post-bg-re-vs-ng2.jpg", "post-bg-rwd.jpg", "post-bg-YesOrNo.jpg", "post-bg-android.jpg", "post-bg-coffee.jpeg", "post-bg-debug.png", "post-bg-e2e-ux.jpg", "post-bg-js-version.jpg", "post-bg-hacker.jpg", "post-bg-ios10.jpg", "post-bg-ioses.jpg", "post-bg-desk.jpg", "post-bg-github-cup.jpg", "post-bg-iWatch.jpg", "post-bg-mma-6.jpg", "post-bg-mma-4.jpg", "post-bg-alibaba.jpg", "post-bg-mma-5.jpg", "post-bg-mma-1.jpg", "home-bg-geek.jpg", "post-bg-swift2.jpg", "post-bg-mma-0.png", "post-bg-unix-linux.jpg", "post-bg-mma-2.jpg", "post-bg-swift.jpg", "post-bg-keybord.jpg", "post-bg-os-metro.jpg", "post-bg-BJJ.jpg", "post-bg-map.jpg", "post-bg-2015.jpg"]

logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s %(name)s %(filename)s[line:%(lineno)d] %(funcName)s %(levelname)s %(message)s',
    handlers=[logging.handlers.RotatingFileHandler("run_debug.log", maxBytes=1024 * 1024 * 10, backupCount=5, encoding="utf-8")]
)


class XmlToMd(object):

    def __init__(self, xml_file_list=None):
        if not xml_file_list:
            return False
        self._loads_args()
        self._loads_file(xml_file_list)
        self._loads_re_pat()

    def _loads_args(self):
        self.md_sucess_count = 0
        self.md_faild_count = 0
        self.xml_post_total = 0
        self.start_time = time.time()

    def _loads_re_pat(self):
        self.post_pat = re.compile(r'<item>(.+?)</item>', re.S)
        self.post_title_pat = re.compile(r'<title>(.+?)</title>')
        self.post_date_pat = re.compile(r'<pubDate>(.+?)</pubDate>')
        self.space_pat = re.compile(r'[\[\]\s/]+')

    def _loads_file(self, file_list, file_path=None):
        if not file_path:
            file_path = os.getcwd()
        self.md_dir_pname = "%s/%s" % (file_path, "md_data")
        self.xml_dir_pname = "%s/%s" % (file_path, "xml_data")

        for data_dir in [self.md_dir_pname, self.xml_dir_pname]:
            if os.path.exists(data_dir):
                continue
            else:
                os.makedirs(data_dir)

        self.abs_xml_file_list = []
        for xml_pname in file_list:
            if os.path.isabs(xml_pname):
                self.abs_xml_file_list.append(xml_pname)
            elif xml_pname.startswith("."):
                self.abs_xml_file_list.append(os.path.abspath(xml_pname))
            else:
                self.abs_xml_file_list.append(os.path.join(self.xml_dir_pname, xml_pname))
        logging.debug("xml file to abs pname done, count file: %s" % len(self.abs_xml_file_list))

    def start_work(self):
        for file_pname in self.abs_xml_file_list:
            if not os.path.exists(file_pname):
                logging.debug("%s not exists" % file_pname)
                continue
            with open(file_pname, "r+", encoding='utf-8') as f:
                self.gen_md_file(f.read())
        logging.debug("xml to md done, spend time: %s \npost total: %s, to md result: \nsuccess: %s, faild: %s" % (time.time() - self.start_time, self.xml_post_total, self.md_sucess_count, self.md_faild_count))

    def gen_md_file(self, html):
        item_list = self.post_pat.findall(html)
        self.xml_post_total = len(item_list)
        logging.debug("find post total: %s" % len(item_list))
        for item in item_list:
            try:
                self.desc_to_md(item)
                self.md_sucess_count += 1
            except Exception as e:
                logging.debug(e)
                self.md_faild_count += 1
                continue

    def desc_to_md(self, desc):
        md_head, file_pname = self.get_md_head_and_file_pname(desc)

        with open(file_pname, "w+", encoding='utf-8') as f:
            f.write(md_head.strip("\n") + tomd.Tomd(desc).markdown)

    def get_md_head_and_file_pname(self, desc):

        file_name = self.post_title_pat.findall(desc)[0]
        file_name = self.space_pat.sub('', file_name)
        pub_date = self.get_datetime(self.post_date_pat.findall(desc)[0])

        md_head = MD_HEAD.format(title=file_name, subtitle="", date=pub_date, author=AUTHOR, header_img="%s/%s" % ("img", random.choice(HEADER_IMG_LIST)))
        file_pname = "%s/%s-%s.md" % (self.md_dir_pname, pub_date, file_name)
        
        return md_head, file_pname

    def get_datetime(self, date):
        GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
        n_time = datetime.datetime.strptime(date, GMT_FORMAT)
        return str(n_time)[:10]


if __name__ == "__main__":
    xml_file_list = sys.argv[1:]
    xmltomd = XmlToMd(xml_file_list)
    xmltomd.start_work()
