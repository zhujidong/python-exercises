# 回显客户端程序
import socket

HOST = ''    # 远端主机
PORT = 50007              # 与服务器所用端口相同
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print('connect...')

    while True:
        ch = input()    
        if ch=='QUIT':
            break
        else:
            s.sendall(ch.encode())
            data = s.recv(1024)
            print('Received:', data.decode())