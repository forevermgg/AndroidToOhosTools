import os
from collections import OrderedDict
from pprint import pprint

import xmltodict
from prettyprinter import cpprint

supportTags = ["string", "color", "dimen", "style"]


def resourcesItemIsList(resources: OrderedDict):
    for key, vals in resources.items():
        print(f"-----> [{key}]-->")
        if not isinstance(vals, list):
            print("其它类型--- " + type(vals).__name__)
            resources[key] = list(resources.values())  # 转到list，方便统一处理


# 读xml文件并转成dict
def readXmlFile(path):
    print(f"\n=====> start: =====> {path} ")
    with open(path, 'r') as file:
        xml_str = file.read()
        return convertXml2Dict(xml_str)


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
print(os.getcwd())
# 获取src下所有文件
__src__files = os.listdir(os.getcwd() + "/src/")
# 打印文件集合
print(__src__files)

resource = readXmlFile(os.getcwd() + "/src/" + "strings.xml")
pprint(resource)
cpprint(resource)
