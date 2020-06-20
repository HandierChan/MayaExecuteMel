# mayatoABC
用python执行cmd来把maya导出成abc

# 解释
mayaGUI(mel): `AbcExport -j "-file z:/a.abc";`

cmd: `mayabatch.exe -file z:/a.ma -command "AbcExport -j \"-file z:/a.abc\";" `

python: 

```python
mayaFile = 'z:/a.ma'
commandLine = 'mayabatch.exe -file '+mayaFile+' -command '+'"AbcExport -j \\"-file z:/a.abc\\";"'
os.system(commandLine)
```

# 有望那一天
1. 可能会加上只导出某对象，比如camera
2. 可能会加上反馈进度条
