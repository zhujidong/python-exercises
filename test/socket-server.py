#server program
import socket

HOST = ''                 # 该符号名表示所有可用接口
PORT = 50007              # 任意非特权端口

try:
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(0)
    while True:
        print('waiting for Connect...')
        conn, addr = s.accept()
        print('Connected by:', addr)
        try:
            while True:
                data = conn.recv(1024)
                if data: 
                    print('Received:', data.decode())
                    conn.sendall(data)
                else:
                    print('disconnected, bye')
                    break
        finally:
            conn.close()
finally:
    s.close()
