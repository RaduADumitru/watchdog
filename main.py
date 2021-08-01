import time
import resource
import psutil
import yaml


f = open('config.yaml', 'r')
procs = yaml.load(f, Loader=yaml.FullLoader)
f.close()
pidlist = []
for p in procs['limits'].keys():
    name = p
    pid = ''
    path = ''
    for proc in psutil.process_iter():
        if name in proc.name():
            pid = proc.pid
            path = proc.exe()
            pidlist.append(pid)
    if path == '':
        raise ('Process ' + name + ' not found\n')
    p1 = psutil.Process(pid)
    fields = procs['limits'][p].keys()
    for limres in fields:
        value = procs['limits'][p][limres]
        exec('resource.prlimit(pid, resource.RLIMIT_' + limres + ', (value, value))')
while True:
    for pid in pidlist:
        p1 = psutil.Process(pid)
        path = p1.exe()
        if not (p1.is_running()) or (p1.status() == psutil.STATUS_ZOMBIE):
            p1 = psutil.Popen(path)
            print('Process ' + p1.name() + ' filepath(' + p1.exe() + ') restarted\n')
            pid = p1.pid()
            fields = procs['limits'][p1.name()].keys()
            for limres in fields:
                value = procs['limits'][p1.name()][limres]
                exec('resource.prlimit(pid, resource.RLIMIT_' + limres + ', (value, value))')
    time.sleep(1)
