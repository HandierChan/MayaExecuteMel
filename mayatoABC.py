import os
from tkinter import *

def MayaMeltoCMD():
    mayaEXE = mayaInstPath.get()+'/bin/mayabatch.exe'
    mayaPath = mayaPathEntry.get()
    abcPath = abcPathEntry.get()

    mayaAbsEXE = os.path.abspath(mayaEXE)
    mayaAbsPath = os.path.abspath(mayaPath)
    abcAbsPath = os.path.abspath(abcPath)

    fileLists = [i for i in os.listdir(mayaAbsPath) if os.path.isfile(mayaAbsPath+'/'+i)]
    mayaExt = ['.ma','.mb']
    mayaFiles = [i for i in fileLists if os.path.splitext(i)[1] in mayaExt]

    for i in mayaFiles:
        mayaName = os.path.splitext(i)[0]
        mayaExt = os.path.splitext(i)[1]
        mayaExec = '\"'+mayaAbsEXE+'\"'+' -file '+'\"'+mayaAbsPath+'/'+mayaName+mayaExt+'\"'
        mel = 'int $startFrame=`playbackOptions -q -ast`;\
            int $endFrame=`playbackOptions -q -aet`;\
            string $commandMel=\\"-frameRange \\"+$startFrame+\\" \\"+$endFrame+\\" -file '+'\\\\\\\"'+abcAbsPath+'/'+mayaName+'.abc'+'\\\\\\\"'+' -uvWrite -worldSpace -writeVisibility -dataFormat ogawa\\";\
            AbcExport -j $commandMel;'
        cmd = mayaExec+' -command '+'"'+mel+'"'
        os.system(cmd)
        print(mayaExec)

def aa():
    mayaInst=mayaInstPath.get()+'/bin/mayabatch.exe'
    print(mayaInst)

tk = Tk()
tk.title("mayaExportABC")
tk.geometry("550x150+500+500")

# Variable
mayaVarInstPath = StringVar(tk, value=r'C:\Progra~1\Autodesk\Maya2018')
mayaVarPath = StringVar(tk,'z:/')
abcVarPath = StringVar(tk,'z:/')

# Widget
mayaInstPathLabel = Label(tk, text="Maya Install Path")
mayaInstPath = Entry(tk, textvariable=mayaVarInstPath)
mayaFileLabel = Label(tk, text="Maya Path")
mayaPathEntry = Entry(tk, textvariable=mayaVarPath)
abcPathLabel = Label(tk, text="ABC Path")
abcPathEntry = Entry(tk, textvariable=abcVarPath)
convert = Button(tk, text="Convert", command=MayaMeltoCMD)

# Layout
mayaInstPathLabel.grid(row=0, sticky='e')
mayaInstPath.grid(row=0, column='1', sticky='we',ipadx=150)
mayaFileLabel.grid(row=1, sticky='e')
mayaPathEntry.grid(row=1, column='1', sticky='we',ipadx=150)
abcPathLabel.grid(row=2, sticky='e')
abcPathEntry.grid(row=2, column='1', sticky='we',ipadx=150)
convert.grid(row=3, column='1',sticky='w')

tk.mainloop()
