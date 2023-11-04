from Modules.com import *
from Modules.log import *
from Modules.result import *
from Modules.interaction import *
from colorama import init, Fore
import queue

hosts_info = {}
devices_info = {
    'dev_name': 'C1-core',
    'dev_num': 3,
    'module_num': 3,
    'IP': '192.168.140.1',
    'testing strategy': {
        0x00: [1, 'parallelable'],     # list第一个元素为0，则为查询结果模式
        0x02: [3, 'unparallelable'],
        0x01: [3, 'unparallelable']
    }

}


def init_dvt_sys(info):
    dev_name = devices_info['dev_name']
    dev_num = devices_info['dev_num']
    mod_num = devices_info['module_num']
    ip = devices_info['IP']
    port = 8080
    strategy = devices_info['testing strategy']
    qm = []
    for x in range(dev_num):
        qm.append(QueueManager())
    q_inquire = queue.Queue()

    com = []
    log = []
    for x in range(dev_num):
        log.append(LogProcess(qm[x], dev_name + str(x)))
        com.append(ClientTcp(ip, port + x, qm[x]))

    for x in range(dev_num):
        log[x].start()
    for x in range(dev_num):
        com[x].connect()
        com[x].start_recv_thread()
        com[x].start_process_frame()

    res = ResultMaintainer(dev_name, dev_num, mod_num, qm, q_inquire)
    res.create_result_dict()
    res.run_threads()

    time.sleep(5)
    inter = Interaction(dev_name, dev_num, strategy, com, qm, q_inquire)
    inter.run_threads()

    while True:
        if inter.finish_cnt == dev_num:
            time.sleep(5)
            inter.stop_threads()
            print('\ndvt finish, please check result.')
            break


if __name__ == '__main__':
    # init()
    init_dvt_sys(devices_info)
