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
    '''
    过滤目录是否有对应格式的文件
    '''
    fileLists = [i for i in os.listdir(mayaAbsPath) if os.path.isfile(mayaAbsPath+'/'+i)]
    Files = [i for i in fileLists if os.path.splitext(i)[1] in fileExt]
    return Files

def about():
    tk = Tk()
    tk.title('关于')
    tkWinWidth = 300
    tkWinHeigth = 80
    screenWidth = tk.winfo_screenwidth()
    screenHeight = tk.winfo_screenheight()
    tkWinXPos = (screenWidth - tkWinWidth) / 2
    tkWinYPos = (screenHeight - tkWinHeigth) / 2
    tk.geometry( "%dx%d+%d+%d" % (tkWinWidth,tkWinHeigth,tkWinXPos,tkWinYPos))
    Label(tk,text='制作：天雷动漫').grid(row=0,column=0,sticky='w')
    Label(tk,text='测试环境：python3.7 maya2018').grid(row=0,column=1,sticky='w')
    Label(tk,text='源码：https://github.com/HandierChan/mayatoABC').grid(row=2,sticky='w',columnspan=2)

# tkinter窗口
tk = Tk()
tk.title('mayaExportABC')
#tk.iconbitmap('C:/aa.ico')
tk.resizable(0,0)
tkWinWidth = 700
tkWinHeigth = 150
screenWidth = tk.winfo_screenwidth()
screenHeight = tk.winfo_screenheight()
tkWinXPos = (screenWidth - tkWinWidth) / 2
tkWinYPos = (screenHeight - tkWinHeigth) / 2
tk.geometry( "%dx%d+%d+%d" % (tkWinWidth,tkWinHeigth,tkWinXPos,tkWinYPos))

# 初始变量
mayaVarInstPath = StringVar(tk, value=r'C:\Program Files\Autodesk\Maya2018')
mayaVarPath = StringVar(tk)
abcVarPath = StringVar(tk)

# GUI界面元素
mayaInstPathLabel = Label(tk, text='Maya Install Path')
mayaInstPath = Entry(tk, textvariable=mayaVarInstPath)
mayaFileLabel = Label(tk, text='Maya File or Path')
mayaPathEntry = Entry(tk, textvariable=mayaVarPath)
abcPathLabel = Label(tk, text='ABC Path')
abcPathEntry = Entry(tk, textvariable=abcVarPath)
noticeLabel = Label(tk, text='( Maya 和 ABC 路径目前不支持中文和空格)',fg='green')
convertButton = Button(tk, text='Convert', command = exportAllABC)
aboutLabel = Button(tk,text='关于',command=about)

# GUI界面布局
mayaInstPathLabel.grid(row=0, sticky='e',ipadx=10)
mayaInstPath.grid(row=0, column=1, sticky='w',ipadx=80)
mayaFileLabel.grid(row=1, sticky='e',ipadx=10)
mayaPathEntry.grid(row=1, column=1, sticky='w',ipadx=200,columnspan=2)
abcPathLabel.grid(row=2, sticky='e',ipadx=10)
abcPathEntry.grid(row=2, column=1, sticky='w',ipadx=200,columnspan=2)
noticeLabel.grid(row=3, column=1, sticky='w')
convertButton.grid(row=4, column=1, sticky='w', ipadx=20)
aboutLabel.grid(row=4,column=2,sticky='e')

tk.mainloop()
