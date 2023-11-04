from Modules.frame import *
from Modules.queue_manager import *

import threading
import queue
import os
from datetime import datetime


class LogProcess:
    def __init__(self, queue_manager, name):
        self.input_queue = queue_manager.get_queue3()
        self.output_queue_1 = queue.Queue()
        self.output_queue_2 = queue.Queue()
        self.dev_name = name

    def start(self):
        thread_receiver = threading.Thread(target=self.recv_log)
        thread_processor_1 = threading.Thread(target=self.print_log)
        thread_processor_2 = threading.Thread(target=self.save_log)

        thread_receiver.start()
        thread_processor_1.start()
        thread_processor_2.start()

    def recv_log(self):
        while True:
            # 假设此处从外部队列接收数据，并放入输入队列
            frame = self.input_queue.get()
            self.output_queue_1.put(frame)
            self.output_queue_2.put(frame)

    def print_log(self):
        while True:
            frame = self.output_queue_1.get()
            # 对数据进行处理，假设为打印数据
            frame_parse = FrameDVT()
            frame_parse.parse_frame(frame)
            log_bytes = bytes(frame_parse.f_content)
            print(log_bytes.decode('utf-8'))
            # print(log_bytes.decode('ascii'))

    def save_log(self):
        # 获取当前时间
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        # 构建文件名
        file_name = current_time + self.dev_name + "_log.txt"
        # 构建文件路径
        os.makedirs("log", exist_ok=True)
        file_path = os.path.join("log", file_name)
        while True:
            frame = self.output_queue_2.get()
            frame_parse = FrameDVT()
            frame_parse.parse_frame(frame)
            log_bytes = bytes(frame_parse.f_content)
            log_string = log_bytes.decode('utf-8')
            with open(file_path, 'a', encoding='utf-8') as file:
                file.write(log_string)
            # print('log写入成功。')


# # 示例函数，模拟从外部队列接收数据
# def receive_from_external_queue():
#     return "Data from external queue"
#
# # 创建 DataProcessor 实例
# data_processor = DataProcessor()
#
# # 启动 DataProcessor
# data_processor.start()
