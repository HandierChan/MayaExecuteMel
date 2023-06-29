# win10 python3.10 maya2018

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



def generateCmdStruct():
    '''
    循环每个maya文件，生成mel转成cmd的代码列表
    返回3个列表[]，[0]是maya文件，[1]提交maya的cmd代码，[2]提交deadline的cmd代码
    '''
    mayaInstallPathCorrect= correctWinPath(mayaInstallPathEntry.get()+'/bin')
    outputPath = correctWinPath(outputPathEntry.get())
    melCommand = melCommandScrolledText.get(1.0,END).strip().replace('\n','').replace('\r','').replace('"',r'\"') #多行转单行

    # 系统cmd的"<>"表示命令输入输出，去异成"^<^>"，用正则对照列表一一对应替换
    mayaMelMatch=['<Scene>','<RenderLayer>','<Camera>','<RenderPassFileGroup>','<RenderPass>','<RenderPassType>','<Extension>','<Version>']
    mayaMelMatchToCmd=['^<Scene^>','^<RenderLayer^>','^<Camera^>','^<RenderPassFileGroup^>','^<RenderPass^>','^<RenderPassType^>','^<Extension^>','^<Version^>']
    for i in range(len(mayaMelMatch)):
        if re.search(re.escape(mayaMelMatch[i]),melCommand,re.I):
            melCommand = re.sub(re.escape(mayaMelMatch[i]),mayaMelMatchToCmd[i],melCommand,flags=re.I)

    # mel代码中含有{###.abc}（这里需要优化代码??????????）
    try:fileExt=melCommand.split("{###.")[1].split("}",1)[0]
    except:fileExt=''

    # 过滤所有maya文件
    mayaPathNameExtFilterLists=mayaFilesEntry.get().split(';')
    mayaPathNameExtLists=[]
    for i in mayaPathNameExtFilterLists:
        files = filterFileExt(i.strip(), ('.ma','.mb'))
        if files:
            [mayaPathNameExtLists.append(j) for j in files]

    # 修正每个maya文件路径格式
    mayaPathNameExtLists = [correctWinPath(i) for i in mayaPathNameExtLists]

    # 循环每个maya文件
    mayaFile=[]
    localExecuteCmdList=[]
    submitDeadlineCmdList=[]
    for i in mayaPathNameExtLists:
        mayaFile.append(i)
        mayaName = os.path.splitext(i)[0].split('/')[-1].lstrip('"')
        # replace {###.abc} to outputName.ext, use export ABC file
        melCommandCorrect = melCommand.replace('{###.'+fileExt+'}',f'{outputPath}/{mayaName}.{fileExt}')

        localExecuteCmd=f'''mayabatch.exe -file {i} -command "{melCommandCorrect}"'''
        localExecuteCmdList.append(localExecuteCmd)

        submitDeadlineCmd=f'''{mayaInstallPathCorrect}/mayabatch.exe -file {i} -command "{melCommandCorrect}"'''
        submitDeadlineCmdList.append(submitDeadlineCmd)
    return mayaFile,localExecuteCmdList,submitDeadlineCmdList,

def ExecuteLocalCmd(execute=False,message=False):
    '''
    本机执行代码，还是打印出来(用于测试)
    '''
    mayaInstallPath=mayaInstallPathEntry.get()+'/bin'
    if execute:
        for i in generateCmdStruct()[1]:
            subprocess.run(i,cwd=mayaInstallPath,shell=True,encoding="utf-8",check=False)
    else:
        for i in generateCmdStruct()[1]:
            print(i)
    if message:
        doneMessage(tk)

def ExecuteCmdToDeadline(execute=False):
    '''
    提交给deadline执行代码，还是打印出来(用于测试)
    '''
    deadlineInstallPath=deadlineInstallPathEntry.get()
    outputPath = correctWinPath(outputPathEntry.get())
    if execute:
        for i in range(len(generateCmdStruct()[0])):
            file=generateCmdStruct()[0][i]
            mayaName=os.path.splitext(os.path.basename(file))[0]
            deadlineSubmission.quickCmdSubmit(deadlineInstallPath,outputPath,mayaName,generateCmdStruct()[2][i])
    else:
        for i in range(len(generateCmdStruct()[0])):
            print(generateCmdStruct()[2][i])
    doneMessage(tk)

def ExecuteArnoldToDeadline(execute=False):
    '''
    提交给deadline执行代码，还是打印出来(用于测试)
    '''
    ExecuteLocalCmd(1,0) #maya执行mel并保存
    deadlineInstallPath=deadlineInstallPathEntry.get()
    if execute:
        for i in range(len(generateCmdStruct()[0])):
            file=generateCmdStruct()[0][i]
            deadlineSubmission.quickArnoldSubmit(deadlineInstallPath,mayaInstallPathEntry.get()+'/bin',generateCmdStruct()[0][i])
    else:
        for i in range(len(generateCmdStruct()[0])):
            file=generateCmdStruct()[0][i]
            print(generateCmdStruct()[2][i])
    doneMessage(tk)

def correctWinPath(path):
    '''
    纠正路径错误：1反斜杠"\"改成正斜杠"/"；2带空格的路径加上双引号
    '''
    absPath = os.path.abspath(path)
    splitPath = absPath.split('\\')
    for i in range( len(splitPath)):
        if ' ' in splitPath[i]:
            splitPath[i] = '"' + splitPath[i] + '"'
    windowsPath = '/'.join(splitPath)
    return windowsPath

def filterFileExt(path=r'c:/a.txt', fileFilterExt=['.txt','.mp4']):
    '''
    path是文件或文件夹，返回文件夹里一层(path)所有对应文件格式(fileFilterExt)；是文件就判断文件名(path)是否对应fileFilterExt
    Output: 文件全路径(list)
    '''
    if os.path.isdir(path):
        fileLists = [os.path.abspath(path)+'/'+i for i in os.listdir(path) if os.path.isfile(path+'/'+i)]
        files = [i for i in fileLists if os.path.splitext(i)[1] in fileFilterExt]
        return files
    elif os.path.splitext(path)[1] in fileFilterExt:
        file = []
        file.append(path)
        return file

def about(mainTk):
    top=Toplevel()
    mainWidth=mainTk.winfo_width()
    mainHight=mainTk.winfo_height()
    mainXPos=mainTk.winfo_x()
    mainYPos=mainTk.winfo_y()
    ToplevelWidth=350
    ToplevelHight=230
    ToplevelXPos=(mainWidth-ToplevelWidth)/2+mainXPos
    ToplevelYPos=(mainHight-ToplevelHight)/2+mainYPos
    top.geometry( "%dx%d+%d+%d" % (ToplevelWidth,ToplevelHight,ToplevelXPos,ToplevelYPos))
    Label(top,justify='left',text='说明：\n1. 此脚本导出文件的格式，比如导出abc是 {###.abc}\n所以mel里面不要有冲突关键符"{###."和"\\n"\n2. 直接执行mel，记得最后加上“ file -s; ”').grid(row=0,sticky='w')
    Label(top,justify='left',text='').grid(row=1,sticky='w')
    Label(top,justify='left',text=r'制作：天雷动漫').grid(row=2,sticky='w')
    Label(top,justify='left',text=r'测试环境：win10 python3.9 maya2018').grid(row=3,sticky='w')
    Label(top,justify='left',text='源码：\nhttps://github.com/handierchan/MayaExecuteMel\nhttps://gitee.com/handierchan/MayaExecuteMel').grid(row=4,sticky='w')
    Button(top,text='退出',command=lambda:top.destroy()).grid(row=5,sticky='w')

def doneMessage(mainTk):
    top=Toplevel()
    mainWidth=mainTk.winfo_width()
    mainHight=mainTk.winfo_height()
    mainXPos=mainTk.winfo_x()
    mainYPos=mainTk.winfo_y()
    ToplevelWidth=150
    ToplevelHight=100
    ToplevelXPos=(mainWidth-ToplevelWidth)/2+mainXPos
    ToplevelYPos=(mainHight-ToplevelHight)/2+mainYPos
    top.geometry( "%dx%d+%d+%d" % (ToplevelWidth,ToplevelHight,ToplevelXPos,ToplevelYPos))
    top.attributes('-topmost',True)
    Message(top,text='执行完成，查看是否成功').pack()
    Button(top,text='退出',command=lambda:top.destroy()).pack()

def errorMessage(mainTk):
    top=Toplevel()
    mainWidth=mainTk.winfo_width()
    mainHight=mainTk.winfo_height()
    mainXPos=mainTk.winfo_x()
    mainYPos=mainTk.winfo_y()
    ToplevelWidth=150
    ToplevelHight=100
    ToplevelXPos=(mainWidth-ToplevelWidth)/2+mainXPos
    ToplevelYPos=(mainHight-ToplevelHight)/2+mainYPos
    top.geometry( "%dx%d+%d+%d" % (ToplevelWidth,ToplevelHight,ToplevelXPos,ToplevelYPos))
    top.attributes('-topmost',True)
    Message(top,text='执行出错！！').pack()
    Button(top,text='退出',command=lambda:top.destroy()).pack()

def tkGUIPosition(tkinter,addWidth=10,addHight=10):
    tkinter.resizable(0,0)
    tkinter.update()
    tkGUIWidth = tkinter.winfo_width()
    tkGUIHeigth = tkinter.winfo_height()
    screenWidth = tkinter.winfo_screenwidth()
    screenHeight = tkinter.winfo_screenheight()
    tkinter.geometry("%dx%d+%d+%d"%(tkGUIWidth+addWidth,tkGUIHeigth+addHight,(screenWidth-tkGUIWidth)/2,(screenHeight-tkGUIHeigth)/2))

if __name__=='__main__':
    softwareName='MayaExecuteMel'
    tk=Tk()
    tk.title(softwareName)

    mayaInstallPathVar=StringVar(tk,value=r'C:/Program Files/Autodesk/Maya2018')
    deadlineInstallPathVar=StringVar(tk,value=r'C:/Program Files/Thinkbox/Deadline10')
    mayaFilesVar=StringVar(tk)
    outputPathVar=StringVar(tk)




    def defaultParameters():
        mayaInstallPathVar.set(r'C:/Program Files/Autodesk/Maya2018')
        deadlineInstallPathVar.set(r'C:/Program Files/Thinkbox/Deadline10')
        mayaFilesVar.set('')
        outputPathVar.set('')
        melCommandScrolledText.delete(1.0,END)

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
    melCommandScrolledText = ScrolledText(tk,width='80',height='15',wrap='word')
    # melCommandScrolledText.insert(1.0,'aaaaaa')
    melCommandScrolledText.grid(row=4,column=1,sticky='we',columnspan=2)
    melCommandScrolledText.focus()
    Label(tk, text='(1.Maya 文件路径不支持中文和空格；2.代码不支持中文和注释)',fg='SaddleBrown').grid(row=5, column=1, sticky='w')
    localConvertButton = Button(tk,text='Local Render',fg='green',width=15,command=lambda:ExecuteLocalCmd(1,1))
    localConvertButton.grid(row=6,column=1,sticky='w')
    cmdToDeadlineButton=Button(tk,text='CMD to Deadline',fg='green',width=20,command=lambda:ExecuteCmdToDeadline(1))
    cmdToDeadlineButton.grid(row=6,column=1,sticky='w',padx=130)
    arnoldToDeadlineButton=Button(tk,text='Arnold to Deadline',fg='green',width=20,command=lambda:ExecuteArnoldToDeadline(1))
    arnoldToDeadlineButton.grid(row=6,column=1,sticky='e',padx=130)
    aboutButton=Button(tk,text='About',command=lambda:about(tk))
    aboutButton.grid(row=6, column=2, sticky='e')

    ### Save/Load History Config
    def getHistoryConfig():
        historyConfig={
            'MayaInstallPath':mayaInstallPathEntry.get(),
            'DeadlineInstallPath':deadlineInstallPathEntry.get(),
            'MayaFiles':mayaFilesVar.get(),
            'OutputPath':outputPathVar.get(),
            'melCommand':melCommandScrolledText.get(1.0, END),
            }
        return historyConfig
    def quitWindow():
        try:configFile.configDictToFile(configFile.createAppDataPath(softwareName,'')+'/history.txt',getHistoryConfig())
        except:pass
        tk.quit()
        tk.destroy()
        exit()

    try:
        configDict=configFile.configFileToDict(configFile.createAppDataPath(softwareName,'')+'/history.txt')
        mayaInstallPathVar.set(configDict.get('MayaInstallPath'))
        deadlineInstallPathVar.set(configDict.get('DeadlineInstallPath'))
        mayaFilesVar.set(configDict.get('MayaFiles'))
        outputPathVar.set(configDict.get('OutputPath'))
        melCommandScrolledText.insert(1.0,configDict.get('melCommand'))
    except:pass

    ### 鼠标拖动复制字符
    def mayaInstallPathEntry_MouseDrag(files):
        if os.path.isdir(files[0]): mayaInstallPathVar.set(files[0])
    def deadlineInstallPathEntry_MouseDrag(files):
        if os.path.isdir(files[0]): deadlineInstallPathVar.set(files[0])
    def mayaFilesEntry_MouseDrag(files):
        filesFilters=[i for i in files if os.path.isfile(i)]
        filesList='; '.join((i for i in filesFilters))
        mayaFilesVar.set(filesList)
    def outputPathEntry_MouseDrag(files):
        if os.path.isdir(files[0]): outputPathVar.set(files[0])
    def melCommandScrolledText_MouseDrag(files):
        with open(files[0], "r", encoding='utf-8') as r:
            try:text=r.read()
            except:text=''
        melCommandScrolledText.delete(1.0,END)
        melCommandScrolledText.insert(1.0,text)
    windnd.hook_dropfiles(mayaInstallPathEntry,func=mayaInstallPathEntry_MouseDrag,force_unicode=1)
    windnd.hook_dropfiles(deadlineInstallPathEntry,func=deadlineInstallPathEntry_MouseDrag,force_unicode=1)
    windnd.hook_dropfiles(mayaFilesEntry,func=mayaFilesEntry_MouseDrag,force_unicode=1)
    windnd.hook_dropfiles(outputPathEntry,func=outputPathEntry_MouseDrag,force_unicode=1)
    windnd.hook_dropfiles(melCommandScrolledText,func=melCommandScrolledText_MouseDrag,force_unicode=1) #gui行数太小会卡崩???????

    # Button 颜色事件
    def SetBGColor(event):
        event.widget.config(bg='DarkSeaGreen')
    def ReturnBGColor(event):
        event.widget.config(bg='SystemButtonFace')
    for i in [mayaFilesButton,outputPathButton,localConvertButton,cmdToDeadlineButton,arnoldToDeadlineButton]:
        i.bind("<Enter>", SetBGColor)
        i.bind("<Leave>", ReturnBGColor)


    tkGUIPosition(tk,addWidth=30,addHight=10)
    tk.protocol("WM_DELETE_WINDOW",quitWindow)
    tk.mainloop()

