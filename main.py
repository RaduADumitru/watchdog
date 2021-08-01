import time
import resource
import psutil
import yaml


resources = {'CORE': resource.RLIMIT_CORE,
             'CPU': resource.RLIMIT_CPU,
             'FSIZE': resource.RLIMIT_FSIZE,
             'DATA': resource.RLIMIT_DATA,
             'STACK': resource.RLIMIT_STACK,
             'RSS': resource.RLIMIT_RSS,
             'NPROC': resource.RLIMIT_NPROC,
             'NOFILE': resource.RLIMIT_NOFILE,
             'OFILE': resource.RLIMIT_OFILE,
             'MEMLOCK': resource.RLIMIT_MEMLOCK,
             'AS': resource.RLIMIT_AS,
             'MSGQUEUE': resource.RLIMIT_MSGQUEUE,
             'NICE': resource.RLIMIT_NICE,
             'RTPRIO': resource.RLIMIT_RTPRIO,
             'RTTIME': resource.RLIMIT_RTTIME,
             'SIGPENDING': resource.RLIMIT_SIGPENDING
             }

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
        if limres in resources.keys():
            value = procs['limits'][p][limres]
            resource.prlimit(pid, resources[limres], (value, value))
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
                if limres in resources.keys():
                    value = procs['limits'][p1.name()][limres]
                    resource.prlimit(pid, resources[limres], (value, value))
    time.sleep(1)
