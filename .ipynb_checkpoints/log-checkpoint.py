import datetime
import os
import re
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWUSR
# https://www.tutorialspoint.com/How-to-change-the-permission-of-a-file-using-Python

class Log:
    # Private Functions #
    def __init__(self, logname):
        self.logfile = f".{logname}.txt"
        self.filepath = os.path.expanduser(f"~\Documents\.DockAutomate") # Windows
        # = os.path.expanduser(f"~/Documents/.DockAutomate/.{logname}") # MacOS/Linux
        
        if not os.path.exists(self.filepath):
            os.mkdir(self.filepath)
            os.system(f"attrib +h {self.filepath}")
        
        """If Log file does not exist, create a new one and set necessary permissions"""
        if not self.__find_valid_log(logname):
            print("No file, would you like to create a new one") # Change to match customer
            print("The log file has the logical year appended to its name. What year do you want the log file?")
            
            self.filepath += f"\\{self.logfile}"
            f = open(self.filepath, "w")
            f.close()
            
            # Set attributes to protect log file
            os.system(f"attrib +h {self.filepath}")
            self.__read_only()
        
    def __write_enable(self):
        os.chmod(self.filepath, S_IWUSR|S_IREAD)
    
    def __read_only(self):
        os.chmod(self.filepath, S_IREAD|S_IRGRP|S_IROTH)
    
    """Search through ~\.DockAutomate directory for a valid Log file"""
    def __find_valid_log(self, logname:str):
        filename = re.compile(f".{logname}\d+.txt")
        for file in os.listdir(self.filepath):
            if filename.fullmatch(file):
                return True
        
        return False

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
        self.__write_enable()
        curr_month = datetime.datetime.now().strftime("%B")
        curr_time = datetime.datetime.now().ctime()[4:].split()[1:]
        print(f"{curr_month} {self.__day_suffix(int(curr_time[0]))} {curr_time[2]}: {curr_time[1][:-3]} {action}")
        self.__read_only()
    
    # write a user comment into log file
    def writecomment(self, comment:str):
        self.write_log(f"Comment: {comment}")
    
# test = Log('')
# test.write_comment('Testing Comment')