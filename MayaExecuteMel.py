# win10 python3.9

# python module
import os,subprocess,re
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askdirectory,askopenfilenames
from tkinter.scrolledtext import ScrolledText

# local module
import deadlineSubmission
import configFile

# extra module
import windnd

def executeCmd(execute=False,deadline=False):
    deadlineInstallPath=deadlineInstallPathEntry.get()
    mayaInstallPath=mayaInstallPathEntry.get()+'/bin'
    _mayaInstallPath= correctWinPath(mayaInstallPathEntry.get()+'/bin')
    outputPath = correctWinPath(outputPathEntry.get())
    melCommand = melCommandScrolledText.get(1.0,END).strip().replace('\n','').replace('\r','').replace('"',r'\"')
    # if has {###.abc}, !!!! need to rewrite
    try:fileExt=melCommand.split("{###.")[1].split("}",1)[0]
    except:fileExt=''
    ### 过滤所有maya文件
    mayaPathNameExtFilterLists=mayaFilesEntry.get().split(';')
    mayaPathNameExtLists=[]
    for i in mayaPathNameExtFilterLists:
        files = filterFileExt(i.strip(), ('.ma','.mb'))
        if files:
            [mayaPathNameExtLists.append(j) for j in files]
    # 修正每个maya文件路径格式
    mayaPathNameExtLists = [correctWinPath(i) for i in mayaPathNameExtLists]
    # 循环每个maya文件
    for i in mayaPathNameExtLists:
        mayaName = os.path.splitext(i)[0].split('/')[-1].lstrip('"')
        # replace {###.abc} to outputName.ext
        melCommandCorrect = melCommand.replace('{###.'+fileExt+'}',f'{outputPath}/{mayaName}.{fileExt}')
        localExecuteCmd=f'''mayabatch.exe -file {i} -command "{melCommandCorrect}"'''
        submitDeadlineCmd=f'''{_mayaInstallPath}/mayabatch.exe -file {i} -command "{melCommandCorrect}"'''
        if execute:
            if deadline: deadlineSubmission.quickSubmit_CMD(deadlineInstallPath,outputPath,mayaName,submitDeadlineCmd)
            elif not deadline: subprocess.run(localExecuteCmd,cwd=mayaInstallPath,shell=True,encoding="utf-8",check=False)
        elif deadline: print(submitDeadlineCmd)
        elif not deadline: print(localExecuteCmd)

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

def filterFileExt(path=r'c:/a.txt', fileExt=['.txt','.mp4']):
    '''
    path是文件或文件夹，返回文件夹里一层(path)所有对应文件格式(fileExt)；是文件就判断文件名(path)是否对应fileExt
    Output: 文件全路径(list)
    '''
    if os.path.isdir(path):
        fileLists = [os.path.abspath(path)+'/'+i for i in os.listdir(path) if os.path.isfile(path+'/'+i)]
        files = [i for i in fileLists if os.path.splitext(i)[1] in fileExt]
        return files
    elif os.path.splitext(path)[1] in fileExt:
        file = []
        file.append(path)
        return file

def about():
    tk = Tk()
    tk.title('About')
    tkWinWidth = 350
    tkWinHeigth = 170
    screenWidth = tk.winfo_screenwidth()
    screenHeight = tk.winfo_screenheight()
    tkWinXPos = (screenWidth - tkWinWidth) / 2
    tkWinYPos = (screenHeight - tkWinHeigth) / 2
    tk.geometry( "%dx%d+%d+%d" % (tkWinWidth,tkWinHeigth,tkWinXPos,tkWinYPos))

    Label(tk,justify='left',text='说明：\n1. 此脚本导出文件的格式，比如导出abc是 {###.abc}\n所以mel里面不要有冲突关键符“ {###. ”\n2. 直接执行mel，记得最后加上“ file -s; ”').grid(row=0,sticky='w')
    Label(tk,text='').grid(row=1,sticky='w')
    Label(tk,text=r'制作：天雷动漫').grid(row=2,sticky='w')
    Label(tk,text=r'测试环境：win10 python3.9 maya2018').grid(row=3,sticky='w')
    Label(tk,text=r'源码：https://github.com/handierchan/MayaExecuteMel').grid(row=4,sticky='w')

def tkGUIPosition(tkinter,addWidth=10,addHight=10):
    tkinter.resizable(0,0)
    tkinter.update()
    tkGUIWidth = tkinter.winfo_width()
    tkGUIHeigth = tkinter.winfo_height()
    screenWidth = tkinter.winfo_screenwidth()
    screenHeight = tkinter.winfo_screenheight()
    tkinter.geometry("%dx%d+%d+%d"%(tkGUIWidth+addWidth,tkGUIHeigth+addHight,(screenWidth-tkGUIWidth)/2,(screenHeight-tkGUIHeigth)/2))

def createAppDataPath(softwareName='',dataFolder=''):
    # win10 %appdata% 创建文件夹，放用户数据
    appdataPath=os.getenv('appdata')
    pathName=os.path.normpath(f'{appdataPath}/{softwareName}/{dataFolder}')
    if not os.path.exists(pathName):
        try:os.makedirs(pathName)
        except:pass
    else:return pathName


if __name__=='__main__':
    softwareName='MayaExecuteMel'
    tk=Tk()
    tk.title(softwareName)

    mayaInstallPathVar=StringVar(tk,value=r'C:\Program Files\Autodesk\Maya2018')
    deadlineInstallPathVar=StringVar(tk,value=r'C:\Program Files\Thinkbox\Deadline10')
    mayaFilesVar=StringVar(tk)
    outputPathVar=StringVar(tk)

    ### mel Example
    exportABCAll=r'''int $playbackStartFrame=`playbackOptions -q -ast`;
int $playbackEndFrame=`playbackOptions -q -aet`;
int $outputStartFrame=`getAttr defaultRenderGlobals.startFrame`;
int $outputEndFrame=`getAttr defaultRenderGlobals.endFrame`;
int $abcStartFrame,$abcEndFrame;
if (`getAttr defaultRenderGlobals.animation`==1){
    $abcStartFrame=$outputStartFrame; $abcEndFrame=$outputEndFrame;}
else{
    $abcStartFrame=$playbackStartFrame; $abcEndFrame=$playbackEndFrame;}

string $frameRange="-frameRange "+$abcStartFrame+" "+$abcEndFrame;
string $melCommand=$frameRange+" -uvWrite -worldSpace -writeVisibility -dataFormat ogawa -file {###.abc}";
AbcExport -j $melCommand;'''

    def defaultParameters():
        mayaInstallPathVar.set(r'C:\Program Files\Autodesk\Maya2018')
        deadlineInstallPathVar.set(r'C:\Program Files\Thinkbox\Deadline10')
        mayaFilesVar.set('')
        outputPathVar.set('')
        melCommandScrolledText.delete(1.0,END)
        melCommandScrolledText.insert(1.0,exportABCAll)

    def selectMayaFiles(tkVar):
        selectPath=askopenfilenames(filetypes=[('Maya Files',('*.ma;*.mb'))])
        tkVar.set('; '.join(selectPath))
    def selectoutputPath(tkVar):
        selectPath=askdirectory()
        tkVar.set(selectPath)

    ### 界面
    Label(tk, text='Maya Install Path').grid(row=0, column=0, sticky='e',ipadx=10)
    mayaInstallPathEntry = Entry(tk, textvariable=mayaInstallPathVar)
    mayaInstallPathEntry.grid(row=0, column=1, sticky='w',ipadx=150)
    defaultButton=Button(tk, text='Default',width=8,command=lambda:defaultParameters())
    defaultButton.grid(row=0, column=2, sticky='w')
    Label(tk, text='Deadline Install Path').grid(row=1, column=0, sticky='e',ipadx=10)
    deadlineInstallPathEntry = Entry(tk, textvariable=deadlineInstallPathVar)
    deadlineInstallPathEntry.grid(row=1, column=1, sticky='w',ipadx=150)
    Label(tk, text='Maya Files/Path').grid(row=2, column=0, sticky='e',ipadx=10)
    mayaFilesEntry = Entry(tk, textvariable=mayaFilesVar)
    mayaFilesEntry.grid(row=2, column=1, sticky='w',ipadx=250)
    mayaFilesButton=Button(tk, text='Select', width=8,command=lambda:selectMayaFiles(mayaFilesVar))
    mayaFilesButton.grid(row=2, column=2, sticky='w')
    Label(tk, text='Output Path').grid(row=3, column=0, sticky='e',ipadx=10)
    outputPathEntry = Entry(tk, textvariable=outputPathVar)
    outputPathEntry.grid(row=3, column=1, sticky='w',ipadx=250)
    outputPathButton=Button(tk, text='Select', width=8,command=lambda:selectoutputPath(outputPathVar))
    outputPathButton.grid(row=3, column=2, sticky='w')
    Label(tk, text='Mel Command').grid(row=4, column=0, sticky='ne',ipadx=10)
    melCommandScrolledText = ScrolledText(tk,width='80',height='8',wrap='word')
    melCommandScrolledText.insert(1.0,exportABCAll)
    melCommandScrolledText.grid(row=4,column=1,sticky='we',columnspan=2)
    melCommandScrolledText.focus()
    Label(tk, text='( Maya 文件路径不支持中文和空格)',fg='SaddleBrown').grid(row=5, column=1, sticky='w')
    localConvertButton = Button(tk,text='Local Convert',fg='green',width=15,command=lambda:executeCmd(execute=1,deadline=0))
    localConvertButton.grid(row=6,column=1,sticky='w')
    submitToDeadlineButton=Button(tk,text='Submit to Deadline',fg='green',width=20,command=lambda:executeCmd(execute=1,deadline=1))
    submitToDeadlineButton.grid(row=6,column=1,sticky='w',padx=130)
    aboutButton=Button(tk,text='About',command=about)
    aboutButton.grid(row=6, column=2, sticky='e')

    ### Save/Load history config
    def getHistoryConfig():
        historyConfig={
            'MayaInstallPath':mayaInstallPathEntry.get(),
            'DeadlineInstallPath':deadlineInstallPathEntry.get(),
            # 'MayaFiles':mayaFilesVar.get(),
            'OutputPath':outputPathVar.get()
            }
        return historyConfig
    def quitWindow():
        try:configFile.configDictToFile(createAppDataPath(softwareName,'presets')+'/history.txt',getHistoryConfig())
        except:pass
        tk.quit()
        tk.destroy()
        exit()
    configFileNameExt=createAppDataPath(softwareName,'presets')+'/history.txt'
    try:configDict=configFile.configFileToDict(configFileNameExt)
    except:pass
    try:
        mayaInstallPathVar.set(configDict.get('MayaInstallPath'))
        deadlineInstallPathVar.set(configDict.get('DeadlineInstallPath'))
        outputPathVar.set(configDict.get('OutputPath'))
    except:pass

    ### Mouse Drag
    def mayaFilesEntry_MouseDrag(files):
        _files='; '.join((i for i in files))
        mayaFilesVar.set(_files)
    def melCommandScrolledText_MouseDrag(files):
        with open(files[0], "r", encoding='utf-8') as r:
            try:text=r.read()
            except:text=''
        melCommandScrolledText.delete(1.0,END)
        melCommandScrolledText.insert(1.0,text)
    windnd.hook_dropfiles(mayaFilesEntry,func=mayaFilesEntry_MouseDrag,force_unicode=1)
    windnd.hook_dropfiles(melCommandScrolledText,func=melCommandScrolledText_MouseDrag,force_unicode=1)

    # Button 颜色事件
    def SetBGColor(event):
        event.widget.config(bg='DarkSeaGreen')
    def ReturnBGColor(event):
        event.widget.config(bg='SystemButtonFace')
    for i in [defaultButton,mayaFilesButton,outputPathButton,localConvertButton,submitToDeadlineButton]:
        i.bind("<Enter>", SetBGColor)
        i.bind("<Leave>", ReturnBGColor)

    tkGUIPosition(tk,addWidth=30,addHight=10)
    tk.protocol("WM_DELETE_WINDOW",quitWindow)
    tk.mainloop()

