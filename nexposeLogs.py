from datetime import datetime

class LOG:
    def __init__(self, file):
        self.file = file
        self.file.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " Logging started\n")
        return
    
    def writeLog(self, msg):
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.file.write(time + " " + msg + "\n")
        