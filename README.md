# mayatoABC
用 python 执行 cmd 来把 maya 文件(\*.ma \*.mb)导出成 alembic 文件(\*.abc)


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

# 有望那一天
1. 可能会加上只导出某对象，比如camera
2. 可能会加上反馈进度条
