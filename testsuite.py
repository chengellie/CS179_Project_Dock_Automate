from log import Log
from main import create_ship
from datetime import datetime

class TestSuite:
    def __init__(self, manifest, logcase):
        self.manifest = manifest
        self.logcase = logcase
        self.logfile = Log(logcase[:-4])

    """Compare for correctness between produced log file and test log file"""
    def __compare_logs(self) -> [bool, str]:  # TODO: Maybe change to compare # of comments and actual texts written?
        logdata = self.logfile.readlog()
        for (i, j) in zip(self.testlogcase, logdata):
            if i != j:
                return False 
        return True, None

    """Check all container placements are valid"""
    def __check_placement(self) -> [bool, str]:    # TODO: Check valid placement, asymetrical ship (non-container), and output issues
        return False

    """Check ship is balanced left and right"""
    def __check_balance(self) -> [bool, float, float]:  # TODO: Compute total weights, comparison, and printing of weights
        left = 0.0
        right = 0.0
        # TODO: Go through and check left and right to see if actually balanced (Without using isBalanced())
        return False, left, right
        
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

            self.ship = create_ship(self.manifest)   # TODO: Add load, unloads
            # TODO: Run program
            print(f"Time: {(datetime.now() - start_time).total_seconds()}s")

            # Test Log Files
            print("\tLog File:", end=" ")
            with self.compare_logs() as (passed, failline):
                if passed:
                    print("PASSED")
                else:
                    print(f"FAILED: {failline}")

            # Test Ship Balance
            print("\tShip Balancing:", end=" ")
            if self.__check_balance(ship):
                print("PASSED")
            else:
                print("FAILED")

            # Test Ship Outbound (Load/Unload Correctness)
            outboundcase = create_ship(f"{self.manifest}OUTBOUND.txt")

        print("#" * 15)
            
t = TestSuite("shipcasetest.txt", "LogCase1.txt")
t.test(3, "load_unload.txt")

"""
Test Suite 1 - ShipCase1.txt
Offload: [Cat]
    -> Onload: [Bat]
Offload: [Dog]
Onload: [Bird, Bird]
"""
