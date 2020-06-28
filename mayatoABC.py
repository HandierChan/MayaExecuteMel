# python3.7
import os
from tkinter import *
from tkinter.filedialog import askdirectory,askopenfilenames

def exportAllABC():
    '''
    用mel写的maya export ABC，通过python发到cmd执行
    '''
    # 获取GUI界面参数
    mayaEXE = mayaInstPath.get()+'/bin/mayabatch.exe'
    mayaEXEPath = correctWinPath(mayaEXE)

    abcPath = abcPathEntry.get()
    abcAbsPath = correctWinPath(abcPath)

    # 得到所有maya文件
    mayaFilesJudge = mayaFilesEntry.get().split(' ')
    mayaFiles=[]
    for i in mayaFilesJudge:
        # file
        if os.path.isfile(i):
            file = filterFileExt(i, ['.ma','.mb'], 0)
            mayaFiles.append(file)
        # directory
        else:
            files = filterFileExt(i, ['.ma','.mb'], 1)
            for j in files:
                mayaFiles.append(j)
    # 修正每个maya文件路径格式
    mayaFiles = [correctWinPath(i) for i in mayaFiles]

    # 循环每个maya文件发到cmd执行
    for i in mayaFiles:
        mayaName=os.path.splitext(i)[0].split('/')[-1]
        fileExt = os.path.splitext(i)[1]
        mayaExec = mayaEXEPath+' -file '+os.path.dirname(i)+'/'+'"'+mayaName+fileExt+'"'
        mel = 'int $startFrame=`playbackOptions -q -ast`;\
            int $endFrame=`playbackOptions -q -aet`;\
            string $commandMel=\\"-frameRange \\"+$startFrame+\\" \\"+$endFrame+\\" -file '+abcAbsPath+'/'+'"'+mayaName+'.abc'+'"'+' -uvWrite -worldSpace -writeVisibility -dataFormat ogawa\\";\
            AbcExport -j $commandMel;'
        cmd = mayaExec+' -command '+'"'+mel+'"'
        os.system(cmd)
        #print(mayaExec)

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

def filterFileExt(path, fileExt, isdir=1):
    '''
    path 可以是文件或文件夹，是文件夹就过滤 path 里对应格式的文件，是文件就判断 path 是否对应格式
    '''
    if isdir:
        fileLists = [os.path.abspath(path)+'/'+i for i in os.listdir(path) if os.path.isfile(path+'/'+i)]
        files = [i for i in fileLists if os.path.splitext(i)[1] in fileExt]
        return files
    elif os.path.splitext(path)[1] in fileExt:
        return path

def about():
    tk = Tk()
    tk.title('关于')
    tkWinWidth = 330
    tkWinHeigth = 100
    screenWidth = tk.winfo_screenwidth()
    screenHeight = tk.winfo_screenheight()
    tkWinXPos = (screenWidth - tkWinWidth) / 2
    tkWinYPos = (screenHeight - tkWinHeigth) / 2
    tk.geometry( "%dx%d+%d+%d" % (tkWinWidth,tkWinHeigth,tkWinXPos,tkWinYPos))
    Label(tk,text='制作：天雷动漫').grid(row=0)
    Label(tk,text='测试环境：python3.7 maya2018').grid(row=1)
    Label(tk,text='源码：https://github.com/HandierChan/mayatoABC').grid(row=2)


# 窗口
tk = Tk()
tk.title('MayatoABC')
#tk.iconbitmap('C:/aa.ico')
tk.resizable(0,0)
tkWinWidth = 740
tkWinHeigth = 150
screenWidth = tk.winfo_screenwidth()
screenHeight = tk.winfo_screenheight()
tkWinXPos = (screenWidth - tkWinWidth) / 2
tkWinYPos = (screenHeight - tkWinHeigth) / 2
tk.geometry( "%dx%d+%d+%d" % (tkWinWidth,tkWinHeigth,tkWinXPos,tkWinYPos))


# 初始变量
VarMayaInstPath = StringVar(tk, value=r'C:\Program Files\Autodesk\Maya2018')
VarmayaFiles = StringVar(tk)
VarabcPath = StringVar(tk)

def selectMayaInstPath():
    select_path = askdirectory()
    VarMayaInstPath.set(select_path)
def selectMayaFiles():
    select_path = askopenfilenames()
    VarmayaFiles.set(select_path)
def selectABCPath():
    select_path = askdirectory()
    VarabcPath.set(select_path)


# 界面元素
mayaInstPathLabel = Label(tk, text='Maya Install Path')
mayaInstPath = Entry(tk, textvariable=VarMayaInstPath)
mayaInstPathButton = Button(tk, text='Select', command=selectMayaInstPath)

mayaFileLabel = Label(tk, text='Maya Files or Path')
mayaFilesEntry = Entry(tk, textvariable=VarmayaFiles)
mayaFilesButton = Button(tk, text='Select', command=selectMayaFiles)

abcPathLabel = Label(tk, text='ABC Path')
abcPathEntry = Entry(tk, textvariable=VarabcPath)
abcPathButton = Button(tk, text='Select', command=selectABCPath)

noticeLabel = Label(tk, text='( Maya 和 ABC 路径目前不支持中文和空格)',fg='green')

convertButton = Button(tk, text='Convert', command = exportAllABC)
aboutLabel = Button(tk,text='关于',command=about)


# 界面布局
mayaInstPathLabel.grid(row=0, column=0, sticky='e',ipadx=10)
mayaInstPath.grid(row=0, column=1, sticky='w',ipadx=100)
#mayaInstPathButton.grid(row=0, column=2, sticky='w')

mayaFileLabel.grid(row=1, column=0, sticky='e',ipadx=10)
mayaFilesEntry.grid(row=1, column=1, sticky='w',ipadx=200)
mayaFilesButton.grid(row=1, column=2, sticky='w')

abcPathLabel.grid(row=2, column=0, sticky='e',ipadx=10)
abcPathEntry.grid(row=2, column=1, sticky='w',ipadx=200)
abcPathButton.grid(row=2, column=2, sticky='w')

noticeLabel.grid(row=3, column=1, sticky='w')

convertButton.grid(row=4, column=1, sticky='w', ipadx=20)
aboutLabel.grid(row=4, column=2, sticky='e')


tk.mainloop()
