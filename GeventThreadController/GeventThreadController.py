from threading import Thread
from gevent import Greenlet
from gevent.pool import Group
import gevent
import queue


class GeventThreadController(Thread):
    def __init__(self, name, sleep=0.2, debug=False):
        Thread.__init__(self)
        self.name = name
        self._q_wait_to_run = queue.Queue()
        self._q_wait_to_stop = queue.Queue()
        self._is_stop = False
        self._greenlets = Group()
        self._sleep = sleep
        self._isdebug = debug

    def run(self):
        self._is_stop = False
        self._debug("{} start".format(self.name))
        while not self._is_stop:
            if not self._q_wait_to_stop.empty():
                self._stop_greenlet(self._q_wait_to_stop.get())
            elif not self._q_wait_to_run.empty():
                self._start_greenlet(self._q_wait_to_run.get())
            else:
                gevent.sleep(self._sleep)
        # Stoping thread
        self._greenlets.kill()
        self._debug("{} stop".format(self.name))

    def stop(self):
        self.stop_nowait()
        self.join()

    def stop_nowait(self):
        self._is_stop = True

    def append(self, name, green_create_task, *args, **kwargs):
        if hasattr(green_create_task, '__call__'):
            self._q_wait_to_run.put(tuple((name, green_create_task, args, kwargs)))
        else:
            raise TypeError("must be \'function\' or  \'GreenClassPack\', not {}".format(type(green_create_task)))
    def stop_greenlet(self, gr_mame):
        self._q_wait_to_stop.put(gr_mame)

    def __getitem__(self, gr_mame):
        gr_obj = self._get_greenlet(gr_mame)
        if gr_obj:
            return gr_obj
        raise IndexError

    def _start_greenlet(self, gr_create_task_tuple):
        gr_task_name = gr_create_task_tuple[0]
        gr_create_task = gr_create_task_tuple[1]
        args = gr_create_task_tuple[2]
        kwargs = gr_create_task_tuple[3]
        gr_obj = gr_create_task(*args, **kwargs)
        if isinstance(gr_obj, Greenlet) and not self._get_greenlet(gr_task_name):
            gevent.spawn(self._task_hndler, gr_obj, gr_task_name)
        else:
            self._debug("Error form {0}.{1}: must be \'gevent.Greenlet\', not {2}. Or same greenlet already runnig"
                        .format(self.name, gr_task_name, type(gr_obj)))

    def _stop_greenlet(self, gr_task_name):
        gr_obj = self._get_greenlet(gr_task_name)
        if gr_obj:
            gr_obj.kill()

    def _get_greenlet(self, name_str):
        gr_name = "{0}.{1}".format(self.name, name_str)
        for gr_obj in self._greenlets:
            if gr_name == gr_obj.name:
                return gr_obj
        return None

    def _task_hndler(self, gr_obj, gr_name):
        gr_obj.name = "{0}.{1}".format(self.name, gr_name)
        self._greenlets.add(gr_obj)
        self._debug("{0}.{1}: starting".format(self.name, gr_name))
        gr_obj.start()
        gr_obj.join()
        self._greenlets.discard(gr_obj)
        self._debug("{0}.{1} is stop".format(self.name, gr_name))

    def _debug(self, log_str):
        if self._isdebug:
            print(log_str)


if __name__ == "__main__":
    import time
    from gevent.event import AsyncResult

    # 1. Building class of Greenlet
    class GrModule(Greenlet):
        def __init__(self):
            Greenlet.__init__(self)

        def _run(self):
            for i in range(5):
                print("{0}: {1}".format(self.name, i))
                gevent.sleep(2)

    class GrLoop(Greenlet):
        def __init__(self, evt_stop):
            Greenlet.__init__(self)
            self._evt_stop = evt_stop

        def _run(self):
            i = 0
            while True:
                try:
                    self._evt_stop.get(timeout=1)
                    break
                except gevent.timeout.Timeout:
                    print("{0}: {1}".format(self.name, i))
                    i += 1

        def test(self):
            print("{0}: Test ok".format(self.name))

    # 2. Create and run a threads
    '''
    GeventThreadController have a params: 
        name - name of module run in new thread 
        sleep=0.2 - pause in control cycle, define delay before Greenlets start and stop. 
                    Value = 0 will be load a processor/ 
        debug=False - print debugging message
    '''

    thread1 = GeventThreadController("First", debug=False)
    thread1.start()
    thread2 = GeventThreadController("Second", debug=False)
    thread2.start()

    # 3. Add tasks and run
    evt_stop = AsyncResult()
    for i in range(5):
        thread1.append("G{}".format(i), GrModule)
        thread2.append("G{}".format(i), GrLoop, evt_stop)

    # 4. Control tasks
    time.sleep(2)
    evt_stop.set(True)
    thread1.stop_greenlet("G4")
    thread2["G2"].test()

    time.sleep(6)
    thread1.stop_nowait()
    thread2.stop()
