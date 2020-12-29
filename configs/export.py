import datetime
import os


def write_to_log(filename, defname, result):
    dirdate = datetime.datetime.now().strftime("%Y-%m-%d")
    dirpath = os.path.join('log', dirdate)
    os.makedirs(dirpath, exist_ok=True)
    filepath = os.path.join(dirpath, filename+'.log')
    tofile = open(filepath, mode='a+', encoding='utf-8')
    content = str(datetime.datetime.now()) + ',' + defname + ',' + result
    print(content, file=tofile)
    print(content)
