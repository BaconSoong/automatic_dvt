import queue


class QueueManager(object):
    def __init__(self):
        self.queue1 = queue.Queue()
        self.queue2 = queue.Queue()
        self.queue3 = queue.Queue()
        # self.queue4 = queue.Queue()

    def get_queue1(self):
        return self.queue1

    def get_queue2(self):
        return self.queue2

    def get_queue3(self):
        return self.queue3

    # def get_queue4(self):
    #     return self.queue4
