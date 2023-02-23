from ship import Ship
from log import Log
from main import create_ship
from datetime import datetime

class TestSuite:
    def __init__(self, manifest, logcase):
        self.manifest = manifest
        self.logcase = logcase
        self.logfile = Log(logcase[:-4])

    def __compare_logs(self) -> bool:
        logdata = self.logfile.readlog()
        for (i, j) in zip(self.testlogcase, logdata):
            if i != j:
                return False
        return True
        
    def test(self, num_runs, transferlist):
        print("#" * 15)
        print(f"Manifest: {self.manifest}")
        print(f"Transfer List: {transferlist}")
        print("=" * 15)

        with open(self.logcase) as testfile:
            self.testlogcase = [line.strip('\n') for line in testfile.readlines()]
        for run in range(0, num_runs):
            print(f"Test Run {run + 1}")
            start_time = datetime.now()

            ship = create_ship(self.manifest, transferlist)
            # TODO: Run program
            print(f"Time: {(datetime.now() - start_time).total_seconds()}s")

            print("\tLog File:", end=" ")
            if self.__compare_logs():
                print("PASSED")
            else:
                print("FAILED")

            print("\tShip Balancing:", end=" ")
            if ship.is_balanced():
                print("PASSED")
            else:
                print("FAILED")

        print("#" * 15)
            
t = TestSuite("shipcasetest.txt", "LogCase1.txt")
t.test(3, "load_unload.txt")

"""
Test Suite 1 - ShipCase1.txt
Offload: [Cat]
    -> Onload: [Bat]
Offload: [Dog]
Onload: [Bird, Bird]

LogCase1.txt
"""
