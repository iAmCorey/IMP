# -*- coding: utf-8 -*-
# written by mark zeng 2018-11-14
from multiprocessing import Process, Queue
import time
import sys
import numpy as np

N=10000

class Worker(Process):
    def __init__(self, inQ, outQ, random_seed):
        super(Worker, self).__init__(target=self.start)
        self.inQ = inQ
        self.outQ = outQ
        # 如果子进程的任务是有随机性的，一定要给每个子进程不同的随机数种子，否则就在重复相同的结果了
        np.random.seed(random_seed)

    def run(self):
        while True:
            task = self.inQ.get()  # 取出任务， 如果队列为空， 这一步会阻塞直到队列有元素
            res = 0
            for i in range(100):
                res += i
            self.outQ.put(res)

def create_worker(num,worker):
    for i in range(num):
        worker.append(Worker(Queue(), Queue(), np.random.randint(0, 10 ** 9)))
        worker[i].start()


def finish_worker(worker):
    for w in worker:
        w.terminate()


if __name__ == '__main__':
    now = time.time()
    worker = []
    worker_num = 8
    create_worker(worker_num,worker)
    for i in range(N):
        worker[i % worker_num].inQ.put(i)
    result = 0
    for i in range(N):
        print(i)
        result += worker[i % worker_num].inQ.get()
    print(result)
    finish_worker(worker)
    print(time.time()- now)
