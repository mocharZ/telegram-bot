import pip

#测试自己python支持哪些文件名的whl安装包
def ss():
    print(pip.pep425tags.get_supported())

