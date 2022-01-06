import unittest
import log
import random
import datetime

def lineCount(filename):
    count = 0
    with open(filename, 'r') as h:
        for line in h:
            count += 1
    return count

class testLogger(unittest.TestCase):
    def test_write(self):
        pname = hex(int(random.random()*10000000))
        logger = log.Logger(pname, nodate=True)
        for i in range(10):
            logger.error(str(i))
        logger.stop()
        self.assertEqual(10, lineCount('/tmp/{}.log'.format(pname)))

    def test_stop_wait(self):
        pname = hex(int(random.random()*10000000))
        logger = log.Logger(pname, nodate=True)
        for i in range(100):
            logger.error(str(i))
        logger.stop()
        self.assertEqual(100, lineCount('/tmp/{}.log'.format(pname)))

    def test_stop_immediate(self):
        pname = hex(int(random.random()*10000000))
        logger = log.Logger(pname, nodate=True)
        for i in range(400):
            logger.error(str(i))
        logger.stop(False)
        self.assertGreater(400, lineCount('/tmp/{}.log'.format(pname)))

    def test_midnight(self):
        pname = hex(int(random.random()*10000000))
        logger = log.Logger(pname)
        logger.error("test")
        oldfilename = logger.logFile
        import pdb; pdb.set_trace()
        newdatetime = datetime.datetime.fromtimestamp(datetime.datetime.now().timestamp()+5*24*60*60)
        logger.dtObj = newdatetime
        logger.error("test")
        newfilename = logger.logFile

        self.assertNotEqual(oldfilename, newfilename)

if __name__ == "__main__":
    unittest.main()
