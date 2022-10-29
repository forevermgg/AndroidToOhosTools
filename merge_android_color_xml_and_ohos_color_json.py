import json
import os
from collections import OrderedDict
from pprint import pprint

import xmltodict

supportTags = ["string", "color", "dimen", "style"]


def resourcesItemIsList(resources: OrderedDict):
    for key, vals in resources.items():
        pprint(f"-----> [{key}]-->")
        if not isinstance(vals, list):
            pprint("其它类型--- " + type(vals).__name__)
            resources[key] = list(resources.values())  # 转到list，方便统一处理


# 读xml文件并转成dict
def readXmlFile(path):
    pprint(f"\n=====> start: =====> {path} ")
    with open(path, 'r') as file:
        xml_string = file.read()
        return convertXml2Dict(xml_string)


def readJson(path):
    pprint(f"\n=====> readJson start: =====> {path} ")
    # 设置以utf-8解码模式读取文件，encoding参数必须设置，否则默认以gbk模式读取文件，当文件中包含中文时，会报错
    f = open(path, encoding="utf-8")
    json_string = json.load(f)
    # pprint(f"\n=====> jsonString: =====> {json_string} ")
    pprint(f"\n=====> readJson end: =====> {path} ")
    return json_string


def get_all_dict(data):
    if isinstance(data, dict):
        for x in range(len(data)):
            temp_key = list(data.keys())[x]
            temp_value = data[temp_key]
            print('KEY --> {}\nVALUE --> {}'.format(temp_key, temp_value))
            print('\t')
            get_all_dict(temp_value)  # 迭代输出结果


# dict转成json
def convertXml2Dict(xmlStr: str):
    try:
        obj = xmltodict.parse(xmlStr, attr_prefix='', cdata_key='value')
        if 'resources' in obj:
            resources: OrderedDict = obj['resources']
            # 过滤tag
            for key in resources.copy().keys():
                if key not in supportTags:
                    resources.pop(key)
            # resources下只有一行元素，需要将此item放进list
            resourcesItemIsList(resources)

            # 处理dimen:单位转换
            if 'dimen' in resources:
                vals = resources.get('dimen')
                for item in vals:
                    # print(item)
                    # print(type(item))#item 是个 OrderedDict
                    v = item['value']  # 通过key取dict的value
                    if v.endswith("dp"):
                        item['value'] = v[:-2] + "vp"  # 修改单位 dp ---> vp
                resources['float'] = resources.pop('dimen')
            # 处理style
            if 'style' in resources:
                styles = resources.get('style')
                for style in styles:
                    # print(style)
                    # print(type(style))#style 是个 OrderedDict
                    if 'item' in style:
                        if not isinstance(style['item'], list):
                            print(f"----item 只有一行: ---> {style['item']}")
                            style['value'] = [style.pop('item')]  # item 应该是list
                        else:
                            style['value'] = style.pop('item')
                        vals = style.get('value')
                        for item in vals:
                            # print('----')
                            # print(item)
                            # print(type(item))#item 是个 OrderedDict
                            v: str = item['value']  # 通过key取dict的value
                            if v.startswith("@color/"):
                                # print("---"+v)
                                item['value'] = "$color:" + v[7:]
                resources['pattern'] = resources.pop('style')

            return resources
    except Exception:
        return None
    return None


# 获得当前目录
pprint(os.getcwd())
# 获取src下所有文件
__src__files = os.listdir(os.getcwd() + "/src/")
# 打印文件集合
pprint(__src__files)

android_colors = readXmlFile(os.getcwd() + "/src/" + "colors.xml")
androidDict = {}
for k, v in android_colors.items():
    # print(k, v)
    for list_item in v:
        # print(list_item)
        androidDict[list_item['name']] = list_item['value']
# cpprint(androidDict)
# pprint(android_strings)
# cpprint(android_strings)
pprint('==========================================================')
string_json = readJson(os.getcwd() + "/src/" + "color.json")
ohosDict = {}
for k, v in string_json.items():
    # print(k, v)
    for list_item in v:
        # print(list_item)
        ohosDict[list_item['name']] = list_item['value']
pprint('==========================================================')


# cpprint(ohosDict)
# get_all_dict(string_json['string'])


def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res


# print(androidDict)
# print(ohosDict)
mergeDict = Merge(androidDict, ohosDict)
# print(mergeDict)

resultList = []
for k, v in mergeDict.items():
    # print(k, v)
    resultList.append({'name': k, 'value': v})

resultList = sorted(resultList, key=lambda x: x['name'])
# print(resultList)
resultDict = {'color': resultList}
print(string_json)
print(resultDict)

with open(os.getcwd() + "/des/" + "color.json", 'w', encoding="utf-8") as f:
    json.dump(resultDict, f, indent=2, ensure_ascii=False)  # 会在目录下生成一个1.json的文件，文件内容是dict数据转成的json数据
