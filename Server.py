import socket
import struct
import json
import os
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '192.168.137.131'
port = 65533
buffsize=1024#��������С
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)#�ظ�ʹ�ö˿ں�
s.bind((host, port))#�������źͶ˿ں�
s.listen(5)#����
c, addr = s.accept()#��������
while True:
    print("�ȴ�ѡ�񡭡�")
    accept_data = str(c.recv(1024), encoding="utf8")#�����ַ�
    if accept_data == "1":
        print("�Է�ѡ�����ļ�")
        if not c:
            print("�����ж�")
            break
        filemesg =input("������Ҫ���͵��ļ���").strip()
        filesize_bytes = os.path.getsize(filemesg)#�õ��ļ���С
        filename = 'new' + filemesg
        dirc ={
            'filename':filename,
            'filesize_bytes':filesize_bytes,
        }
        head_info=json.dumps(dirc)#���ڽ�dict���͵�����ת��str
        head_info_len=struct.pack("i",len(head_info))#�õ���ͷ����
        c.send(head_info_len)#���ͱ�ͷ����
        c.send(head_info.encode("utf8"))#���뷢��
        with open(filemesg,"rb") as f:#���ļ�
            data = f.read()
            c.sendall(data)#����
        print("�ļ����ͳɹ�")
    else:
        if accept_data == "2":
            print("�Է�ѡ��Ի�")
            while True:
                accept_data = str(c.recv(1024), encoding="utf8")#���մ��������ַ�
                print("Client��",accept_data)
                if accept_data == "byebye":#����ѡ��������롰byebye�������˳��Ự
                    break
                send_data =input("I(Server)��")
                c.sendall(bytes(send_data,encoding="utf8"))#�����ַ�������
        else:
            if accept_data == "3":
                break
c.close()
print("�Ự����")