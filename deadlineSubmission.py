"""
https://stackoverflow.com/questions/37404111/maya-to-deadline-job-submission-python-command
"""

import os,subprocess,re

def tempFileWrite(fileNameExt='',fileContent=''):
    PathFileExt=f'''{os.getenv('TEMP')}/{fileNameExt}'''
    with open(PathFileExt,'w',encoding='utf-8') as i:
        i.write(fileContent)
    return PathFileExt

def submitToDeadline(deadlinePath='',JobInfo='',PluginInfo=''):
    JobInfoFile=tempFileWrite('JobInfo.job',JobInfo)
    PluginInfoFile=tempFileWrite('PluginInfo.job',PluginInfo)
    deadlinePath=f'{deadlinePath}/bin'
    command=f'''deadlinecommand.exe "{JobInfoFile}" "{PluginInfoFile}"'''
    process=subprocess.run(command,cwd=deadlinePath,shell=True,encoding='utf-8')




def quickCmdSubmit(deadlineInstallPath='',OutputDirectory='',jobName='',cmd=''):
    JobInfo=f'''
Name={jobName}
Plugin=CommandLine
Priority=51
OutputDirectory0={OutputDirectory}
'''
    PluginInfo=f'''
ShellExecute=True
Shell=cmd
SingleFramesOnly=True
Arguments={cmd}
Executable=C:/Windows/System32/cmd.exe
'''
    submitToDeadline(deadlineInstallPath,JobInfo,PluginInfo)




def queryMayaFile(mayaBinPath='',mayaFile='',mel=''):
    singleMel=mel.strip().replace('\n','').replace('\r','').replace('"',r'\"')
    process=subprocess.check_output('mayabatch.exe -file '+mayaFile+' -command "'+singleMel+'"',cwd=mayaBinPath,shell=True,encoding='utf-8',universal_newlines=True)
    processList=process.strip().split('\n')
    return processList

def quickArnoldSubmit(deadlineInstallPath='',mayaBinPath='',mayaFile=''):
    melFrameRange=r'''
string $start_frame=getAttr("defaultRenderGlobals.startFrame");
string $end_frame=getAttr("defaultRenderGlobals.endFrame");
string $frame_range[2]={"start_frame="+$start_frame,"end_frame="+$end_frame};
print($frame_range);
'''
    maya_return=queryMayaFile(mayaBinPath,mayaFile,melFrameRange)
    for i in maya_return:
        if i.startswith('start_frame='):
            start_frame=i.split('=')[-1]
        if i.startswith('end_frame='):
            end_frame=i.split('=')[-1]

    jobName=os.path.splitext(os.path.basename(mayaFile))[0]

    mayaFile=os.path.normpath(mayaFile)
    pattern=r'.+maya.*?[\\]'
    match = re.search(pattern,mayaFile,flags=re.I)
    OutputDirectory=match.group(0)+'images'

    JobInfo=f'''
Name={jobName}
Plugin=MayaCmd
Priority=50
Group=cpu
ChunkSize=5
Frames={start_frame}-{end_frame}
OutputDirectory0={OutputDirectory}
'''
    PluginInfo=f'''
Renderer=arnold
Version=2018
SceneFile={mayaFile}
OutputFilePath={OutputDirectory}
'''
    submitToDeadline(deadlineInstallPath,JobInfo,PluginInfo)




if __name__=='__main__':
#     deadlinePath=r'C:/Program Files/Thinkbox/Deadline10'
#     cmd=r'ping 127.0.0.1 > C:/Users/tthunder/Desktop/testPing.txt'
#     JobInfo=f'''
# Name=aaaaa
# Group=
# Whitelist=
# Plugin=CommandLine
# Priority=51
# OutputDirectory0='C:/Users/tthunder/Desktop'
# '''
#     PluginInfo=f'''
# ShellExecute=True
# Shell=cmd
# SingleFramesOnly=True
# Arguments={cmd}
# Executable=C:/Windows/System32/cmd.exe
# '''
    # submitToDeadline(deadlinePath,JobInfo,PluginInfo)
    melFrameRange=r'''
string $start_frame=getAttr("defaultRenderGlobals.startFrame");
string $end_frame=getAttr("defaultRenderGlobals.endFrame");
string $frame_range[2]={"start_frame="+$start_frame,"end_frame="+$end_frame};
print($frame_range);
'''
    maya_return=queryMayaFile('C:/Program Files/Autodesk/Maya2018/bin','z:/maya/aa.ma',melFrameRange)
    maya_return=maya_return.strip().split('\n')
    for i in maya_return:
        if i.startswith('start_frame='):
            start_frame=i.split('=')[-1]
        if i.startswith('end_frame='):
            end_frame=i.split('=')[-1]
    print(start_frame,end_frame)