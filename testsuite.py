from log import Log
# from main import create_ship
from datetime import datetime
from ship import Ship
import copy
import shiputil
import search
from container import Container
from random import choices

# TODO: Output to a testlog_id

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

print(
"""
#######################################
Auxiliary Testing - All Functionalities
#######################################
"""
)
# Loading a Manifest to Build Ship From Scratch and Adding Containers
print("============================== Loading a Manifest to Build a Ship From Scratch by Adding Containers")
scratch_ship = shiputil.create_ship(
        "ShipCase/emptyship.txt",
        "load_unload.txt",
        "OUTBOUNDShipCase/OUTBOUNDshipcasetest.txt",
    )
scratch_ship.add_cntr(Container([-1,-1], 50, "Cat", [scratch_ship.row, scratch_ship.col]), 0)
scratch_ship.add_cntr(Container([-1,-1], 50, "Cat", [scratch_ship.row, scratch_ship.col]), 1)
scratch_ship.add_cntr(Container([-1,-1], 75, "Dog", [scratch_ship.row, scratch_ship.col]), 0)
scratch_ship.add_cntr(Container([-1,-1], 50, "Cat", [scratch_ship.row, scratch_ship.col]), 0)
scratch_ship.add_cntr(Container([-1,-1], 25, "Rat", [scratch_ship.row, scratch_ship.col]), 0)
scratch_ship.add_cntr(Container([-1,-1], 50, "Cat", [scratch_ship.row, scratch_ship.col]), 3)
scratch_ship.add_cntr(Container([-1,-1], 75, "Dog", [scratch_ship.row, scratch_ship.col]), 4)
scratch_ship.add_cntr(Container([-1,-1], 100, "Emu", [scratch_ship.row, scratch_ship.col]), 3)
scratch_ship.add_cntr(Container([-1,-1], 300, "Elephant", [scratch_ship.row, scratch_ship.col]), 3)
scratch_ship.add_cntr(Container([-1,-1], 50, "Cat", [scratch_ship.row, scratch_ship.col]), 5)
scratch_ship.add_cntr(Container([-1,-1], 50, "Cat", [scratch_ship.row, scratch_ship.col]), 5)
scratch_ship.add_cntr(Container([-1,-1], 50, "Cat", [scratch_ship.row, scratch_ship.col]), 5)
scratch_ship.add_cntr(Container([-1,-1], 50, "Cat", [scratch_ship.row, scratch_ship.col]), 5)
scratch_ship.add_cntr(Container([-1,-1], 30, "Bird", [scratch_ship.row, scratch_ship.col]), 5)

print(scratch_ship)

# Remove a container
print("============================== Remove 4 Containers From Col 4")
for i in range(0, 4):
    rm_cntr = scratch_ship.remove_cntr(4)

    print(f"Removed {rm_cntr}")

print(scratch_ship)
print(scratch_ship.top_columns)
print(scratch_ship.cntrs_in_row[4])

# Find Best Cat Container
print("============================== Finding 4 Best Cat Containers")
def setup_cntr(coord:list):
    cntr = scratch_ship.get_cntr(coord)
    cntr.selected = True
    return cntr

def get_best_cntr(cntr:Container):
    return scratch_ship.find_best_cntr(cntr)

test_cntrs = [setup_cntr(cntr_coord) for cntr_coord in [[5, 0], [7, 1], [7, 0], [6, 5]]]
test_cntrs = [get_best_cntr(cntr) for cntr in test_cntrs]
[print(cntr.get_cntr_info()) for cntr in test_cntrs]

print("============================== Get Moves for Each Cat Container")
for cntr in test_cntrs:
    moves = scratch_ship.get_moves(cntr.ship_coord, scratch_ship.get_col_top_empty_coord(2))
    print(moves)
print("============================== Move Crane")
print("============================== Set Heuristics")


# unloads = [[6, 4], [4,4]]
# loads = [Container([-1, -1], i, f"Test {i}", [scratch_ship.row, scratch_ship.col]) for i in range(0, 4)]
# search.load_unload(a, unloads=unloads)
# for cntr in unloads:
#     print(cntr.ship_coord)
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

# s = shiputil.create_ship(
#         "ShipCase/ShipCase1.txt",
#         "load_unload.txt",
#         "OUTBOUNDShipCase/OUTBOUNDshipcasetest.txt",
#     )
# t = s.ship_state[7][1]
# for i in range(0, 10):
#     s.add_cntr(t, 1)
# print(s)
# print(s.top_columns)
# s.remove_cntr(0)
# print(s)