# -*- coding:utf_8 -*-


if __name__ == '__main__':
    from os import path as ospath
    from sys import path as syspath
    #将系统查找路径加入到第2人位置。第1个保持为调用python解释器即程序启动路径
    syspath.insert(1, ospath.dirname(ospath.dirname(__file__)))

    #from utility4configreader.configreader import ConfigReader
    from executor import Executor

    ex = Executor()
    _, rs = ex.exec_cmd()
    print(rs)





