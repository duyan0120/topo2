# coding=gbk
import socket
import struct
import json
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host ="192.168.137.131"
port =65533
buffsize = 1024
c.connect((host, port))#���Ӷ˿ںź�������������ķ�����
print("��ʼ�Ự")
print("��������ļ�,������1,�����Ҫ�Ի�,������2,�����Ҫ������������3")
print("�����Ҫ�Ի�����,������byebye")
while True:
    send_data=input("ѡ��")
    c.sendall(bytes(send_data, encoding="utf8"))#���նԷ����������ַ�
    if send_data=="1":
        head_struct=c.recv(4)#���ձ�ͷ
        if head_struct:
            print("�����ӷ��������ȴ���������")
        head_len = struct.unpack("i",head_struct)[0]
        data = c.recv(head_len)
        head_dir = json.loads(data.decode("utf8"))#���룬ת��dirc����
        filesize_bytes=head_dir["filesize_bytes"]
        filename=head_dir["filename"]
        recv_len = 0#��ʼ��
        recv_mesg = b''
        f=open(filename,"wb")#д�ļ�
        while recv_len<filesize_bytes:#���յ��Ĵ�С�ȷ��͵��ļ�С
            if filesize_bytes - recv_len>buffsize:#���ʣ�ಿ�ֱȻ������󣬽��ջ�������С����
                recv_mesg=c.recv(buffsize)
                f.write(recv_mesg)
                recv_len += len(recv_mesg)
            else:#���ʣ�²��ֱȻ�����С��ȫ������
                recv_mesg=c.recv(filesize_bytes - recv_len)
                recv_len += len(recv_mesg)
                f.write(recv_mesg)
        print(recv_len,filesize_bytes)
        f.close()#�ر��ļ�
        print("�ļ��������")
    else:
        if send_data == "2":
            while True:
                send_data = input("I(Client)��")
                c.sendall(bytes(send_data, encoding="utf8"))#�����ַ���
                if send_data == "byebye":
                    break
                accept_data = str(c.recv(1024), encoding="utf8")#�����ַ���
                print("".join(("Server��", accept_data)))
        else:
            if send_data == "3":
                break
c.close()
print("�Ự����")
