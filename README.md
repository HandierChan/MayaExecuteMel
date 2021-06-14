# 简介
测试环境：win10, python3.9, maya2018
用 python 执行 cmd 来把 maya 文件(\*.ma \*.mb)导出成 alembic 文件(\*.abc)

# 说明
1. 此脚本导出文件的格式，比如导出abc是 {###.abc}，所以mel里面不要有冲突关键符" {###. "
2. 直接执行mel，记得最后加上" file -s; "

# 代码解释
mayaGUI(mel):
```bash
AbcExport -j "-file z:/a.abc";
```

windows(cmd):
```bash
mayabatch.exe -file z:/a.ma -command "AbcExport -j \"-file z:/a.abc\";"
```

python:

```python
mayaFile = 'z:/a.ma'
commandLine = 'mayabatch.exe -file '+mayaFile+' -command '+'"AbcExport -j \\"-file z:/a.abc\\";"'
os.system(commandLine)
```
