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
            break
    if (path == ''):
        raise ('Process ' + name + ' not found\n')
    p1 = psutil.Process(pid)
    fields = procs['limits'][p].keys()
    for limres in fields:
        value = procs['limits'][p][limres]
        if limres == 'CORE':
            resource.prlimit(pid, resource.RLIMIT_CORE, (value, value))
        elif limres == 'CPU':
            resource.prlimit(pid, resource.RLIMIT_CPU, (value, value))
        elif limres == 'FSIZE':
            resource.prlimit(pid, resource.RLIMIT_FSIZE, (value, value))
        elif limres == 'DATA':
            resource.prlimit(pid, resource.RLIMIT_DATA, (value, value))
        elif limres == 'STACK':
            resource.prlimit(pid, resource.RLIMIT_STACK, (value, value))
        elif limres == 'RSS':
            resource.prlimit(pid, resource.RLIMIT_RSS, (value, value))
        elif limres == 'NPROC':
            resource.prlimit(pid, resource.RLIMIT_NPROC, (value, value))
        elif limres == 'NOFILE':
            resource.prlimit(pid, resource.RLIMIT_NOFILE, (value, value))
        elif limres == 'OFILE':
            resource.prlimit(pid, resource.RLIMIT_OFILE, (value, value))
        elif limres == 'MEMLOCK':
            resource.prlimit(pid, resource.RLIMIT_MEMLOCK, (value, value))
        elif limres == 'AS':
            resource.prlimit(pid, resource.RLIMIT_AS, (value, value))
        elif limres == 'MSGQUEUE':
            resource.prlimit(pid, resource.RLIMIT_MSGQUEUE, (value, value))
        elif limres == 'NICE':
            resource.prlimit(pid, resource.RLIMIT_NICE, (value, value))
        elif limres == 'RTPRIO':
            resource.prlimit(pid, resource.RLIMIT_RTPRIO, (value, value))
        elif limres == 'RTTIME':
            resource.prlimit(pid, resource.RLIMIT_RTTIME, (value, value))
        elif limres == 'SIGPENDING':
            resource.prlimit(pid, resource.RLIMIT_SIGPENDING, (value, value))

while True:
    for pid in pidlist:
        p1 = psutil.Process(pid)
        path = p1.exe()
        if not (p1.is_running()) or (p1.status() == psutil.STATUS_ZOMBIE):  # WIP
            p1 = psutil.Popen(path)
            print('Process ' + p1.name() + ' filepath(' + p1.exe() + ') restarted\n')
            pid = p1.pid()
            fields = procs['limits'][p1.name()].keys()
            for limres in fields:
                value = procs['limits'][p1.name()][limres]
                if limres == 'CORE':
                    resource.prlimit(pid, resource.RLIMIT_CORE, (value, value))
                elif limres == 'CPU':
                    resource.prlimit(pid, resource.RLIMIT_CPU, (value, value))
                elif limres == 'FSIZE':
                    resource.prlimit(pid, resource.RLIMIT_FSIZE, (value, value))
                elif limres == 'DATA':
                    resource.prlimit(pid, resource.RLIMIT_DATA, (value, value))
                elif limres == 'STACK':
                    resource.prlimit(pid, resource.RLIMIT_STACK, (value, value))
                elif limres == 'RSS':
                    resource.prlimit(pid, resource.RLIMIT_RSS, (value, value))
                elif limres == 'NPROC':
                    resource.prlimit(pid, resource.RLIMIT_NPROC, (value, value))
                elif limres == 'NOFILE':
                    resource.prlimit(pid, resource.RLIMIT_NOFILE, (value, value))
                elif limres == 'OFILE':
                    resource.prlimit(pid, resource.RLIMIT_OFILE, (value, value))
                elif limres == 'MEMLOCK':
                    resource.prlimit(pid, resource.RLIMIT_MEMLOCK, (value, value))
                elif limres == 'AS':
                    resource.prlimit(pid, resource.RLIMIT_AS, (value, value))
                elif limres == 'MSGQUEUE':
                    resource.prlimit(pid, resource.RLIMIT_MSGQUEUE, (value, value))
                elif limres == 'NICE':
                    resource.prlimit(pid, resource.RLIMIT_NICE, (value, value))
                elif limres == 'RTPRIO':
                    resource.prlimit(pid, resource.RLIMIT_RTPRIO, (value, value))
                elif limres == 'RTTIME':
                    resource.prlimit(pid, resource.RLIMIT_RTTIME, (value, value))
                elif limres == 'SIGPENDING':
                    resource.prlimit(pid, resource.RLIMIT_SIGPENDING, (value, value))
    time.sleep(1)
