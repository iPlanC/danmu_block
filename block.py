"""
Author: PlanC
Date: 2020-11-05 08:49:19
LastEditTime: 2020-11-05 11:14:50
FilePath: \danmu_block\block.py
"""
"""
Author: PlanC
Date: 2020-08-31 11:36:33
LastEditTime: 2020-11-05 10:58:16
FilePath: \danmu_block\block.py
"""
#%%

import os
import json
import requests
import time
import MySQLdb
import jieba.analyse
import xml.dom.minidom
from lxml import etree

class Bilibili():
    """docstring for Bilibili"""
    def __init__(self, cid):
        self.headers = {
        "Host": "comment.bilibili.com",
        "Connection": "keep-alive",
        "Cache-Control": "max-age = 0",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36",
        "Accept": "text/html, application/xhtml + xml, application/xml;q = 0.9, image/webp, image/apng, */*;q = 0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN, zh;q = 0.9",
        "Cookie": "finger = edc6ecda; LIVE_BUVID = AUTO1415378023816310; stardustvideo = 1; CURRENT_FNVAL = 8; buvid3 = 0D8F3D74-987D-442D-99CF-42BC9A967709149017infoc; rpdid = olwimklsiidoskmqwipww; fts = 1537803390"
        }
        self.url = "http://comment.bilibili.com/" + str(cid) + ".xml"
        self.barrage_reault = self.get_page()

    # 获取信息
    def get_page(self):
        try:
            # 延时操作，防止太快爬取
            time.sleep(0.5)
            response = requests.get(self.url, headers = self.headers)
        except Exception as e:
            print("获取xml内容失败, %s" % e)
            return False
        else:
            if response.status_code == 200:
                # 下载xml文件
                with open("bilibili.xml", "wb") as f:
                    f.write(response.content)
                return True
            else:
                return False

    # 解析网页
    def param_page(self):
        time.sleep(1)
        if self.barrage_reault:
            # 文件路径，html解析器
            html = etree.parse("bilibili.xml", etree.HTMLParser())
            # xpath解析，获取当前所有的d标签下的所有文本内容
            results = html.xpath("//d//text()")
            return results

    # 词云制作
    def make_wordCloud(self, bvid):
        doc = xml.dom.minidom.Document()
        root = doc.createElement("filters")
        doc.appendChild(root)
        barrages = self.param_page()
        text = ""
        for barrage in barrages:
            text = text + barrage
        keywords_textrank = jieba.analyse.textrank(text)
        for word in keywords_textrank:
            nodeItem = doc.createElement("item")
            nodeItem.setAttribute("enabled", "false")
            nodeItem.appendChild(doc.createTextNode("t=" + word))
            root.appendChild(nodeItem)
        fp = open("block_" + bvid + ".xml", "w", encoding="utf-8")
        doc.writexml(fp, indent = "\t", addindent = "\t", newl = "\n", encoding = "utf-8")
        fp.close()
        print(keywords_textrank)
        self.post_word(keywords_textrank, bvid)

    # 传输至远端sql数据库用作日后统计
    def post_word(self, words, bvid):
        db = MySQLdb.connect("39.106.19.94", "danmu_user", "idislikejojo", "danmu_block")
        db.set_character_set("utf8")
        cursor = db.cursor()
        for word in words:
            cursor.execute("insert into blocker values(\"" + word + "\", \"" + bvid + "\")")
            db.commit()
        db.close()
        print("post to sql server finished")

    #获取视频cid
    def CIDget(self, bvid):
        url = "https://api.bilibili.com/x/player/pagelist?bvid=" + str(bvid) + "&jsonp=jsonp"
        response = requests.get(url)
        dirt = json.loads(response.text)
        cid = dirt["data"][0]["cid"]
        return cid

if __name__ ==  "__main__":
    #jojo1_and_jojo2 = Bilibili(CIDget("BV1MJ411S7LK"))
    #jojo3_1 = Bilibili(CIDget("BV1tJ411R7bY"))
    #jojo3_2 = Bilibili(CIDget("BV1yJ411R7je"))
    #jojo4 = Bilibili(CIDget("BV1sW411S7oL"))
    #jojo5 = Bilibili(CIDget("BV1nW41127fv"))

    #jojo1_and_jojo2.make_wordCloud("jojo1_and_jojo2")
    #jojo3_1.make_wordCloud("jojo3_1")
    #jojo3_2.make_wordCloud("jojo3_2")
    #jojo4.make_wordCloud("jojo4")
    #jojo5.make_wordCloud("jojo5")

    video = input("input BV (bid):")
    Bilibili(Bilibili.CIDget(Bilibili, video)).make_wordCloud(video)
