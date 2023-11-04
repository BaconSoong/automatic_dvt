# # import sys
# # from PyQt5.QtWidgets import QApplication, QWidget, QProgressBar, QVBoxLayout, QPushButton
# # from PyQt5.QtCore import QTimer
# #
# # class ProgressBarExample(QWidget):
# #     def __init__(self):
# #         super().__init__()
# #         self.initUI()
# #
# #     def initUI(self):
# #         self.setWindowTitle('Indeterminate Progress Bar')
# #         self.setGeometry(100, 100, 400, 200)
# #
# #         layout = QVBoxLayout()
# #
# #         self.progress_bar = QProgressBar()
# #         self.progress_bar.setRange(0, 0)  # 设置范围为0，表示不确定进度
# #         layout.addWidget(self.progress_bar)
# #
# #         self.start_button = QPushButton('Start Task')
# #         self.start_button.clicked.connect(self.start_task)
# #         layout.addWidget(self.start_button)
# #
# #         self.setLayout(layout)
# #
# #         self.timer = QTimer(self)
# #         self.timer.timeout.connect(self.update_progress)
# #         self.task_started = False  # 用于标记任务是否已开始
# #
# #     def start_task(self):
# #         if not self.task_started:
# #             self.progress_bar.setFormat("Task in progress")
# #             self.timer.start(50)  # 定时器用于模拟任务进行中
# #             self.task_started = True
# #
# #     def update_progress(self):
# #         # 模拟任务进行中
# #         if self.progress_bar.text() == "Task in progress...":
# #             self.progress_bar.setFormat("Task in progress")
# #         else:
# #             self.progress_bar.setFormat("Task in progress...")
# #         self.progress_bar.repaint()
# #
# # if __name__ == '__main__':
# #     app = QApplication(sys.argv)
# #     window = ProgressBarExample()
# #     window.show()
# #     sys.exit(app.exec_())
# from Modules.com import *
# from Modules.frame import *
# from Modules.log import *
# from Modules.queue_manager import *
# from Modules.log import *
#
# q_manager = QueueManager()
# dict1 = {
#     'type': 0x03,
#     'dev_tag': 0x01,
#     'mod_tag': 0x02,
#     'islast_tag': 0x03,
#     'status': 0x04,
#     'mes_tag': 0x010203,
#     'stream_tag': 0x0A0B0C0D,
#     # 'content_len': 6,
#     'content': [0x64, 0x69, 0x63, 0x74, 0x20, 0x3D, 0x20, 0x7B, 0x0D, 0x0A, 0x20, 0x20, 0x20, 0x20, 0x27, 0x64, 0x65,
#                 0x76, 0x30, 0x27, 0x20, 0x3A, 0x20, 0x7B, 0x0D, 0x0A, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20,
#                 0x27, 0x6D, 0x6F, 0x64, 0x75, 0x6C, 0x65, 0x30, 0x27, 0x20, 0x3A, 0x20, 0x5B]
# }
#
# # while True:
# frame = FrameDVT(**dict1)
# packed_frame = frame.pack_frame()
# print(packed_frame.hex())  # 打印原始的帧数据
#
# byte_array_frame = bytearray(packed_frame)  # 转换为可变字节数组
# # byte_array_frame[0] = 0xA8  # 修改第一个字节的值为0xA8
#
# modified_frame = bytes(byte_array_frame)  # 转换回字节序
# print(modified_frame.hex())  # 打印修改后的帧数据
#
# frame.parse_frame(modified_frame)  # 解析修改后的帧数据
# packed_frame = frame.pack_frame()
# print(packed_frame.hex())  # 打印再次打包后的帧数据
# # time.sleep(1)
# log = LogProcess(q_manager)
# log.start()
#
# server_host = '192.168.122.1'
# server_port = 8080
# client_tcp = ClientTcp(server_host, server_port, q_manager)
# client_tcp.connect()
# client_tcp.start_recv_thread()
# client_tcp.start_process_frame()
# client_tcp.send_cmd(packed_frame)
# # client_tcp.

# import time
# from colorama import init, Fore
#
# # 初始化colorama
# init()
#
# # 动画帧和初始文字
# frames = ['-', '\\', '|', '/']
# text = "Loading..."
#
# # 打印动画
# for i in range(1000000):
#     # 获取当前帧
#     frame = frames[i % len(frames)]
#
#     # 设置光标位置并打印动画帧和文字
#     print(f'\r{Fore.GREEN}{frame} {text}', end='')
#
#     # 更新文字
#     text = "Loading" + "." * (i % 4 + 1)
#
#     # 延迟一段时间
#     time.sleep(0.2)
#
# # 恢复光标位置
# print('\r', end='')
#
# # 清除colorama设置
# init(autoreset=True)

# import time
# from colorama import init, Fore
# from threading import Thread
#
# # 初始化colorama
# init()
#
# # 动画帧和初始文字
# frames = ['-', '\\', '|', '/']
# text = "Loading..."
#
#
# # 打印动画的函数
# def print_animation():
#     for i in range(10):
#         # 获取当前帧
#         frame = frames[i % len(frames)]
#
#         # 设置光标位置并打印动画帧和文字
#         print(f'\r{Fore.GREEN}{frame} {text}', end='')
#
#         # 更新文字
#         text = "Loading" + "." * (i % 4 + 1)
#
#         # 延迟一段时间
#         time.sleep(0.2)
#
#
# # 创建线程并启动
# thread = Thread(target=print_animation)
# thread.start()
#
# # 在主线程中执行其他操作
# # ...
#
# # 等待线程结束
# thread.join()
#
# # 恢复光标位置
# print('\r', end='')
#
# # 清除colorama设置
# init(autoreset=True)


# import time
# from colorama import init, Fore
# from threading import Thread
#
# # 初始化colorama
# init()
#
# # 动画帧和初始文字
# frames = ['-', '\\', '|', '/']
# text = ""
#
#
# # 打印动画的函数
# def print_animation():
#     global text  # 声明变量为全局变量
#     for i in range(10):
#         # 获取当前帧
#         frame = frames[i % len(frames)]
#
#         # 设置光标位置并打印动画帧和文字
#         print(f'\r{Fore.GREEN}{frame} {text}', end='')
#
#         # 更新文字
#         text = "Loading" + "." * (i % 4 + 1)
#
#         # 延迟一段时间
#         time.sleep(0.2)
#
#
# # 创建线程并启动
# thread = Thread(target=print_animation)
# thread.start()
#
# # 在主线程中执行其他操作
# # ...
#
# # 等待线程结束
# thread.join()
#
# # 恢复光标位置
# print('\r', end='')
#
# # 清除colorama设置
# init(autoreset=True)

# import time
# from colorama import init, Fore
# from threading import Thread
#
# # 初始化colorama
# init()
#
# # 动画帧和初始文字
# frames = ['-', '\\', '|', '/']
# texts = ["Loading...", "Processing...", "Waiting..."]
#
#
# # 打印动画的函数
# def print_animation(thread_id, text):
#     for i in range(10000):
#         # 获取当前帧
#         frame = frames[i % len(frames)]
#
#         # 设置光标位置并打印动画帧和文字
#         print(f'\r{Fore.GREEN}[Thread {thread_id}] {frame} {text}', end='')
#
#         # 延迟一段时间
#         time.sleep(1)
#
#
# # 创建并启动线程
# threads = []
# for i, text in enumerate(texts):
#     thread = Thread(target=print_animation, args=(i + 1, text))
#     thread.start()
#     threads.append(thread)
#
# # 等待所有线程结束
# for thread in threads:
#     thread.join()
#
# # 恢复光标位置
# print('\r', end='')
#
# # 清除colorama设置
# init(autoreset=True)
#
# import time
# from colorama import init, Fore
# from threading import Thread, Lock
#
# # 初始化colorama
# init()
#
# # 动画帧和初始文字
# frames = ['-', '\\', '|', '/']
# texts = ["Loading...", "Processing...", "Waiting..."]
#
# # 创建线程锁
# lock = Lock()
#
# # 打印动画的函数
# def print_animation(thread_id, text):
#     for i in range(10000):
#         # 获取当前帧
#         frame = frames[i % len(frames)]
#
#         # 获取锁
#         lock.acquire()
#
#         # 设置光标位置并打印动画帧和文字
#         print(f'\r{Fore.GREEN}[Thread {thread_id}] {frame} {text}', end='')
#
#         # 释放锁
#         lock.release()
#
#         # 延迟一段时间
#         time.sleep(1)
#
#
# # 创建并启动线程
# threads = []
# for i, text in enumerate(texts):
#     thread = Thread(target=print_animation, args=(i + 1, text))
#     thread.start()
#     threads.append(thread)
#
# # 等待所有线程结束
# for thread in threads:
#     thread.join()
#
# # 恢复光标位置
# print('\r', end='')
#
# # 清除colorama设置
# init(autoreset=True)

# import time
# from colorama import init, Fore
# from threading import Thread
# from queue import Queue
#
# # 初始化colorama
# init()
#
# # 动画帧和初始文字
# frames = ['-', '\\', '|', '/']
#
# # 打印动画的函数
# def print_animation(queue):
#     # text = "Loading..."
#     text = {
#     "dev0": {
#         "0x0": {
#             "success_times": 0,
#             "failure_times": 9,
#             "error_case": [
#                 "0b11111111",
#                 "0b11111111",
#                 "0b1"
#             ]
#         },
#         "0x1": {
#             "success_times": 0,
#             "failure_times": 0,
#             "error_case": []
#         },
#         "0x2": {
#             "success_times": 0,
#             "failure_times": 0,
#             "error_case": []
#         }
#     },
#     "dev1": {
#         "0x0": {
#             "success_times": 0,
#             "failure_times": 0,
#             "error_case": []
#         },
#         "0x1": {
#             "success_times": 0,
#             "failure_times": 10,
#             "error_case": [
#                 "0b11111111",
#                 "0b11111110",
#                 "0b1"
#             ]
#         },
#         "0x2": {
#             "success_times": 0,
#             "failure_times": 0,
#             "error_case": []
#         }
#     },
#     "dev2": {
#         "0x0": {
#             "success_times": 0,
#             "failure_times": 0,
#             "error_case": []
#         },
#         "0x1": {
#             "success_times": 0,
#             "failure_times": 0,
#             "error_case": []
#         },
#         "0x2": {
#             "success_times": 0,
#             "failure_times": 3,
#             "error_case": [
#                 "0b11111111",
#                 "0b11111110",
#                 "0b1"
#             ]
#         }
#     }
# }
#     for i in range(10000):
#         # 获取当前帧
#         frame = frames[i % len(frames)]
#
#         # 检查队列是否有数据
#         if not queue.empty():
#             text = queue.get()
#
#         # 设置光标位置并打印动画帧和文字
#         print(f'\r{Fore.GREEN}{frame} {text}', end='')
#
#         # 延迟一段时间
#         time.sleep(1)
#
#
# # 创建并启动线程
# queue = Queue()
# thread = Thread(target=print_animation, args=(queue,))
# thread.start()
#
# # 模拟接收到不同的text
# # queue.put("Processing...")
# # time.sleep(3)
# # queue.put("Waiting...")
# # time.sleep(3)
#
# # 等待线程结束
# thread.join()
#
# # 恢复光标位置
# print('\r', end='')
#
# # 清除colorama设置
# init(autoreset=True)


import time
from colorama import init, Fore
from threading import Thread
from queue import Queue

# 初始化colorama
init()

# 动画帧和初始文字
frames = ['-', '\\', '|', '/']


# 打印动画的函数
def print_animation(queue):
    text = {
        "dev0": {
            "0x0": {
                "success_times": 0,
                "failure_times": 9,
                "error_case": [
                    "0b11111111",
                    "0b11111111",
                    "0b1"
                ]
            },
            "0x1": {
                "success_times": 0,
                "failure_times": 0,
                "error_case": []
            },
            "0x2": {
                "success_times": 0,
                "failure_times": 0,
                "error_case": []
            }
        },
        "dev1": {
            "0x0": {
                "success_times": 0,
                "failure_times": 0,
                "error_case": []
            },
            "0x1": {
                "success_times": 0,
                "failure_times": 10,
                "error_case": [
                    "0b11111111",
                    "0b11111110",
                    "0b1"
                ]
            },
            "0x2": {
                "success_times": 0,
                "failure_times": 0,
                "error_case": []
            }
        },
        "dev2": {
            "0x0": {
                "success_times": 0,
                "failure_times": 0,
                "error_case": []
            },
            "0x1": {
                "success_times": 0,
                "failure_times": 0,
                "error_case": []
            },
            "0x2": {
                "success_times": 0,
                "failure_times": 3,
                "error_case": [
                    "0b11111111",
                    "0b11111110",
                    "0b1"
                ]
            }
        }
    }

    for i in range(10000):
        # 获取当前帧
        frame = frames[i % len(frames)]

        # 检查队列是否有数据
        if not queue.empty():
            text = queue.get()

        # 格式化输出文字内容
        formatted_text = format_text(text)

        # 设置光标位置并打印动画帧和文字
        print(f'\r{Fore.GREEN}{frame} {formatted_text}', end='')

        # 延迟一段时间
        time.sleep(1)


# 格式化输出文字内容
def format_text(text, indent=0):
    formatted_text = ""
    for key, value in text.items():
        formatted_text += f"{indent * '  '}{key}:"
        if isinstance(value, dict):
            formatted_text += '\n' + format_text(value, indent + 1)
        else:
            formatted_text += f" {value}\n"
    return formatted_text


# 创建并启动线程
queue = Queue()
thread = Thread(target=print_animation, args=(queue,))
thread.start()

# 模拟接收到不同的text
# queue.put(text)
# time.sleep(3)
# queue.put(text)
# time.sleep(3)

# 等待线程结束
thread.join()

# 恢复光标位置
print('\r', end='')

# 清除colorama设置
init(autoreset=True)