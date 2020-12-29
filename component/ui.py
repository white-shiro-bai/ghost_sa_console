# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys
from prettytable import PrettyTable
sys.path.append("./")
sys.setrecursionlimit(10000000)

def ui(data):
    while True:
        print("\n<------------------------------------------------------------------------------------------------>")
        if 'desc' in data:
            print(data['desc'])
        if data["type"] == "option":
            if 'limit_func' in data and data['limit_func'] is True:
                #限制使用返回等功能
                display_keys = []
            else:    
                display_keys = ['~back','~refresh','~home','~exit']
            key_map = {"~back":"~back","~home":"~home","~refresh":"~refresh"} #
            if len(data["data"]) != 0:
                tb = PrettyTable(field_names=data["data"][0].keys())
                tb.padding_width = 1
                for item in data["data"]:
                    display_keys.append(str(item[data["display_key"]]))
                    row = []
                    for content in item.keys():
                        row.append(str(item[content]))
                    tb.add_row(row)
                    key_map[str(item[data["display_key"]])] = str(item[data["func_key"]])
                print(tb)
            else:
                print('无可用数据')    
            print('可供输入的'+data["display_key"]+"有：",display_keys)
            key_in = input("请输入选择的 "+data["display_key"]+" 并按回车键确认：")
            if key_in == "~back":
                return '~back','~menu'
            elif key_in == "~refresh":
                return '~refresh','~menu'
            elif key_in == "~exit":
                print("程序结束")
                exit()
            elif key_in == "~home":
                return '~home','~menu'
            elif key_in =="" and 'limit_func' in data and data['limit_func'] is True:
                continue
            elif key_in =="":
                return '~refresh','~menu'
            elif key_in not in display_keys and ',' not in key_in:
                print("\n<------------------------------------------------------------------------------------------------>\n 你输入的",key_in,"不是一个有效的输入，好好看选项，不然会报错的！")
                continue
            if ',' in key_in:
                key_out = []
                for key in key_in.split(','):
                    key_out.append(key_map[key])
                print("你输入的"+data["display_key"]+"是:",key_in,"执行的是：",','.join(key_out))
                return ','.join(key_out),key_in
            elif key_in[0] =='~':
                print("你输入的"+data["display_key"]+"是:",key_in,"执行的是：",key_in)
                return key_in,key_in
            else:
                print("你输入的"+data["display_key"]+"是:",key_in,"执行的是：",key_map[key_in])
                return key_map[key_in],key_in
        elif data["type"] == "keyword":
            key_in = input("请输入 "+data["display_key"]+" 并按回车键确认：")
            if key_in == "~exit":
                print("程序结束")
                exit()
            elif data["allow_none"] is False and key_in == '':
                print("\n<------------------------------------------------------------------------------------------------>\n "+data["display_key"] +" 选项不可以输入空字符，会报错的！")
                continue
            print("你输入的"+data["display_key"]+"是:",key_in,"执行的是：",key_in)
            if key_in != '' and key_in[0] == '~':
                return key_in,'~menu'
            return key_in,key_in
        elif data["type"] == "show":
            if len(data["data"]) != 0:
                tb = PrettyTable(field_names=data["data"][0].keys())
                tb.padding_width = 1
                for item in data["data"]:
                    row = []
                    for content in item.keys():
                        row.append(str(item[content]))
                    tb.add_row(row)
                print(tb)
                return None,None
            else:
                print('无可用数据')
                return None,None

if __name__ == "__main__":
    print('这是一个选项的示例，输出的是',ui(data={"type":"option","display_key":"key_name","func_key":"a","data":[{"key_name":1,"a":"aa","b":"bb","c":"cc"},{"key_name":2,"a":"dd","b":"ee","c":"ff"}]}))
    # print('这是一个填空的示例，输出的是',ui(data={"type":"keyword","display_key":"key_name","allow_none":False}))