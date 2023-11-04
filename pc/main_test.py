from Modules.com import *
from Modules.frame import *
from Modules.log import *
from Modules.queue_manager import *
from Modules.log import *

q_manager = QueueManager()
dict1 = {
    'type': 0x01,
    'dev_tag': 0x01,
    'mod_tag': 0x00,
    'islast_tag': 0x01,
    'status': 0x00,
    'mes_tag': 0x000001,
    'stream_tag': 0x00000001,
    # 'content_len': 6,
    'content': [0x00, 0x00, 0x00, 0x00, \
                0x00, 0x00, 0x00, 0x11, \
                0x00, 0x00, 0x00, 0x11, \
                0xFF, 0xFF, 0x01]
    # 'content': []
}

# while True:
frame = FrameDVT(**dict1)
packed_frame = frame.pack_frame()
print(packed_frame.hex())  # 打印原始的帧数据

byte_array_frame = bytearray(packed_frame)  # 转换为可变字节数组
# byte_array_frame[0] = 0xA8  # 修改第一个字节的值为0xA8

modified_frame = bytes(byte_array_frame)  # 转换回字节序
print(modified_frame.hex())  # 打印修改后的帧数据

frame.parse_frame(modified_frame)  # 解析修改后的帧数据
packed_frame = frame.pack_frame()
print(packed_frame.hex())  # 打印再次打包后的帧数据
# time.sleep(1)
log = LogProcess(q_manager)
log.start()

server_host = '192.168.140.1'
server_port = 8080
client_tcp = ClientTcp(server_host, server_port, q_manager)
client_tcp.connect()
client_tcp.start_recv_thread()
client_tcp.start_process_frame()
client_tcp.send_cmd(packed_frame)
# client_tcp.
