from log import Log
# from main import create_ship
from datetime import datetime
from ship import Ship
import copy
import shiputil

class TestSuite:
    def __init__(self, manifest, logcase):
        self.manifest = manifest
        self.logcase = logcase
        self.logfile = Log(logcase[:-4])
        self.ship = create_ship(self.manifest)   # TODO: Add load, unloads
        self.columns = self.ship.get_ship_columns() # get columns of ship
        # TODO: Run program

    """Compare for correctness between produced log file and test log file"""
    def compare_logs(self) -> [bool, str]:  # TODO: Maybe change to compare # of comments and actual texts written?
        logdata = self.logfile.readlog()
        for (i, j) in zip(self.testlogcase, logdata):
            if i != j:
                return False 
        return True, None

    """Check all container placements are valid"""
    def check_placement(self) -> [bool, str]:    # TODO: Check valid placement, asymetrical ship (non-container), and output issues
        return False

    """Check ship is balanced left and right"""
    def check_balance(self) -> [bool, float, float]:  # TODO: Compute total weights, comparison, and printing of weights
        left = 0.0
        right = 0.0

        for col in zip(self.columns[:len(self.columns)//2], self.columns[len(self.columns)//2:]):
            left += sum([c.weight for c in col[0]])
            right += sum([c.weight for c in col[1]])

        if min(left, right) >= max(left, right) * 0.9:
            return True, left, right
        # TODO: Go through and check left and right to see if actually balanced (Without using isBalanced())
        return False, left, right
        
    def test(self, num_runs:int=3):
        print("#" * 15)
        print(f"Manifest: {self.manifest}")
        print(f"Transfer List: {transferlist}")
        print("=" * 15)

        with open(self.logcase) as testfile:
            self.testlogcase = [line.strip('\n') for line in testfile.readlines()]
        for run in range(0, num_runs):
            print(f"Test Run {run + 1}")
            start_time = datetime.now()
            # Test to solve
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
            with self.check_balance(ship) as [balanced, left, right]:
                if balanced:
                    print("PASSED")
                else:
                    print(f"FAILED -> {left} {right}: ")

            # Test Ship Outbound (Load/Unload Correctness)
            outboundcase = create_ship(f"{self.manifest}OUTBOUND.txt")

        print("#" * 15)
            
# t = TestSuite("shipcasetest.txt", "LogCase1.txt")
# t.test(3, "load_unload.txt")

"""
Auxiliary Testing - All Functions
"""

s = shiputil.create_ship(
        "ShipCase/ShipCase4.txt",
        "load_unload.txt",
        "OUTBOUNDShipCase/OUTBOUNDshipcasetest.txt",
    )

a = copy.deepcopy(s)
# a = Ship(s.ship_state, ["Bird"], ['Cat', 'Cat'])
print(a)
print(a.top_columns)
print(a.cntrs_in_row[6])

# Add a container
print("============================== Add Cat")
test_cntr = a.ship_state[6][4]
print(a.cntrs_in_row[5])
a.add_cntr(copy.deepcopy(test_cntr), 11)
print(a)
print(a.top_columns)
print(a.cntrs_in_row[6])

# Remove a container
print("============================== Remove 4 Containers From Col 4")
for i in range(0, 4):
    rm_cntr = a.remove_cntr(4)

    print(f"Removed {rm_cntr}")

print(a)
print(a.top_columns)
print(a.cntrs_in_row[4])
print(a.get_container_depth(test_cntr))
# test_cntr = a.find_best_cntr(test_cntr)
# print(test_cntr)
# print(test_cntr.ship_coord)
# print(s.ship_state[7][1].ship_coord)
# print(a.goal_state)
# Log("")

# t = TestSuite("OUTBOUNDShipCase/OUTBOUNDshipcasetest.txt", "LogCase/LogCase1.txt")

# leftWeight = 0
# rightWeight = 0
# for col in zip(columns[:len(columns)//2], columns[len(columns)//2:]):
#     leftWeight += sum([c.weight for c in col[0]])
#     rightWeight += sum([c.weight for c in col[1]])
# print(leftWeight, rightWeight)

"""
Test Suite 0.1 - shipcasetest.txt
Offload: [Cat]
    -> Onload: [Bat]
Offload: [Dog]
Onload: [Bird, Bird]
"""

"""
Test Suite 0.2 - shipcasetest2.txt
Offload: [Cat]
    -> Onload: [Bat]
Offload: [Dog]
Onload: [Bird, Bird]
"""

"""
Test Suite 1 - ShipCase1.txt
Offload: [Cat]
    -> Onload: [Bat]
Offload: [Dog]
Onload: [Bird, Bird]
"""

"""
Test Suite 2 - ShipCase2.txt
Offload: [Cat]
    -> Onload: [Bat]
Offload: [Dog]
Onload: [Bird, Bird]
"""

