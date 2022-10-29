import os
from functools import reduce

# -*- coding:utf-8 -*-
import requests


def translate(content):
    data = {
        'doctype': 'json',
        'type': 'AUTO',
        'i': content
    }
    url = "http://fanyi.youdao.com/translate"
    r = requests.get(url, params=data)
    result = r.json()
    print(result['translateResult'])
    return_result = ''
    for key in range(len(result['translateResult'])):
        print(result['translateResult'][key])
        for key2 in range(len(result['translateResult'][key])):
            test = result['translateResult'][key][key2]['tgt']
            print(test)
            test = test.replace(" ", "_")
            test = test.replace("-", "_")
            test = test.replace(",", "_")
            test = test.replace(".", "")
            test = test.replace("__", "_")
            test = reduce(lambda x, y: x + '_{}'.format(y.lower()) if y.isupper() else x + y,
                          test.replace(test[0], test[0].lower()))
            print(test)
            return_result = test
            break
    return return_result


# 获得当前目录
print(os.getcwd())
# 获取src下所有文件
__src__files = os.listdir(os.getcwd() + "/translate/")
# 打印文件集合
print(__src__files)

file_read = open(os.getcwd() + "/translate/" + "src.log", "r", encoding="utf-8")
# 将文件内容保存到内存
lines = file_read.readlines()
file_write = open(os.getcwd() + "/translate/" + "translate.log", "w", encoding="utf-8")
for line in lines:
    file_write.write(translate(line) + "\r\n")
file_write.close()
file_read.close()

