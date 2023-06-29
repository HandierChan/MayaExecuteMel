'''
关闭软件时保存配置文件到%appdata%，打开软件自动读取上一次配置信息
'''

import os
import ast

def configDictToFile(pathFileNameExt,_dict):
    '''
    给文件名+路径和字典，写入到该文件
    _dict(字典)不能有嵌套，(这里代码需要优化???????)
    '''
    txt=''
    for k,v in _dict.items():
        if type(v)==str and '\n' in str(v):  #如果字符串有多行，转成列表
            v=v.strip().split('\n')
        item=f'{k}={v}'
        txt+=item+'\n'
    with open(pathFileNameExt,'w',encoding='utf-8') as file:
        file.write(txt.strip())

def configFileToDict(pathFileNameExt):
    '''
    给文件名，读取里面字典，查找字典用"键.get()"
    '''
    if os.path.exists(pathFileNameExt):
        with open(pathFileNameExt,'r',encoding='utf-8') as file:
            txt=file.read()
        # _dict={k:v for i in txt.split('\n') for k,v in (i.split('='),)}
        _dict={}
        for i in txt.split('\n'):
            for k,v in (i.split('=',1),):
                if v.startswith('['): #判断包含符号'[]'，导出历史文件已经列表转字符，是列表就拆成多行字符
                    v=ast.literal_eval(v)
                    v='\n'.join(v)
                _dict.update({k:v})
        return _dict

def createAppDataPath(softwareName='',dataFolder=''):
    '''
    创建文件夹在%appdata%，放用户数据
    '''
    appdataPath=os.getenv('appdata')
    pathName=os.path.normpath(f'{appdataPath}/{softwareName}/{dataFolder}')
    if not os.path.exists(pathName):
        try:os.makedirs(pathName)
        except:pass
    else:return pathName

if __name__=='__main__':
    a='aaa'
    b=222
    c='''a=aaa
b=222
c=['#多行 saf', '    aadf']
'''
    configDict={'a':a,'b':b,'c':c}
    configFileNameExt = 'history.txt'
    configPathFileNameExt = f'{os.getcwd()}/{configFileNameExt}'

    configDictToFile(configPathFileNameExt,configDict)
    # d=configFileToDict(configPathFileNameExt)
    # print(d.get('c'))
