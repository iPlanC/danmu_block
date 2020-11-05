#
# Author: PlanC
# Date: 2020-11-05 10:57:56
# LastEditTime: 2020-11-05 11:30:19
# FilePath: \danmu_block\update.py

#%%

import MySQLdb
import xml.dom.minidom

def getlist(bvid):
    # 连接数据库
    db = MySQLdb.connect("39.106.19.94", "danmu_user", "idislikejojo", "danmu_block")
    db.set_character_set("utf8")
    cursor = db.cursor()

    # 获取数据
    try:
        cursor.execute("select * from blocker where source like \"" + bvid + "\"")
    except:
        print("can\"t fentch data")
        return
    keywords_textrank = cursor.fetchall()
    print(keywords_textrank)
    db.close()

    # 如果列表不为空则写入xml
    if len(keywords_textrank):
        doc = xml.dom.minidom.Document()
        root = doc.createElement("filters")
        doc.appendChild(root)

        for word in keywords_textrank:
            nodeItem = doc.createElement("item")
            nodeItem.setAttribute("enabled", "false")
            nodeItem.appendChild(doc.createTextNode("t=" + word[0]))
            root.appendChild(nodeItem)

        if bvid == "%":
            fp = open("block_all.xml", "w", encoding="utf-8")
        else:
            fp = open("block_" + bvid + ".xml", "w", encoding="utf-8")

        doc.writexml(fp, indent = "\t", addindent = "\t", newl = "\n", encoding = "utf-8")
        fp.close()
    else:
        print("unable to fetch any data from shared datbase, please try to fetch from original video")

if __name__ == "__main__":
    bvid = input("input the bvid to fetch from database, input % for all:")
    getlist(bvid)
