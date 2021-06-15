"""
https://stackoverflow.com/questions/37404111/maya-to-deadline-job-submission-python-command
"""

import os,subprocess

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

def quickSubmit_CMD(deadlineInstallPath='',OutputDirectory='',jobName='',cmd=''):
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

if __name__=='__main__':
    deadlinePath=r'C:/Program Files/Thinkbox/Deadline10'
    cmd='ping 127.0.0.1 > C:/Users/tthunder/Desktop/testPing.txt'
    JobInfo=f'''
Name=testPing
Group=
Whitelist=
Plugin=CommandLine
Priority=51
OutputDirectory0='C:/Users/tthunder/Desktop'
'''
    PluginInfo=f'''
ShellExecute=True
Shell=cmd
SingleFramesOnly=True
Arguments={cmd}
Executable=C:/Windows/System32/cmd.exe
'''
    submitToDeadline(deadlinePath,JobInfo,PluginInfo)
