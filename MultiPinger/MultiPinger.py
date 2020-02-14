#!/usr/bin/python
import os
import multiprocessing
import subprocess
from datetime import datetime
from time import sleep


class MultiPinger:
    def __init__(self, host_list, iteration_sleep=0.5, ping_timeout=2, ping_attempts=2, show_success=False, show_failed=True):
        self._host_list = host_list
        self._sleep = iteration_sleep
        self._ping_timeout = str(ping_timeout)
        self._ping_attempts = str(ping_attempts)
        self._show_success = show_success
        self._show_failed = show_failed
        self._DNULL = open(os.devnull, 'w')

    def start(self):
        try:
            while True:
                success, failed = self._worker()
                time = datetime.now().strftime("%H:%M:%S %d-%m-%Y")
                if self._show_failed:
                    for host in failed:
                        print("{0} host {1}\tis down".format(time, host))
                if self._show_success:
                    for host in success:
                        print("{0} host {1}\tis up".format(time, host))
                sleep(self._sleep)
        except KeyboardInterrupt:
            print("Exit")

    def _worker(self):
        mp_queue = multiprocessing.Queue()
        processes = []
        for device in self._host_list:
            p = multiprocessing.Process(target=self._ping, args=(device, mp_queue))
            processes.append(p)
            p.start()
        for p in processes:
            p.join()
        results = {True: [], False: []}
        for p in processes:
            key, value = mp_queue.get()
            results[key] += [value]
        return results[True], results[False]

    def _ping(self, host, mp_queue):
        response = subprocess.call(["ping", "-c", self._ping_attempts, "-w", self._ping_timeout, host], stdout=self._DNULL)
        if response == 0:
            result = True  # host is up
        else:
            result = False  # host is down
        mp_queue.put((result, host))


if __name__ == "__main__":
    devices = ['192.168.10.1', '172.22.3.3', '172.22.3.4', '172.22.3.5', '172.22.3.6', '172.22.3.7', '172.22.3.8']
    pinger = MultiPinger(devices)
    pinger.start()

