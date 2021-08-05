import time
import resource
import psutil
import yaml


f = open('config.yaml', 'r')
procs = yaml.load(f, Loader=yaml.FullLoader)
f.close()
pidlist = []  # list of PIDs of monitored processes
for p in procs['limits'].keys():
    name = p
    pid = ''
    path = ''
    for proc in psutil.process_iter():  # check if process is running
        if name in proc.name():  # if so, get PID and path and add process to list
            pid = proc.pid
            path = proc.exe()
            pidlist.append(pid)
    if path == '':
        raise ('Process ' + name + ' not found\n')
    fields = procs['limits'][name].keys()  # resources limited
    for limres in fields:  # apply limit for each given resource
        value = procs['limits'][name][limres]
        exec('resource.prlimit(pid, resource.RLIMIT_' + limres + ', (value, value))')
while True:
    for pid in pidlist:  # check if each process in list is running, if not then restart it
        p1 = psutil.Process(pid)
        path = p1.exe()
        if not (p1.is_running()) or (p1.status() == psutil.STATUS_ZOMBIE):
            # zombie process will be seen as running by is_running()
            p1 = psutil.Popen(path)
            print('Process ' + p1.name() + ' (filepath' + p1.exe() + ') restarted\n')
            pid = p1.pid()  # update PID because it changes, restarted process is counted as new process
            fields = procs['limits'][p1.name()].keys()  # apply limits again
            for limres in fields:
                value = procs['limits'][p1.name()][limres]
                exec('resource.prlimit(pid, resource.RLIMIT_' + limres + ', (value, value))')
    time.sleep(1)
