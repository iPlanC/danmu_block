import os
import json
import requests
import time
import xml.dom.minidom
from lxml import etree

class Bilibili():
    """docstring for Bilibili"""
    def __init__(self, oid):
        self.headers = {
        'Host': 'comment.bilibili.com',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age = 0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36',
        'Accept': 'text/html, application/xhtml + xml, application/xml;q = 0.9, image/webp, image/apng, */*;q = 0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN, zh;q = 0.9',
        'Cookie': 'finger = edc6ecda; LIVE_BUVID = AUTO1415378023816310; stardustvideo = 1; CURRENT_FNVAL = 8; buvid3 = 0D8F3D74-987D-442D-99CF-42BC9A967709149017infoc; rpdid = olwimklsiidoskmqwipww; fts = 1537803390'
        }
        self.url = 'http://comment.bilibili.com/' + str(oid) + '.xml'
        self.barrage_reault = self.get_page()

    # 获取信息
    def get_page(self):
        try:
            # 延时操作，防止太快爬取
            time.sleep(0.5)
            response = requests.get(self.url, headers = self.headers)
        except Exception as e:
            print('获取xml内容失败, %s' % e)
            return False
        else:
            if response.status_code == 200:
                # 下载xml文件
                with open('bilibili.xml', 'wb') as f:
                    f.write(response.content)
                return True
            else:
                return False

    # 解析网页
    def param_page(self):
        time.sleep(1)
        if  self.barrage_reault:
            # 文件路径，html解析器
            html = etree.parse('bilibili.xml', etree.HTMLParser())
            # xpath解析，获取当前所有的d标签下的所有文本内容
            results = html.xpath('//d//text()')
            return results

    # 弹幕去重
    def remove_double_barrage(self):
        '''
        double_arrage:所有重复弹幕的集合
        results:去重后的弹幕
        barrage:每种弹幕内容都存储一遍
        '''
        double_barrage = []
        results = []
        barrage = set()
        for result in self.param_page():
            if result not in results:
                results.append(result)
            else:
                double_barrage.append(result)
                barrage.add(result)
        return double_barrage, results, barrage

    # 弹幕重复计算和词云的制作
    def make_wordCloud(self, filename):
        doc = xml.dom.minidom.Document()
        root = doc.createElement('filters')
        doc.appendChild(root)
        double_barrages, results, barrages = self.remove_double_barrage()
        # 重词计数
        f = open('barrages_' + filename + '.txt', 'w', encoding='utf-8')
        for barrage in barrages:
            amount = double_barrages.count(barrage)
            if (amount + 1 >= 5):
                f.write(barrage + ':' + str(amount + 1) + '\n')
                nodeItem = doc.createElement('item')
                nodeItem.setAttribute('enabled', 'true')
                nodeItem.appendChild(doc.createTextNode('t=' + barrage))
                root.appendChild(nodeItem)

        fp = open('block_' + filename + '.xml', 'w', encoding='utf-8')
        doc.writexml(fp, indent = '\t', addindent = '\t', newl = '\n', encoding = "utf-8")
        f.close()
        fp.close()

def CIDget(bvid):#获取视频cid
    url = "https://api.bilibili.com/x/player/pagelist?bvid=" + str(bvid) + "&jsonp=jsonp"
    response = requests.get(url)
    dirt = json.loads(response.text)
    cid = dirt['data'][0]['cid']
    return cid

if __name__ ==  '__main__':
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
    Bilibili(CIDget(video)).make_wordCloud(video)
