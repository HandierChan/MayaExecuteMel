import os

def configDictToFile(pathFileNameExt,_dict):
    # _dict 不能有嵌套 !!! need to rewrite
    txt=''
    for k,v in _dict.items():
        item=f'{k}={v}'
        txt+=item+'\n'
    with open(pathFileNameExt,'w',encoding='utf-8') as file:
        file.write(txt.strip())

def configFileToDict(pathFileNameExt):
    if os.path.exists(pathFileNameExt):
        with open(pathFileNameExt,'r',encoding='utf-8') as file:
            txt=file.read()
        _dict={k:v for i in txt.split('\n') for k,v in (i.split('='),)}
        return _dict

def createAppDataPath(softwareName='',dataFolder=''):
    # win10 %appdata% 创建文件夹，放用户数据
    appdataPath=os.getenv('appdata')
    pathName=os.path.normpath(f'{appdataPath}/{softwareName}/{dataFolder}')
    if not os.path.exists(pathName):
        try:os.makedirs(pathName)
        except:pass
    else:return pathName

if __name__=='__main__':
    a='aaa'
    b=222
    c='ccc'
    configDict={'a':a,'b':b,'c':c}
    configFileNameExt = 'history.txt'
    configPathFileNameExt = f'{os.getcwd()}/{configFileNameExt}'

    configDictToFile(configPathFileNameExt,configDict)
    d=configFileToDict(configPathFileNameExt)
    print(d.get('b'))
