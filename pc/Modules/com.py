import struct
import socket
import threading
import queue
import time
from Modules.print import *
from Modules.frame import *


F_HEADER = (0xC3, 0xF5, 0xD4, 0xA6)
F_HEADER_SIZE = 4
F_TAILER = (0xA7, 0xC8)
F_TAILER_SIZE = 2
F_MES_TAG_SIZE = 3




class ClientTcp(object):

    def __init__(self, server_host, server_port, queue_manager):
        self.server_host = server_host
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.recv_thread = None  # 接收线程
        self.process_frame_thread = None   # 处理线程
        # self.is_running = False  # 标识是否正在运行
        self.reconnect_attempts = 0  # 重新连接尝试次数
        # 创建队列用于传递接收到的帧
        self.frame_queue = queue.Queue()
        # 创建线程停止的事件对象
        self.stop_event = threading.Event()
        self.qm = queue_manager

    def connect(self):
        try:
            self.client_socket.connect((self.server_host, self.server_port))
            print('\n连接成功！')
            self.reconnect_attempts = 0  # 连接成功后重置尝试次数
        except ConnectionRefusedError:
            Print.custom_print('连接被拒绝，无法连接到服务器。')
            if self.reconnect():
                raise ConnectionRefusedError('无法连接到服务器')  # 抛出自定义异常并终止程序
        except socket.timeout:
            Print.custom_print('连接超时，无法连接到服务器。')
            if self.reconnect():
                raise socket.timeout('连接超时')  # 抛出自定义异常并终止程序
        except Exception as e:
            Print.custom_print(f'连接发生错误：{str(e)}')
            if self.reconnect():
                raise  # 抛出原始异常并终止程序

    def reconnect(self):
        while True:
            self.reconnect_attempts += 1
            if self.reconnect_attempts > 5:
                Print.custom_print('连接尝试次数超过上限，无法重新连接。')
                self.client_socket.close()
                # self.stop_recv_thread()  # 关闭线程
                # self.stop_process_frame()
                return -1
            print(f'\n正在重新连接，尝试次数：{self.reconnect_attempts}...')


            self.client_socket.close()
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # while True:
            try:
                self.client_socket.connect((self.server_host, self.server_port))
                print('\n重新连接成功！')
                self.reconnect_attempts = 0  # 连接成功后重置尝试次数
                break
            except ConnectionRefusedError:
                Print.custom_print('连接被拒绝，无法连接到服务器。')
            except socket.timeout:
                Print.custom_print('连接超时，无法连接到服务器。')
            except Exception as e:
                Print.custom_print(f'连接发生错误：{str(e)}')
            time.sleep(5)  # 等待5秒后重试连接
        return 0

    def send_cmd(self, frame_stream):
        try:
            self.client_socket.send(frame_stream)
            print('\n数据发送成功！')
        except BrokenPipeError:
            Print.custom_print('连接已中断，无法发送数据。')
        except OSError as e:
            Print.custom_print(f'发送数据时发生错误：{str(e)}')

    def start_recv_thread(self):
        self.recv_thread = threading.Thread(target=self._recv_thread_func)
        self.recv_thread.start()

    def stop_recv_thread(self):
        self.stop_event.set()
        if self.recv_thread is not None:
            # self.recv_thread.join()
            self.recv_thread = None

    def _recv_thread_func(self):
        while not self.stop_event.is_set():
            frame = self.recv_frame()
            if frame is not None:
                # 将接收到的帧放入队列
                self.frame_queue.put(frame)

    def recv_frame(self):
        # 接收帧头
        header = bytearray()
        for i in range(4):
            chunk = self.client_socket.recv(1)
            if not chunk:
                Print.custom_print('连接已中断，无法接收帧头。')
                if self.reconnect():
                    self.stop_process_frame()
                    self.stop_recv_thread()
                return None
            elif i == 0:
                if chunk != b'\xc3':
                    Print.custom_print('错误帧头'+ str(i) + ': ' + chunk.hex())
                    return None
            elif i == 1:
                if chunk != b'\xf5':
                    Print.custom_print('错误帧头'+ str(i) + ': ' + chunk.hex())
                    return None
            elif i == 2:
                if chunk != b'\xd4':
                    Print.custom_print('错误帧头'+ str(i) + ': ' + chunk.hex())
                    return None
            elif i == 3:
                if chunk != b'\xa6':
                    Print.custom_print('错误帧头'+ str(i) + ': ' + chunk.hex())
                    return None
            header += chunk

        # 检查帧头
        if header != bytearray(F_HEADER):
            Print.custom_print('无效的帧头。')
            return None

        # print(header.hex())

        # 接收帧Dword1：3
        dword1_3 = bytearray()
        dword1_3_len = 12
        while len(dword1_3) < dword1_3_len:
            chunk = self.client_socket.recv(dword1_3_len - len(dword1_3))
            if not chunk:
                Print.custom_print('连接已中断，无法接收帧内容。')
                if self.reconnect():
                    self.stop_process_frame()
                    self.stop_recv_thread()
                return None
            dword1_3 += chunk
        # print(dword1_3.hex())

        # 接收帧内容长度
        content_len_bytes = self.client_socket.recv(4)
        if len(content_len_bytes) < 4:
            Print.custom_print('无法接收帧内容长度。')
            return None
        content_len = struct.unpack('!I', content_len_bytes)[0]
        # print(content_len_bytes.hex())
        # 接收帧内容
        content = bytearray()
        while len(content) < content_len:
            chunk = self.client_socket.recv(content_len - len(content))
            if not chunk:
                Print.custom_print('连接已中断，无法接收帧内容。')
                if self.reconnect():
                    self.stop_process_frame()
                    self.stop_recv_thread()
                return None
            content += chunk
        # print(content.hex())

        # 接收crc
        crc = self.client_socket.recv(2)
        crc1 = int.from_bytes(crc, byteorder='big')
        frame_revalidation = header + dword1_3 + struct.pack('!I', content_len) + content
        crc_revalidation = FrameDVT.crc(frame_revalidation)
        if crc1 != crc_revalidation:
            Print.custom_print('ERR: wrong crc, calculate cre: %x  original crc: %x.' % (crc_revalidation, crc1))
            return None
        # print(crc.hex())

        # 接收帧尾
        tailer = bytearray()
        while len(tailer) < F_TAILER_SIZE:
            chunk = self.client_socket.recv(F_TAILER_SIZE - len(tailer))
            if not chunk:
                Print.custom_print('连接已中断，无法接收帧尾。')
                if self.reconnect():
                    self.stop_process_frame()
                    self.stop_recv_thread()
                return None
            tailer += chunk
        # print(tailer.hex())
        # 检查帧尾
        if tailer != bytearray(F_TAILER):
            Print.custom_print('无效的帧尾。')
            return None

        # 构建完整帧
        frame = header + dword1_3 + struct.pack('!I', content_len) + content + crc + tailer
        return frame

    def start_process_frame(self):
        self.process_frame_thread = threading.Thread(target=self._process_frame_func)
        self.process_frame_thread.start()

    def stop_process_frame(self):
        if self.process_frame_thread is not None:
            self.stop_event.set()
            # self.process_frame_thread.join()
            self.process_frame_thread = None

    def _process_frame_func(self):
        while not self.stop_event.is_set():
            try:
                frame = self.frame_queue.get(timeout=1)  # 阻塞等待获取帧，超时时间为1秒
                self.process_frame(frame)
            except queue.Empty:
                pass

    def process_frame(self, frame):
        # 处理接收到的帧的逻辑
        # print(frame.hex())
        frame_tmp = FrameDVT()
        if frame_tmp.parse_frame(frame):
            Print.custom_print('crc error.')
        type = frame_tmp.f_type
        if type == 0x00:
            Print.custom_print('wrong type: 0x%x. shouldn\'t recieve cmd frame. \n' % type)
        elif type == 0x01:
            q = self.qm.get_queue1()
            q1 = self.qm.get_queue2()
            q.put(frame)
            q1.put(frame)
        elif type == 0x02:
            q = self.qm.get_queue2()
            q.put(frame)
        elif type == 0x03:
            q = self.qm.get_queue3()
            q.put(frame)
        else:
            Print.custom_print('wrong type: 0x%x. beyond the type boundary. ' % type)

