from log import Log
from datetime import datetime
from ship import Ship
import copy
import util
import search
import csv
import os
import shutil
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
- Manifest: emptyship.txt
- Test Log: AuxTest.txt
#######################################
"""
)
# ---------------------------------------------------------------------------------------
test_log_file.write("============================== Loading a Manifest to Build a Ship From Scratch by Adding Containers\n")
scratch_ship = util.create_ship(manifest)
test_log_file.write("--------- Empty Ship\n")
test_log_file.write(f"{scratch_ship}")


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

test_log_file.write("--------- Filled Ship\n")
test_log_file.write(f"{scratch_ship}")

# ---------------------------------------------------------------------------------------
test_log_file.write("============================== Remove 4 Containers From Col 4\n")
for i in range(0, 4):
    rm_cntr = scratch_ship.remove_cntr(4)
    test_log_file.write(f"Removed {rm_cntr}\n")

test_log_file.write(f"{scratch_ship}")
test_log_file.write(f"{scratch_ship.top_columns}")

# ---------------------------------------------------------------------------------------
test_log_file.write("============================== Unpack Container Actions\n")
loads, unloads = util.unpack_actions(scratch_ship, op_filename, scratch_ship.row, scratch_ship.col)
test_log_file.write("--------- Unloads\n")
[test_log_file.write(u.get_cntr_info() + "\n") for u in unloads]
test_log_file.write("--------- Loads\n")
[test_log_file.write(l.get_cntr_info() + "\n") for l in loads]

# ---------------------------------------------------------------------------------------
test_log_file.write("============================== Find Best Containers for Unpacked Actions\n")
test_log_file.write("--------- Old Containers\n")
[test_log_file.write(cntr.get_cntr_info() + "\n") for cntr in unloads]
unload_cntrs = [scratch_ship.find_best_cntr(cntr) for cntr in unloads]
test_log_file.write("--------- Best Containers\n")
[test_log_file.write(cntr.get_cntr_info() + "\n") for cntr in unload_cntrs]

# ---------------------------------------------------------------------------------------
test_log_file.write("============================== Initializing Log File (Multi-Step)\n")
# shutil.rmtree("DockAutomate\\")
log = Log()
if not log.open_log_file():
    log.create_log_file(2023)

# ------------------------------------------------------
test_log_file.write("==================== Step 1/3: Directory Missing, Create It\n")
num_passed = 0
if log.debug_flags[0]:
    test_log_file.write("- Missing Directory Detected\n")
    num_passed += 1
if os.path.exists(os.getcwd() + f"\DockAutomate"):
    test_log_file.write("- Directory Successfully Created\n")
    num_passed += 1
test_log_file.write(f"------ Passed {num_passed}/2\n")

# ------------------------------------------------------
test_log_file.write("==================== Step 2/3: Log Config Missing, Create It\n")
num_passed = 0
if log.debug_flags[1]:
    test_log_file.write("- Missing Log Config Detected\n")
    num_passed += 1
if os.path.exists(os.getcwd() + f"\DockAutomate\.log_config.json"):
    test_log_file.write("- Log Config Successfully Created\n")
    num_passed += 1
test_log_file.write(f"------ Passed {num_passed}/2\n")

# ------------------------------------------------------
test_log_file.write("==================== Step 3/3: Log File Missing, Create It\n")
num_passed = 0
if log.debug_flags[2]:
    test_log_file.write("- Missing Log File Detected\n")
    num_passed += 1
if os.path.exists(os.getcwd() + f"\DockAutomate\\activitylog2023.txt"):
    test_log_file.write("- Log File Successfully Created\n")
    num_passed += 1
test_log_file.write(f"------ Passed {num_passed}/2\n")

# ---------------------------------------------------------------------------------------
test_log_file.write("============================== Log Writing (Multi-Step)\n")
# ------------------------------------------------------
test_log_file.write("==================== Step 1/2: Write Actions To Log\n")
num_passed = 0
for i in range(0, 3):
    if log.writelog(f"Container {i} Offloaded"):
        test_log_file.write("Written Successfully, Check \DockAutomate\\activitylog2023.txt for Validity\n")
        num_passed += 1
test_log_file.write(f"------ Passed {num_passed}/3\n")

# ------------------------------------------------------
test_log_file.write("==================== Step 2/2: Write Comments To Log\n")
num_passed = 0
for i in range(0, 3):
    if log.writecomment(f"Container {i} is Broken"):
        test_log_file.write("Written Successfully, Check \DockAutomate\\activitylog2023.txt for Validity\n")
        num_passed += 1
test_log_file.write(f"------ Passed {num_passed}/3\n")

# ---------------------------------------------------------------------------------------
test_log_file.write("============================== Balance Empty Ship\n")
scratch_ship = util.create_ship(manifest)
test_log_file.write(f"--------- Initial Ship\n")
test_log_file.write(f"{scratch_ship}")
sol_scratch_ship = search.uniform_cost_balance(scratch_ship, "cntr-cross")

test_log_file.write(f"--------- Container Moves Start End\n")
if sol_scratch_ship != None:
    for i, move in enumerate(sol_scratch_ship.moves):
        test_output = f"{move}"
        if (i % 2 == 0):
            test_output += " "
        else:
            test_output += "\n"
        test_log_file.write(test_output)

test_log_file.write(f"--------- Final Ship\n")
if sol_scratch_ship is None:
    test_log_file.write("Unable to Balance\n")
else:
    test_log_file.write(f"{sol_scratch_ship}")

# ================================================================================================================
test_log_file_path = "TestingLogs/"
test_log_file = open(test_log_file_path + "ShipTest0_1.txt", 'w')
test_log_file.write(
"""###############################################
Ship Testing 0.1 - Testing Unload/Load
- Manifest: ShipCase1.txt
- Test Log: ShipTest0_1.txt
1. Unload Cat
2. Load Elephant
3. Unload Cat, Load Elephant
4. Stress Test: Unload Cat and Dog, Load Elephant
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
    
ship0_1_0 = util.create_ship(manifest, op_filename)
test_log_file.write(f"--------- Initial Ship\n")
test_log_file.write(f"{ship0_1_0}")

test_log_file.write(f"--------- Unloads\n")
[test_log_file.write(f"{u.get_cntr_info()}\n") for u in ship0_1_0.unloads]
test_log_file.write(f"--------- Loads\n")
[test_log_file.write(f"{l.get_cntr_info()}\n") for l in ship0_1_0.loads]

sol_ship0_1_0 = search.uniform_cost_lu(ship0_1_0, "cntr-lu")
test_log_file.write(f"--------- Container Moves Start End\n")
if sol_ship0_1_0 != None:
    for i, move in enumerate(sol_ship0_1_0.moves):
        test_output = f"{move}"
        if (i % 2 == 0):
            test_output += " "
        else:
            test_output += "\n"
        test_log_file.write(test_output)

test_log_file.write(f"--------- Final Ship\n")
test_log_file.write(f"{sol_ship0_1_0}")

# ---------------------------------------------------------------------------------------
test_log_file.write("============================== 2. Load Elephant\n")
with open(op_filename, mode = 'w', newline='') as csvfile:
    file_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    file_writer.writerow(['name','qty','type','coords','weight'])
    file_writer.writerow(['Elephant',1,'Load','N/A',250])
    
ship0_1_1 = util.create_ship(manifest, op_filename)
test_log_file.write(f"--------- Initial Ship\n")
test_log_file.write(f"{ship0_1_1}")

test_log_file.write(f"--------- Unloads\n")
[test_log_file.write(f"{u.get_cntr_info()}\n") for u in ship0_1_1.unloads]
test_log_file.write(f"--------- Loads\n")
[test_log_file.write(f"{l.get_cntr_info()}\n") for l in ship0_1_1.loads]

sol_ship0_1_1 = search.uniform_cost_lu(ship0_1_1, "cntr-lu")
test_log_file.write(f"--------- Container Moves Start End\n")
if sol_ship0_1_1 != None:
    for i, move in enumerate(sol_ship0_1_1.moves):
        test_output = f"{move}"
        if (i % 2 == 0):
            test_output += " "
        else:
            test_output += "\n"
        test_log_file.write(test_output)

test_log_file.write(f"--------- Final Ship\n")
test_log_file.write(f"{sol_ship0_1_1}")

# ---------------------------------------------------------------------------------------
test_log_file.write("============================== 3. Unload Cat, Load Elephant\n")
with open(op_filename, mode = 'w', newline='') as csvfile:
    file_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    file_writer.writerow(['name','qty','type','coords','weight'])
    file_writer.writerow(['Cat',1,'Unload','7_1',99])
    file_writer.writerow(['Elephant',1,'Load','N/A',250])
    
ship0_1_2 = util.create_ship(manifest, op_filename)
test_log_file.write(f"--------- Initial Ship\n")
test_log_file.write(f"{ship0_1_2}")

test_log_file.write(f"--------- Unloads\n")
[test_log_file.write(f"{u.get_cntr_info()}\n") for u in ship0_1_2.unloads]
test_log_file.write(f"--------- Loads\n")
[test_log_file.write(f"{l.get_cntr_info()}\n") for l in ship0_1_2.loads]

sol_ship0_1_2 = search.uniform_cost_lu(ship0_1_2, "cntr-lu")
test_log_file.write(f"--------- Container Moves Start End\n")
if sol_ship0_1_2 != None:
    for i, move in enumerate(sol_ship0_1_2.moves):
        test_output = f"{move}"
        if (i % 2 == 0):
            test_output += " "
        else:
            test_output += "\n"
        test_log_file.write(test_output)
    
test_log_file.write(f"--------- Final Ship\n")
test_log_file.write(f"{sol_ship0_1_2}")

# ---------------------------------------------------------------------------------------
test_log_file.write("============================== 4. Stress Test: Unload Cat and Dog, Load Elephant and Bird x2\n")
with open(op_filename, mode = 'a', newline='') as csvfile:
    file_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    file_writer.writerow(['Dog',1,'Unload','7_2',100])
    file_writer.writerow(['Bird',2,'Load','N/A',50])
    
ship0_1_3 = util.create_ship(manifest, op_filename)
test_log_file.write(f"--------- Initial Ship\n")
test_log_file.write(f"{ship0_1_3}")

test_log_file.write(f"--------- Unloads\n")
[test_log_file.write(f"{u.get_cntr_info()}\n") for u in ship0_1_3.unloads]
test_log_file.write(f"--------- Loads\n")
[test_log_file.write(f"{l.get_cntr_info()}\n") for l in ship0_1_3.loads]

sol_ship0_1_3 = search.uniform_cost_lu(ship0_1_3, "cntr-lu")
test_log_file.write(f"--------- Container Moves Start End\n")
if sol_ship0_1_3 != None:
    for i, move in enumerate(sol_ship0_1_3.moves):
        test_output = f"{move}"
        if (i % 2 == 0):
            test_output += " "
        else:
            test_output += "\n"
        test_log_file.write(test_output)
    
test_log_file.write(f"--------- Final Ship\n")
test_log_file.write(f"{sol_ship0_1_3}")

# ================================================================================================================
test_log_file = open(test_log_file_path + "ShipTest0_2.txt", 'w')
test_log_file.write(
"""###############################################
Ship Testing 0.2 - Testing Balancing
- Manifest: ShipTest1.txt
- Test Log: ShipTest0_2.txt
1. Balance Original
2. Balance Removing Cat From Original
3. Balance Adding Elephant From Original
###############################################
"""
)
ship0_2_0 = util.create_ship(manifest)

# ---------------------------------------------------------------------------------------
test_log_file.write("============================== 1. Balance Original\n")
test_log_file.write(f"--------- Initial Ship\n")
test_log_file.write(f"{ship0_2_0}")
sol_ship0_2_0 = search.uniform_cost_balance(ship0_2_0, "cntr-cross")

test_log_file.write(f"--------- Container Moves Start End\n")
if sol_ship0_2_0 != None:
    for i, move in enumerate(sol_ship0_2_0.moves):
        test_output = f"{move}"
        if (i % 2 == 0):
            test_output += " "
        else:
            test_output += "\n"
        test_log_file.write(test_output)

test_log_file.write(f"--------- Final Ship\n")
if sol_ship0_2_0 is None:
    test_log_file.write("Unable to Balance\n")
else:
    test_log_file.write(f"{sol_ship0_2_0}")

# ---------------------------------------------------------------------------------------
test_log_file.write("============================== 2. Balance Removing Cat From Original\n")
test_log_file.write(f"--------- Initial Ship\n")
test_log_file.write(f"{sol_ship0_1_0}")
sol_ship0_2_1 = search.uniform_cost_balance(sol_ship0_1_0, "cntr-cross")

test_log_file.write(f"--------- Container Moves Start End\n")
if sol_ship0_2_1 != None:
    for i, move in enumerate(sol_ship0_2_1.moves):
        test_output = f"{move}"
        if (i % 2 == 0):
            test_output += " "
        else:
            test_output += "\n"
        test_log_file.write(test_output)

test_log_file.write(f"--------- Final Ship\n")
if sol_ship0_2_1 is None:
    test_log_file.write("Unable to Balance\n")
else:
    test_log_file.write(f"{sol_ship0_2_1}")

# ---------------------------------------------------------------------------------------
test_log_file.write("============================== 3. Balance Adding Elephant From Original\n")
test_log_file.write(f"--------- Initial Ship\n")
test_log_file.write(f"{sol_ship0_1_1}")
sol_ship0_2_2 = search.uniform_cost_balance(sol_ship0_1_1, "cntr-cross")

test_log_file.write(f"--------- Container Moves Start End\n")
if sol_ship0_2_2 != None:
    for i, move in enumerate(sol_ship0_2_2.moves):
        test_output = f"{move}"
        if (i % 2 == 0):
            test_output += " "
        else:
            test_output += "\n"
        test_log_file.write(test_output)

test_log_file.write(f"--------- Final Ship\n")
if sol_ship0_2_2 is None:
    test_log_file.write("Unable to Balance\n")
else:
    test_log_file.write(f"{sol_ship0_2_2}")

# ================================================================================================================
test_log_file = open(test_log_file_path + "ShipTest1.txt", 'w')
test_log_file.write(
"""###############################################
Ship Testing 1
- ShipCase1.txt
1. Balance Original
2. Unload Cat From Original
3. Balance Resulting Ship
###############################################
"""
)
manifest = "ShipCase/ShipCase1.txt"
op_filename = "data/action_list.csv"
with open(op_filename, mode = 'w', newline='') as csvfile:
    file_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    file_writer.writerow(['name','qty','type','coords','weight'])
    file_writer.writerow(['Cat',1,'Unload','7_1',99])
ship1 = util.create_ship(manifest, op_filename)

# ---------------------------------------------------------------------------------------
test_log_file.write("============================== 1. Balance Original\n")
test_log_file.write(f"--------- Initial Ship\n")
test_log_file.write(f"{ship1}")
sol_ship1 = search.uniform_cost_balance(ship1, "cntr-cross")

test_log_file.write(f"--------- Container Moves Start End\n")
if sol_ship1 != None:
    for i, move in enumerate(sol_ship1.moves):
        test_output = f"{move}"
        if (i % 2 == 0):
            test_output += " "
        else:
            test_output += "\n"
        test_log_file.write(test_output)

test_log_file.write(f"--------- Final Ship\n")
if sol_ship1 is None:
    test_log_file.write("Unable to Balance\n")
else:
    test_log_file.write(f"{sol_ship1}")

# ---------------------------------------------------------------------------------------
test_log_file.write("============================== 2. Unload Cat From Original\n")
test_log_file.write(f"--------- Initial Ship\n")
test_log_file.write(f"{ship1}")

sol_ship1 = search.uniform_cost_lu(ship1, "cntr-lu")
test_log_file.write(f"--------- Container Moves Start End\n")
if sol_ship1 != None:
    for i, move in enumerate(sol_ship1.moves):
        test_output = f"{move}"
        if (i % 2 == 0):
            test_output += " "
        else:
            test_output += "\n"
        test_log_file.write(test_output)

test_log_file.write(f"--------- Final Ship\n")
test_log_file.write(f"{sol_ship1}")

# ---------------------------------------------------------------------------------------
test_log_file.write("============================== 3. Balance Resulting Ship\n")
test_log_file.write(f"--------- Initial Ship\n")
test_log_file.write(f"{sol_ship1}")
sol_ship1 = search.uniform_cost_balance(sol_ship1, "cntr-cross")

test_log_file.write(f"--------- Container Moves Start End\n")
if sol_ship1 != None:
    for i, move in enumerate(sol_ship1.moves):
        test_output = f"{move}"
        if (i % 2 == 0):
            test_output += " "
        else:
            test_output += "\n"
        test_log_file.write(test_output)

test_log_file.write(f"--------- Final Ship\n")
if sol_ship1 is None:
    test_log_file.write("Unable to Balance\n")
else:
    test_log_file.write(f"{sol_ship1}")


# ================================================================================================================
test_log_file = open(test_log_file_path + "ShipTest2.txt", 'w')
test_log_file.write(
"""###############################################
Ship Testing 2
- ShipCase2.txt
1. Balance Original
2. Load Bat Onto Original
3. Balance Resulting Ship
###############################################
"""
)   # TODO: 2, 3
manifest = "ShipCase/ShipCase2.txt"
op_filename = "data/action_list.csv"
with open(op_filename, mode = 'w', newline='') as csvfile:
    file_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    file_writer.writerow(['name','qty','type','coords','weight'])
    file_writer.writerow(['Bat',1,'Load',"N/A",5432])
ship2 = util.create_ship(manifest, op_filename)

# ---------------------------------------------------------------------------------------
test_log_file.write("============================== 1. Balance Original\n")
test_log_file.write(f"--------- Initial Ship\n")
test_log_file.write(f"{ship2}")
sol_ship2 = search.uniform_cost_balance(ship2, "cntr-cross")

test_log_file.write(f"--------- Container Moves Start End\n")
if sol_ship2 != None:
    for i, move in enumerate(sol_ship2.moves):
        test_output = f"{move}"
        if (i % 2 == 0):
            test_output += " "
        else:
            test_output += "\n"
        test_log_file.write(test_output)

test_log_file.write(f"--------- Final Ship\n")
test_log_file.write(f"{sol_ship2}")

# ---------------------------------------------------------------------------------------
test_log_file.write("============================== 2. Load Bat Onto Original\n")
test_log_file.write(f"--------- Initial Ship\n")
test_log_file.write(f"{ship2}")

sol_ship2 = search.uniform_cost_lu(ship2, "cntr-lu")
test_log_file.write(f"--------- Container Moves Start End\n")
if sol_ship2 != None:
    for i, move in enumerate(sol_ship2.moves):
        test_output = f"{move}"
        if (i % 2 == 0):
            test_output += " "
        else:
            test_output += "\n"
        test_log_file.write(test_output)

test_log_file.write(f"--------- Final Ship\n")
test_log_file.write(f"{sol_ship2}")

# ---------------------------------------------------------------------------------------
test_log_file.write("============================== 3. Balance Resulting Ship\n")
test_log_file.write(f"--------- Initial Ship\n")
test_log_file.write(f"{sol_ship2}")
sol_ship2 = search.uniform_cost_balance(sol_ship2, "cntr-cross")

test_log_file.write(f"--------- Container Moves Start End\n")
if sol_ship2 != None:
    for i, move in enumerate(sol_ship2.moves):
        test_output = f"{move}"
        if (i % 2 == 0):
            test_output += " "
        else:
            test_output += "\n"
        test_log_file.write(test_output)

test_log_file.write(f"--------- Final Ship\n")
if sol_ship2 is None:
    test_log_file.write("Unable to Balance\n")
else:
    test_log_file.write(f"{sol_ship2}")