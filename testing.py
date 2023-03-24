from log import Log
from datetime import datetime
from ship import Ship
import copy
import util
import search
import csv
from container import Container
from random import choices

manifest = "ShipCase/emptyship.txt"
# op_filename = "data/action_list.csv"
op_filename = "data/aux_action_list.csv"

test_log_file_path = "TestingLogs/"
test_log_file = open(test_log_file_path + "AuxTest.txt", 'w')
test_log_file.write(
"""#######################################
Auxiliary Testing - All Functionalities
#######################################
"""
)
# Loading a Manifest to Build Ship From Scratch and Adding Containers
test_log_file.write("============================== Loading a Manifest to Build a Ship From Scratch by Adding Containers\n")
scratch_ship = util.create_ship(manifest)

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

test_log_file.write(f"{scratch_ship}")

# Remove a container
test_log_file.write("============================== Remove 4 Containers From Col 4\n")
for i in range(0, 4):
    rm_cntr = scratch_ship.remove_cntr(4)
    test_log_file.write(f"Removed {rm_cntr}\n")

test_log_file.write(f"{scratch_ship}")
test_log_file.write(f"{scratch_ship.top_columns}")
[test_log_file.write(f"{row}") for row in scratch_ship.cntrs_in_row]

test_log_file.write("============================== Unpack Container Actions\n")
loads, unloads = util.unpack_actions(scratch_ship, op_filename, scratch_ship.row, scratch_ship.col)
test_log_file.write("--------- Unloads\n")
[test_log_file.write(u.get_cntr_info() + "\n") for u in unloads]
test_log_file.write("--------- Loads\n")
[test_log_file.write(l.get_cntr_info() + "\n") for l in loads]

test_log_file.write("============================== Find Best Containers for Unpacked Actions\n")
unload_cntrs = [scratch_ship.find_best_cntr(cntr) for cntr in unloads]
[test_log_file.write(cntr.get_cntr_info() + "\n") for cntr in unload_cntrs]

test_log_file.write("============================== Initializing Log File\n")
log = Log()
if not log.open_log_file():
    log.create_log_file(2024)

test_log_file.write("============================== Log Writing\n")
log.writelog("Testing Log")
log.writecomment("""
Good
Day
Sir
""")

test_log_file.write("============================== Restore Operations\n")
log.writelog("Offload Cat")
log.writelog("Onload Cat")
print(log.open_log_file())

test_log_file.write("============================== Unload/Load Search\n")

test_log_file.write("============================== Ship Balancing\n")


test_log_file.close()

# ================================================================================================================

test_log_file_path = "TestingLogs/"
test_log_file = open(test_log_file_path + "ShipTest0_1.txt", 'w')
test_log_file.write(
"""###############################################
Ship Testing 0.1 - Testing Unload/Load
- ShipTests.txt
1. Unload Cat
2. Load Elephant
3. Unload Cat, Load Elephant
4. Stress Test: Unload Cat and Dog, Load Elephant and Bird x2
###############################################
"""
)
manifest = "ShipCase/ShipCase1.txt"
op_filename = "data/action_list.csv"

# ---------------------------------------------------------------------------------------
test_log_file.write("============================== 1. Unload Cat\n")
with open(op_filename, mode = 'w', newline='') as csvfile:
    file_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    file_writer.writerow(['name','qty','type','coords','weight'])
    file_writer.writerow(['Cat',1,'Unload','7_1',99])
    
ship = util.create_ship(manifest, op_filename)
test_log_file.write(f"--------- Initial Ship\n")
test_log_file.write(f"{ship}")

test_log_file.write(f"--------- Unloads\n")
[test_log_file.write(f"{u.get_cntr_info()}\n") for u in ship.unloads]
test_log_file.write(f"--------- Loads\n")
[test_log_file.write(f"{l.get_cntr_info()}\n") for l in ship.loads]

sol_ship = search.uniform_cost_lu(ship)
test_log_file.write(f"--------- Container Moves Start End\n")
if sol_ship != None:
    for i, move in enumerate(sol_ship.moves):
        test_output = f"{move}"
        if (i % 2 == 0):
            test_output += " "
        else:
            test_output += "\n"
        test_log_file.write(test_output)

test_log_file.write(f"--------- Final Ship\n")
test_log_file.write(f"{sol_ship}")

# ---------------------------------------------------------------------------------------
test_log_file.write("============================== 2. Load Elephant\n")
with open(op_filename, mode = 'w', newline='') as csvfile:
    file_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    file_writer.writerow(['name','qty','type','coords','weight'])
    file_writer.writerow(['Elephant',1,'Load','N/A',250])
    
ship = util.create_ship(manifest, op_filename)
test_log_file.write(f"--------- Initial Ship\n")
test_log_file.write(f"{ship}")

test_log_file.write(f"--------- Unloads\n")
[test_log_file.write(f"{u.get_cntr_info()}\n") for u in ship.unloads]
test_log_file.write(f"--------- Loads\n")
[test_log_file.write(f"{l.get_cntr_info()}\n") for l in ship.loads]

sol_ship = search.uniform_cost_lu(ship)
test_log_file.write(f"--------- Container Moves Start End\n")
if sol_ship != None:
    for i, move in enumerate(sol_ship.moves):
        test_output = f"{move}"
        if (i % 2 == 0):
            test_output += " "
        else:
            test_output += "\n"
        test_log_file.write(test_output)

test_log_file.write(f"--------- Final Ship\n")
test_log_file.write(f"{sol_ship}")

# ---------------------------------------------------------------------------------------
test_log_file.write("============================== 3. Unload Cat, Load Elephant\n")
with open(op_filename, mode = 'w', newline='') as csvfile:
    file_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    file_writer.writerow(['name','qty','type','coords','weight'])
    file_writer.writerow(['Cat',1,'Unload','7_1',99])
    file_writer.writerow(['Elephant',1,'Load','N/A',250])
    
ship = util.create_ship(manifest, op_filename)
test_log_file.write(f"--------- Initial Ship\n")
test_log_file.write(f"{ship}")

test_log_file.write(f"--------- Unloads\n")
[test_log_file.write(f"{u.get_cntr_info()}\n") for u in ship.unloads]
test_log_file.write(f"--------- Loads\n")
[test_log_file.write(f"{l.get_cntr_info()}\n") for l in ship.loads]

sol_ship = search.uniform_cost_lu(ship)
test_log_file.write(f"--------- Container Moves Start End\n")
if sol_ship != None:
    for i, move in enumerate(sol_ship.moves):
        test_output = f"{move}"
        if (i % 2 == 0):
            test_output += " "
        else:
            test_output += "\n"
        test_log_file.write(test_output)
    
test_log_file.write(f"--------- Final Ship\n")
test_log_file.write(f"{sol_ship}")

# ---------------------------------------------------------------------------------------
test_log_file.write("============================== 4. Stress Test: Unload Cat and Dog, Load Elephant and Bird x2\n")
with open(op_filename, mode = 'a', newline='') as csvfile:
    file_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    file_writer.writerow(['Dog',1,'Unload','7_2',100])
    file_writer.writerow(['Bird',2,'Load','N/A',50])
    
ship = util.create_ship(manifest, op_filename)
test_log_file.write(f"--------- Initial Ship\n")
test_log_file.write(f"{ship}")

test_log_file.write(f"--------- Unloads\n")
[test_log_file.write(f"{u.get_cntr_info()}\n") for u in ship.unloads]
test_log_file.write(f"--------- Loads\n")
[test_log_file.write(f"{l.get_cntr_info()}\n") for l in ship.loads]

sol_ship = search.uniform_cost_lu(ship)
test_log_file.write(f"--------- Container Moves Start End\n")
if sol_ship != None:
    for i, move in enumerate(sol_ship.moves):
        test_output = f"{move}"
        if (i % 2 == 0):
            test_output += " "
        else:
            test_output += "\n"
        test_log_file.write(test_output)
    
test_log_file.write(f"--------- Final Ship\n")
test_log_file.write(f"{sol_ship}")

# ship = util.create_ship_balance(manifest, outbound)

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

# new_cntr_coords = ship.add_cntr(ship.remove_cntr(5), 3)

# Final Test: testing production level (Into Documents/data/...)

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