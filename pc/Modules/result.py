from Modules.frame import *
import threading
import json
import time
import os
from datetime import datetime


class ResultMaintainer:
    def __init__(self, name, dev_num, mod_num, queue_manager, queue_inquire):
        self.dev_name = name
        self.dev_num = dev_num
        self.mod_num = mod_num
        self.q_m = queue_manager
        self.q_i = queue_inquire
        self.result = {}
        self.mutex = threading.Lock()
        self.threads = []
        self.stop_update = threading.Event()

    def create_result_dict(self):
        self.result = {
            f"dev{i}": {
                hex(j): {'success_times': 0, 'failure_times': 0, 'error_case': []}
                for j in range(self.mod_num)
            }
            for i in range(self.dev_num)
        }

    def update_result(self, frame, dev_index):
        frame_tmp = FrameDVT()
        frame_tmp.parse_frame(frame)
        if frame_tmp.f_content_len == 12:
            with self.mutex:
                self.result['dev' + str(dev_index)][hex(dev_index)]['success_times'] += 1
        else:
            dword = []
            for x in range(3):
                dw = 0
                for y in range(4):
                    dw |= frame_tmp.f_content[4 * x + y] << (3 - y) * 8
                dword.append(dw)
            n = dword[1] // 8 if dword[1] % 8 == 0 else (dword[1] // 8) + 1
            case_group = []
            for x in range(n):
                case_group.append(frame_tmp.f_content[4 * 3 + x])
            with self.mutex:
                self.result['dev' + str(dev_index)][hex(frame_tmp.f_mod_tag)]['failure_times'] += 1
                if len(self.result['dev' + str(dev_index)][hex(frame_tmp.f_mod_tag)]['error_case']):
                    for x in range(n):
                        self.result['dev' + str(dev_index)][hex(frame_tmp.f_mod_tag)]['error_case'][x] = \
                            bin(int(self.result['dev' + str(dev_index)][hex(frame_tmp.f_mod_tag)]['error_case'][x], 2) \
                                | case_group[x])
                else:
                    for x in range(n):
                        self.result['dev' + str(dev_index)][hex(frame_tmp.f_mod_tag)]['error_case'].append(bin(case_group[x]))

    def run_threads(self):
        for dev_index in range(self.dev_num):
            queue = self.q_m[dev_index].get_queue1()
            thread = threading.Thread(target=self.process_queue, args=(queue, dev_index))
            thread.start()
            self.threads.append(thread)
        thread = threading.Thread(target=self.update_to_file)
        thread.start()

    def process_queue(self, queue, dev_index):
        while True:
            frame = queue.get()
            if frame is None:
                break
            self.update_result(frame, dev_index)

    def stop_threads(self):
        for _ in range(self.dev_num):
            self.q_m.put(None)
        for thread in self.threads:
            thread.join()
        self.threads = []
        self.stop_update.set()

    def update_to_file(self):
        timer = time.time() + 10  # 10秒更新一次
        # 获取当前时间
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        # 构建文件名
        file_name = current_time + self.dev_name + "_result.txt"
        # 构建文件路径
        os.makedirs(self.dev_name + "_dvt_result", exist_ok=True)
        file_path = os.path.join(self.dev_name + "_dvt_result", file_name)
        while not self.stop_update.is_set():
            time.sleep(max(0, timer - time.time()))
            with open(file_path, 'w') as file:
                with self.mutex:
                    json.dump(self.result, file, indent=4)
            timer += 10

# if __name__ == '__main__':
#     rm = ResultMaintainer(name=None, dev_num=16, mod_num=10, queue_manager=None, queue_inquire=None)
#     rm.create_result_dict()
#     print(rm.result)
