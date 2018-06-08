# coding=gbk
import socket
import struct
import json
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host ="192.168.137.131"
port =65533
buffsize = 1024
c.connect((host, port))#链接端口号和主机号是这个的服务器
print("开始会话")
print("如果传送文件,请输入1,如果需要对话,请输入2,如果需要结束，请输入3")
print("如果需要对话结束,请输入byebye")
while True:
    send_data=input("选择：")
    c.sendall(bytes(send_data, encoding="utf8"))#接收对方传过来的字符
    if send_data=="1":
        head_struct=c.recv(4)#接收报头
        if head_struct:
            print("已连接服务器，等待接收数据")
        head_len = struct.unpack("i",head_struct)[0]
        data = c.recv(head_len)
        head_dir = json.loads(data.decode("utf8"))#解码，转回dirc类型
        filesize_bytes=head_dir["filesize_bytes"]
        filename=head_dir["filename"]
        recv_len = 0#初始化
        recv_mesg = b''
        f=open(filename,"wb")#写文件
        while recv_len<filesize_bytes:#当收到的大小比发送的文件小
            if filesize_bytes - recv_len>buffsize:#如果剩余部分比缓冲区大，接收缓冲区大小部分
                recv_mesg=c.recv(buffsize)
                f.write(recv_mesg)
                recv_len += len(recv_mesg)
            else:#如果剩下部分比缓冲区小，全部接收
                recv_mesg=c.recv(filesize_bytes - recv_len)
                recv_len += len(recv_mesg)
                f.write(recv_mesg)
        print(recv_len,filesize_bytes)
        f.close()#关闭文件
        print("文件接收完毕")
    else:
        if send_data == "2":
            while True:
                send_data = input("I(Client)：")
                c.sendall(bytes(send_data, encoding="utf8"))#发送字符串
                if send_data == "byebye":
                    break
                accept_data = str(c.recv(1024), encoding="utf8")#接收字符串
                print("".join(("Server：", accept_data)))
        else:
            if send_data == "3":
                break
c.close()
print("会话结束")
