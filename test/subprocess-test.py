#-*- coding:utf_8 -*-

'''
subprocess 模块允许你生成新的进程，连接它们的输入、输出、错误管道，
并且获取它们的返回码。此模块打算代替一些老旧的模块与功能：os.system 与 os.spawn*

推荐的调用子进程的方式是在任何它支持的用例中使用 run() 函数。对于更进阶的用例，也可以使用底层的 Popen 接口。
subprocess.run(args, *, stdin=None, input=None, stdout=None, stderr=None, capture_output=False,
                shell=False, cwd=None, timeout=None, check=False, encoding=None, errors=None, 
                text=None, env=None, universal_newlines=None, **other_popen_kwargs)

'''

import subprocess as subp


def frpc(cmd):
    rs = subp.run(	["systemctl", "--user", F"{cmd}", "frpc.service"],
                    capture_output=True,
                    encoding='UTF-8'
    )
    print('\r\n------the return --------\r\n',rs)
    print('\r\n------the return .stdout-------\r\n',rs.stdout)


def net(cmd):
    rs = subp.run(  ["systemctl", "--user", F"{cmd}", "networking.service"],
                    capture_output=True,
                    encoding='UTF-8'
    )
    print('\r\n------the return -------\r\n',rs)
    print('\r\n------the return .stdout-------\r\n',rs.stdout)

#frpc('stop')

net("status")