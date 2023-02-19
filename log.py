import datetime
import os
# https://docs.python.org/3/library/os.html#os.setxattr

class Log:
    def __init__(self, logname):
        # self.logfile = f".{logname}{year}
        print(os.path.expanduser(f"~/Documents/.{logname}"))    # Testing: MacOS
        # print(os.path.expanduser(f"~\Documents\.{logname}"))    # Testing: Windows

    # append a suffix to day
    def __day_suffix(self, day:int):
        if day % 10 == 1 and int(day / 10) != 1:
            return f"{day}st"
        elif day % 10 == 2 and int(day / 10) != 1:
            return f"{day}nd"
        elif day % 10 == 3 and int(day / 10) != 1:
            return f"{day}rd"
        else:
            return f"{day}th"

    # write formatted log into log file 
    def writelog(self, action):
        curr_month = datetime.datetime.now().strftime("%B")
        curr_time = datetime.datetime.now().ctime()[4:].split()[1:]
        print(f"{curr_month} {self.__day_suffix(int(curr_time[0]))} {curr_time[2]}: {curr_time[1][:-3]} {action}")
    
    # write a user comment into log file
    def writecomment(self, comment:str):
        self.write_log(f"Comment: {comment}")
    
# test = Log('')
# test.write_comment('Testing Comment')