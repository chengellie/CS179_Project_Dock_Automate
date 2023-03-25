from datetime import datetime
import os
import shutil
import re
import json
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
    def __init__(self):
        self.debug_flags = [False, False, False]    # directory had to be created, log config had to be created, log file had to be created
        # self.filepath = os.getcwd() + f"\DockAutomate"   # Testing  Windows
        # self.filepath = os.path.expanduser(f"~\Documents\DockAutomate") # Windows
        self.filepath = os.getcwd() + f"\DockAutomate"   # Testing MacOS/Linux
        # self.filepath = os.path.expanduser(f"~/Documents/DockAutomate") # MacOS/Linux
        if not os.path.exists(self.filepath):
            os.mkdir(self.filepath)
            # os.system(f"attrib +h {self.filepath}")
            self.debug_flags[0] = True
        self.jsonfile = self.filepath + "\.log_config.json"

        json_found, tmp_file = self.__find_valid_files(".log_config.json")
        if not json_found:
            # Initialize json
            print("Creating Log Config")
            with open(self.jsonfile, "w") as config_file:
                config_obj = json.dumps({
                                            "name": "activitylog",                                      # name of log files (w/o year)
                                            "year": None,                                               # year for file we're working on
                                            "init-date": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),  # init date for records
                                            "new": True                                                  # lines for seeking to last line of log
                                        }, indent=4)
                config_file.write(config_obj)
            self.debug_flags[1] = True
            # os.system(f"attrib +h {self.jsonfile}")
        
        # Read json
        with open(self.jsonfile, 'r') as config_file:
            log_config = json.load(config_file)
            self.name = log_config['name']
            self.year = log_config['year']
            self.init_date = log_config['init-date']
            self.new = log_config['new']
        
        # Search to see if there is a valid log file that exists
        if self.year is None:
            self.valid_log, self.logname = self.__find_valid_files(f"{self.name}\d+.txt")
            if self.valid_log:
                self.year = int(self.logname[-8:-4])
                self.__update_json()
        else:
            self.valid_log, self.logname = self.__find_valid_files(f"{self.name}{self.year}.txt")

        self.logfile = ""
    
    """Search through ~\.DockAutomate directory for a valid Log file"""
    def __find_valid_files(self, filename:str):
        re_filename = re.compile(filename)
        for file in os.listdir(self.filepath):
            if re_filename.fullmatch(file):
                return True, file

        return False, None

    def __update_json(self):
        with open(self.jsonfile, "r+") as config_file:
            config_obj = json.dumps({
                                        "name": self.name,                                      # name of log files (w/o year)
                                        "year": self.year,                                               # year for file we're working on
                                        "init-date": self.init_date,  # init date for records
                                        "new": self.new                                                  # lines for seeking to last line of log
                                    }, indent=4)
            config_file.write(config_obj)
        
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
        with open(self.logfile, 'a') as logfile:
            if logfile.closed:
                return False

            curr_month = datetime.now().strftime("%B")
            curr_time = datetime.now().ctime()[4:].split()[1:]

            logfile.write(f"{curr_month} {self.__day_suffix(int(curr_time[0]))} {curr_time[2]}: {curr_time[1][:-3]} {action}\n")
        self.new = False
        self.__update_json()

        return True
    
    """write a user comment into log file"""
    def writecomment(self, comment:str):
        comment = comment.replace('\n', ' ')
        return self.writelog(f"Comment: {comment.strip()}")

    def create_log_file(self, year:int):
        if self.valid_log:
            self.logfile = self.logfile[:-4] + "backup.txt"
        self.logfile = f"{self.filepath}\\{self.name}{year}.txt"
        self.new = True
        with open(self.logfile, 'ab+') as logfile:
            pass
        # TODO: Check if there's already a log present. If there is, turn it into a backup that can't be detected by Log
        self.year = year
        self.__update_json()
        self.debug_flags[2] = True

    def open_log_file(self) -> int:
        if not self.valid_log:  # no valid log files -> create a new one
            return 0
        self.logfile = self.filepath + f"\\{self.logname}"

        # if not self.new:
        #     with open(self.logfile, 'ab+') as logfile:
        #         logfile.seek(-2, 2)    # initial seek behind first line
        #         while logfile.read(1) != b'\n':
        #             logfile.seek(-2, 1)
        #         last_action = logfile.readline().decode()
                
        #         if "Moved" in last_action or "Offload" in last_action or "Onload" in last_action:   # was in the middle of an operation list
        #             return 2    # operation list interruption detected -> resync

        return 1    # normal -> do nothing