import datetime
import os
import shutil
import re
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWUSR
# https://www.tutorialspoint.com/How-to-change-the-permission-of-a-file-using-Python
# TODO: Create a retrievable copy. Change visibility of directory

"""
Log class for logging. Will find a log file in designated space and open that. If multiple, choose one with largest year.
If none (or at start of program depending on costumer), ask user if they would like to start a new log year file.
self.filepath = full file path
self.logfile = the log file name
"""
class Log:
    # Private Functions #
    def __init__(self, logname):
        # Testing
        self.filepath = logname
        self.logfile = f"{logname}{self.__append_year(year)}.txt"    # TODO: Change to variable year
        
        file_exists, self.logfile = self.__find_valid_log()
        
        # self.filepath = os.path.expanduser(f"~\Documents\.DockAutomate") # Windows
        # self.filepath = os.path.expanduser(f"~/Documents/.DockAutomate") # MacOS/Linux
        
        
        # if not os.path.exists(self.filepath):
        #     os.mkdir(self.filepath)
        #     os.system(f"attrib +h {self.filepath}")
        
        # # If Log file does not exist, create a new one and set necessary permissions
        # file_exists, self.logfile = self.__find_valid_log(logname)
        # if not file_exists:
        #     print("No file, would you like to create a new one") # TODO: Change to match customer
        #     print("The log file has the logical year appended to its name. What year do you want the log file?")
            
        #     # Create new log file in filepath
        #     self.logfile = f".{logname}2023.txt"    # TODO: Change to variable year
        #     # self.filepath += f"\\{self.logfile}"  # Windows
        #     self.filepath += f"/{self.logfile}" # MacOS/Linux
        #     f = open(self.filepath, "w")
        #     f.close()
            
        #     # Set attributes to protect log file
        #     # os.system(f"attrib +h {self.filepath}")
        #     self.__read_only()
        # else:
        #     # self.filepath += f"\\{self.logfile}"  # Windows
        #     self.filepath += f"/{self.logfile}" # MacOS/Linux
        #     print(self.filepath)
        
    def __write_enable(self):
        os.chmod(self.filepath, S_IWUSR|S_IREAD)
    
    def __read_only(self):
        os.chmod(self.filepath, S_IREAD|S_IRGRP|S_IROTH)
    
    """Search through ~\.DockAutomate directory for a valid Log file"""
    def __find_valid_log(self, logname:str):
        filename = re.compile(f".{logname}\d+.txt")
        for file in os.listdir(self.filepath):
            if filename.fullmatch(file):
                return True, file   # Modify to consider multiple and take largest one
        
        return False, None

    def __append_year(self, year:int): # TODO: May Discard
        if int(year / 10000) == 0:
            self.logyear = year
            return True
        
        return False
        
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

    # Public Functions #
    """write formatted log into log file"""
    def writelog(self, action):
        curr_month = datetime.datetime.now().strftime("%B")
        curr_time = datetime.datetime.now().ctime()[4:].split()[1:]

        self.__write_enable()
        f = open(self.filepath, 'a')
        f.write(f"{curr_month} {self.__day_suffix(int(curr_time[0]))} {curr_time[2]}: {curr_time[1][:-3]} {action}\n")
        self.__read_only()
    
    """write a user comment into log file"""
    def writecomment(self, comment:str):
        self.writelog(f"Comment: {comment}")

    def readlog(self, printlog:bool = False):
        with open(self.filepath, 'r') as logfile:
            logdata = [logline.strip('\n') for logline in logfile.readlines()]
        if printlog:
            for line in logdata:
                print(line)
        
        return logdata
    
# test = Log('')
# test.write_comment('Testing Comment')