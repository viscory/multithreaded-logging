import datetime
import multiprocessing as mp

def write(args):
    (filename, text) = args
    with open(filename, 'a') as handle:
        handle.write(text)
        handle.close()

def error_decorator(func):
    def inner(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            print("Logger crashed")
            print(e)
    return inner

class Logger:
    @error_decorator
    def __init__(self, program, logFormat="[{} {}] {}\n", nodate=False):
        self.programName = program
        self.dtObj = datetime.datetime
        self.logFmt = logFormat
        self.currDay = self.dtObj.now().day
        self.logFile = "/tmp/{}#{}.log".format(self.programName, self.dtObj.today().isoformat())
        if nodate:
            self.logFile = "/tmp/{}.log".format(self.programName)

        self.writeProcs = []

    @error_decorator
    def update(self):
        day = self.dtObj.now().day
        if self.currDay != day:
            self.currDay = day
            self.logFile = "/tmp/{}#{}.log".format(self.programName, self.dtObj.today().isoformat())

    @error_decorator
    def info(self, msg):
        self.update()
        text = self.logFmt.format(self.dtObj.now().strftime("%H:%M:%S.%f"), 'INFO', msg)
        self.writeProcs.append(mp.Process(target=write, args=((self.logFile, text), )))
        self.writeProcs[-1].start()

    @error_decorator
    def warn(self, msg):
        self.update()
        text = self.logFmt.format(self.dtObj.now().strftime("%H:%M:%S.%f"), 'WARN', msg)
        self.writeProcs.append(mp.Process(target=write, args=((self.logFile, text), )))
        self.writeProcs[-1].start()

    @error_decorator
    def error(self, msg):
        self.update()
        text = self.logFmt.format(self.dtObj.now().strftime("%H:%M:%S.%f"), 'ERROR', msg)
        self.writeProcs.append(mp.Process(target=write, args=((self.logFile, text), )))
        self.writeProcs[-1].start()

    @error_decorator
    def stop(self, wait=True):
        if wait:
            for proc in self.writeProcs:
                proc.join()
        else:
            for proc in self.writeProcs:
                proc.kill()
