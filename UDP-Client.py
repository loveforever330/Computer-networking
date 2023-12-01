# 客户端代码
import socket
import os

# 创建一个UDP套接字
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 输入服务器端的IP地址和端口号
server_ip = input("请输入服务器端的IP地址：")
server_port = int(input("请输入服务器端的端口号："))

# 输入要传输的文件夹的路径
folder_path = input("请输入要传输的文件夹的路径：")
if not folder_path.endswith("\\"): # 如果路径不以反斜杠结尾，就加上一个
    folder_path += "\\"

# 获取文件夹中的所有文件名
file_names = os.listdir(folder_path)

# 循环遍历每个文件
for file_name in file_names:
    # 打开文件，准备读取数据
    file = open(folder_path + file_name, "rb")

    # 获取文件大小
    file_size = os.path.getsize(folder_path + file_name)

    # 发送文件名和文件大小给服务器端
    client.sendto(file_name.encode(), (server_ip, server_port))
    client.sendto(str(file_size).encode(), (server_ip, server_port))

    # 打印发送的文件信息
    print(f"正在发送文件：{file_name}，大小为{file_size}字节")

    # 初始化已发送的文件大小
    sent_size = 0

    # 循环读取文件数据，直到文件末尾
    while True:
        # 读取文件数据
        data = file.read(1024)
        # 如果数据为空，说明文件已经读完，跳出循环
        if not data:
            break
        # 发送文件数据给服务器端
        client.sendto(data, (server_ip, server_port))
        # 更新已发送的文件大小
        sent_size += len(data)
        # 打印发送进度
        print(f"\r已发送{sent_size/file_size*100:.2f}%，{sent_size}/{file_size}", end="")

    # 关闭文件
    file.close()

    # 打印发送完成的信息
    print(f"\n文件{file_name}发送完成，等待服务器端的回复")

    # 接收服务器端的确认信息
    reply, server_address = client.recvfrom(1024)
    reply = reply.decode() # 将字节串解码为字符串
    print(f"收到来自{server_address}的回复：{reply}")

# 关闭套接字
client.close()
