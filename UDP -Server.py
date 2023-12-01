# 服务器端代码 
import socket
import os

# 创建一个UDP套接字
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 绑定服务器端的IP地址和端口号
server_ip = "192.168.186.128" # 可以修改这个IP地址
server_port =12345 # 可以修改这个端口号
server.bind((server_ip, server_port))

# 指定保存文件的文件夹路径
save_path = "/home/jdqi/Desktop/trans//" # 可以修改这个路径
if not os.path.exists(save_path): # 如果文件夹不存在，就创建一个
    os.mkdir(save_path)

# 循环接收客户端发送的文件
while True:
    # 接收客户端发送的文件名和文件大小
    file_name, client_address = server.recvfrom(1024)
    file_name = file_name.decode() # 将字节串解码为字符串
    file_size, client_address = server.recvfrom(1024)
    file_size = int(file_size.decode()) # 将字节串解码为整数

    # 打印接收到的文件信息
    print(f"接收到来自{client_address}的文件：{file_name}，大小为{file_size}字节")

    # 打开一个新的文件，准备写入数据
    file = open(save_path + file_name, "wb")

    # 初始化已接收的文件大小
    received_size = 0

    # 循环接收文件数据，直到文件大小等于已接收的大小
    while received_size < file_size:
        # 接收文件数据
        data, client_address = server.recvfrom(1024)
        # 写入文件
        file.write(data)
        # 更新已接收的文件大小
        received_size += len(data)
        # 打印接收进度
        print(f"\r已接收{received_size/file_size*100:.2f}%，{received_size}/{file_size}", end="")

    # 关闭文件
    file.close()

    # 打印接收完成的信息
    print(f"\n文件{file_name}接收完成，保存在{save_path}")

    # 向客户端发送一个确认信息
    server.sendto(b"OK", client_address)
