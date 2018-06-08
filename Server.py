import socket
import struct
import json
import os
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '192.168.137.131'
port = 65533
buffsize=1024#缓冲区大小
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)#重复使用端口号
s.bind((host, port))#绑定主机号和端口号
s.listen(5)#监听
c, addr = s.accept()#建立连接
while True:
    print("等待选择……")
    accept_data = str(c.recv(1024), encoding="utf8")#接收字符
    if accept_data == "1":
        print("对方选择传送文件")
        if not c:
            print("连接中断")
            break
        filemesg =input("请输入要传送的文件：").strip()
        filesize_bytes = os.path.getsize(filemesg)#得到文件大小
        filename = 'new' + filemesg
        dirc ={
            'filename':filename,
            'filesize_bytes':filesize_bytes,
        }
        head_info=json.dumps(dirc)#用于将dict类型的数据转成str
        head_info_len=struct.pack("i",len(head_info))#得到报头长度
        c.send(head_info_len)#发送报头长度
        c.send(head_info.encode("utf8"))#编码发送
        with open(filemesg,"rb") as f:#读文件
            data = f.read()
            c.sendall(data)#发送
        print("文件发送成功")
    else:
        if accept_data == "2":
            print("对方选择对话")
            while True:
                accept_data = str(c.recv(1024), encoding="utf8")#接收传过来的字符
                print("Client：",accept_data)
                if accept_data == "byebye":#进行选择，如果输入“byebye”，则退出会话
                    break
                send_data =input("I(Server)：")
                c.sendall(bytes(send_data,encoding="utf8"))#发送字符，编码
        else:
            if accept_data == "3":
                break
c.close()
print("会话结束")