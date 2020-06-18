# python3.7
import os
from tkinter import *


def exportAllABC():
    '''
    用mel写的maya export ABC，通过python发到cmd执行
    '''

    # 获取GUI界面参数
    mayaEXE = mayaInstPath.get()+'/bin/mayabatch.exe'
    mayaAbsEXE = correctWinPath(mayaEXE)

    abcPath = abcPathEntry.get()
    abcAbsPath = correctWinPath(abcPath)

    # mayaPath是目录还是maya文件
    mayaPathJudge = mayaPathEntry.get()
    if os.path.isfile(mayaPathJudge):
        mayaPath = os.path.dirname(mayaPathJudge)
        mayaAbsPath = correctWinPath(mayaPath)
        mayaFiles = [os.path.basename(mayaPathJudge)]
    else:
        mayaAbsPath = correctWinPath(mayaPathJudge)
        mayaFiles = filterFileExt(mayaAbsPath, ['.ma','.mb'])


    # 循环每个maya文件发到cmd执行
    for i in mayaFiles:
        mayaName = os.path.splitext(i)[0]
        fileExt = os.path.splitext(i)[1]
        mayaExec = mayaAbsEXE+' -file '+mayaAbsPath+'/'+'"'+mayaName+fileExt+'"'
        mel = 'int $startFrame=`playbackOptions -q -ast`;\
            int $endFrame=`playbackOptions -q -aet`;\
            string $commandMel=\\"-frameRange \\"+$startFrame+\\" \\"+$endFrame+\\" -file '+abcAbsPath+'/'+'"'+mayaName+'.abc'+'"'+' -uvWrite -worldSpace -writeVisibility -dataFormat ogawa\\";\
            AbcExport -j $commandMel;'
        cmd = mayaExec+' -command '+'"'+mel+'"'
        os.system(cmd)
        #print(mayaFiles)

def correctWinPath(path):
    '''
    纠正路径错误：1反斜杠改成正斜杠；2带空格的目录加上双引号
    '''
    absPath = os.path.abspath(path)
    splitPath = absPath.split('\\')
    for i in range( len(splitPath)):
        if ' ' in splitPath[i]:
            splitPath[i] = '"' + splitPath[i] + '"'
    windowsPath = '/'.join(splitPath)
    return windowsPath

def filterFileExt(mayaAbsPath, fileExt):
    # 过滤目录是否有对应格式的文件
    fileLists = [i for i in os.listdir(mayaAbsPath) if os.path.isfile(mayaAbsPath+'/'+i)]
    Files = [i for i in fileLists if os.path.splitext(i)[1] in fileExt]
    return Files


tk = Tk()
tk.title('mayaExportABC')
tk.iconbitmap('C:/aa.ico')
tk.geometry('650x150+500+500')

# 初始tkinter变量
mayaVarInstPath = StringVar(tk, value=r'C:\Program Files\Autodesk\Maya2018')
mayaVarPath = StringVar(tk)
abcVarPath = StringVar(tk)

# GUI界面元素
mayaInstPathLabel = Label(tk, text='Maya Install Path', fg='gray')
mayaInstPath = Entry(tk, textvariable=mayaVarInstPath, fg='gray')
mayaFileLabel = Label(tk, text='Maya File or Path')
mayaPathEntry = Entry(tk, textvariable=mayaVarPath)
abcPathLabel = Label(tk, text='ABC Path')
abcPathEntry = Entry(tk, textvariable=abcVarPath)
noticeLabel = Label(tk, text='( Maya 和 ABC 路径目前不支持空格)',fg='green')
convert = Button(tk, text='Convert', command = exportAllABC)
copyright = Button(tk, text='天雷动漫 github.com/HandierChan/mayatoABC')

# GUI界面布局
mayaInstPathLabel.grid(row=0, sticky='e')
mayaInstPath.grid(row=0, column=1, sticky='we',ipadx=60)
mayaFileLabel.grid(row=1, sticky='e')
mayaPathEntry.grid(row=1, column=1, sticky='we',columnspan=2,ipadx=60)
abcPathLabel.grid(row=2, sticky='e')
abcPathEntry.grid(row=2, column=1, sticky='we',columnspan=2,ipadx=60)
noticeLabel.grid(row=3, column=1, sticky='w')
convert.grid(row=4, column=1,sticky='w')
copyright.grid(row=4, column=2,sticky='e')

tk.mainloop()
