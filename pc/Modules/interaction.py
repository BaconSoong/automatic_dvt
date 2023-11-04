import queue
import time
from colorama import init, Fore
from threading import Thread
from Modules.frame import *
from Modules.com import *


class Interaction:
    def __init__(self, name, dev_num, strategy, com, queue_manager, queue_inquire):
        self.dev_name = name
        self.dev_num = dev_num
        self.testing_strategy = strategy
        self.com = com
        self.q_m = queue_manager
        self.q_i = queue_inquire
        self.q_s = queue.Queue()
        self.frames = ['-', '\\', '|', '/']  # 动画帧和初始文字
        self.threads = []
        self.stop_print = threading.Event()
        self.mutex = threading.Lock()
        self.finish_cnt = 0

    def print_animation(self):
        text = "DVT ing..."
        i = 0
        init()  # 初始化colorama
        while not self.stop_print.is_set():
            # 获取当前帧
            frame = self.frames[i % len(self.frames)]
            i += 1
            # 检查队列是否有数据
            if not self.q_s.empty():
                text += self.q_s.get()

            # 设置光标位置并打印动画帧和文字
            print(f'\r{Fore.GREEN}{frame} {text}', end='')

            # 延迟一段时间
            time.sleep(0.1)

    def start_test(self, dev_index, mod_index, frame_dict):
        frame_tmp = FrameDVT(**frame_dict)
        frame = frame_tmp.pack_frame()
        self.com[dev_index].send_cmd(frame)
        loop_count = 0
        while True:
            if self.testing_strategy[mod_index][1] == 'parallelable':
                return 0

            if not self.q_m[dev_index].get_queue2().empty():
                frame = self.q_m[dev_index].get_queue2().get()
                frame_tmp.parse_frame(frame)
                if frame_tmp.f_type != 0x02:
                    if frame_tmp.f_mod_tag == mod_index:
                        return 0
                    # else:
                    #     loop_count += 1
                elif frame_tmp.f_mod_tag == mod_index:
                    loop_count = 0
                # else:
                #     loop_count += 1
            # else:
            #     loop_count += 1
            if loop_count == 6:
                self.q_s.put(f' dev{dev_index}, mod{mod_index}, sync error;')
                return -1
            loop_count += 1
            time.sleep(1)

    def dvt_thread(self, dev_index):
        for i in range(len(self.testing_strategy)):
            if self.testing_strategy[i][0] == 9999: # debug模式
                frame_dict = {
                    'type': 0x00,
                    'dev_tag': 0x01,
                    'mod_tag': i,
                    'islast_tag': 0x01,
                    'status': 0x00,
                    'mes_tag': 0x000001,
                    'stream_tag': 0x00000001,
                    'content': [0x00, 0x00, 0x00, 0x01]
                }
                if self.start_test(dev_index, i, frame_dict):
                    break
            for j in range(self.testing_strategy[i][0]): # normal模式
                frame_dict = {
                    'type': 0x00,
                    'dev_tag': 0x01,
                    'mod_tag': i,
                    'islast_tag': 0x01,
                    'status': 0x00,
                    'mes_tag': 0x000001,
                    'stream_tag': 0x00000001,
                    'content': [0x00, 0x00, 0x00, 0x00]
                }
                if self.start_test(dev_index, i, frame_dict):
                    break

            if self.testing_strategy[i][0] == 0: # inquire result
                frame_dict = {
                    'type': 0x00,
                    'dev_tag': 0x01,
                    'mod_tag': i,
                    'islast_tag': 0x01,
                    'status': 0x00,
                    'mes_tag': 0x000001,
                    'stream_tag': 0x00000001,
                    'content': [0x00, 0x00, 0x00, 0x02]
                }
                if self.start_test(dev_index, i, frame_dict):
                    break

            print(f'\ndev{dev_index}, mod{i} dvt completed.')
        with self.mutex:
            self.finish_cnt += 1
        print(f'\ndev{dev_index} dvt completed.')

    def run_threads(self):
        thread = threading.Thread(target=self.print_animation)
        thread.start()
        for dev_index in range(self.dev_num):
            thread = threading.Thread(target=self.dvt_thread, args=(dev_index,))
            thread.start()
            self.threads.append(thread)

    def stop_threads(self):
        self.threads = []
        self.stop_print.set()
