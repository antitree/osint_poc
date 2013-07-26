import threading
import Queue


class BaseThread(threading.Thread):
    def __init__(self, func, inq, outq=None):
        threading.Thread.__init__(self)
        self.inq = inq
        self.outq = outq
        self.func = func

    def run(self):
        while True:
            # Do somet shit
            something = self.inq.get()
            result = self.func(something)
            if self.outq is not None:
                self.outq.put(result)
            self.inq.task_done()


def queueup(data, collect, classify, thread_num):
    """
    Class to automatically setup the queuing and threading for your function.

    Example usage:
    - create a collection function that returns a value (collect)
    - create a classification function that returns a value (classi)
    - have some list of data (urls)

    queueup(urls, collect, classi, 5)

    """
    collq = Queue.Queue()
    classq = Queue.Queue()

    for i in range(thread_num):
        collt = BaseThread(collect, collq, classq)
        collt.setDaemon(True)
        collt.start()

    for d in data:
        collq.put(d)

    for i in range(thread_num):
        classt = BaseThread(classify, classq)
        classt.setDaemon(True)
        classt.start()

    # TODO add output/reporting thread

    collq.join()
    classq.join()
