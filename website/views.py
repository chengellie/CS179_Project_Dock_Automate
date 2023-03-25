from flask import Blueprint, render_template, json, request, redirect
import csv
from ship import Ship
from util import *
from search import *
from container import Container
from log import Log
import os
import sys
import copy


home_page = Blueprint("home_page", __name__)
selection_1 = Blueprint("selection_1", __name__)
tables = Blueprint("tables", __name__)
unloading = Blueprint("unloading", __name__)
loading = Blueprint("loading", __name__)
notes = Blueprint('notes',__name__)
log = Blueprint('log',__name__)

log = Log()
log_opened = False
manifest = ""

current_user = ''
current_ship = ''
moves = []
ship = ''
item = ''

def refresh_ship():
    global ship
    global item
    global log
    filepath = os.getcwd() + f"/DockAutomate/manifest"   # Testing  Windows
    # self.filepath = os.path.expanduser(f"~\Documents\.DockAutomate") # Windows
    for x in os.listdir(filepath):
        print(x)
        if x.endswith(".txt"):
            manifest = filepath + f"/{x}"
            break
    ship = create_ship(
        manifest,
        "data/action_list.csv"
    )
    log.writelog(f"Manifest {manifest} is opened. There are containers on the ship.")
    item = copy.deepcopy(ship.ship_state)

def to_html_elememts(moves):
    global log
    global ship
    global manifest
    load_list = [i.name for i in ship.loads]
    try:
        for j in range(len(moves)):
                first = True
                for i, ls in enumerate(moves[j]):
                    if first and ls[0] < 0:
                        moves[j][i] = "add"
                        cntr_name = load_list.pop(0)
                        log.writelog(f"\"{cntr_name}\" is onloaded.")
                    elif ls[0] < 0:
                        moves[j][i] = "remove"
                        log.writelog(f"\"{ship.ship_state[j][i]}\" is offloaded.")
                    else:
                        moves[j][i] = "#ship_" + str(ls[0]) + "_" + str(ls[1])
                    first = False
        log.writelog(f"Finished a cycle. Manifest {manifest} was written to desktop")
    except:
        return
    
def build_moves(path):
    global moves
    i=0
    while i < len(path):
        start = path[i]
        end = path[i+1]
        if start[0] < 0:
            start[1] = end[1]
            # temp_container = Container()
            # ship.add_cntr('TEMP', end[1])
        elif end[0] < 0:
            end[1] = start[1]
            ship.remove_cntr(start[1])
        else:
            ship.add_cntr(ship.remove_cntr(start[1]), end[1])
        moves.append(ship.get_moves(start,end))
        i+=2
        
# def lu_moves(path):
#     global moves
#     i = 0
#     while i < len(path):
#         start = path[i]
#         end = path[i+1]
        

@home_page.route("/", methods = ['GET','POST'])
def home():
    global ship
    global item
    global current_user
    global log
    global log_opened

    if not log_opened:
        log_status = log.open_log_file()
        if log_status == 0:
            # Tell user there is no valid log file, and you will be creating one
            # Ask user to input a year
            # year = input()
            return redirect('/log')
            log.create_log_file(2023)
            log_opened = True
            
        elif log_status == 1:   # Everything is good
            print("File Opened")
            # It asks me “Do you want to start a new log file?” 
                # If YES, it asks me “The log file has the logical year appended to its name, What year do you want the log file”
            log_opened = True

    if current_user != '':
        # user logged out
        pass

    refresh_ship()
    csvfile = open("data/action_list.csv", "w")
    csvfile.truncate()
    csvfile.close()
    with open('data/action_list.csv', mode = 'a', newline='') as csvfile:
            file_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            file_writer.writerow(['name','qty','type','coords','weight'])

    if request.method == 'POST':
        current_user = request.form.get('current_user')
        # user logged in
        return redirect('/home-selection')
    return render_template("home.html",user = current_user)

@selection_1.route("/", methods = ['GET','POST'])
def selection1():
    global moves
    global ship
    global item
    refresh_ship()
    moves = []
    if request.method == 'POST':
        if request.form['submit_button'] == 'load_unload':
            solution = uniform_cost_lu(ship)
            path = solution.moves
            # path = solution.moves
            build_moves(path)
            # moves.append(ship.get_moves([1, 4], [6, 6]))
            print("load/unload selected")

        elif request.form['submit_button'] == 'balance':
            solution = uniform_cost_balance(ship,"cntr-cross")
            try:
                path = solution.moves
                build_moves(path)
            except:
                moves = ["SIFT"]

            print("balance selected")
        
        to_html_elememts(moves)
        return redirect('/table')

    global current_user
    csvfile = open('data/action_list.csv')
    data = list(csv.reader(csvfile,delimiter=","))
    data.pop(0)
    row = len(data)
    return render_template("selection1.html", data = data, row = row, user = current_user)

@unloading.route("/", methods = ['GET','POST'])
def unload():
    global current_user
    global ship
    global item
    if request.method == 'POST':
        unload = request.form.getlist('unload')
        with open('data/action_list.csv', mode = 'a',newline='') as csvfile:
            file_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for i in unload:
                name,position = i.split('__')
                file_writer.writerow([name,1,'Unload',position,"N/A"])

    csvfile = open('data/action_list.csv')
    data = list(csv.reader(csvfile,delimiter=","))
    data.pop(0)
    row = len(data)

    return render_template("unload.html", content = item, data = data, row = row, user = current_user)

@loading.route("/", methods = ['GET','POST'])
def load():
    global current_user
    global ship
    if request.method == 'POST':
        load_name = request.form.get('item_name')
        load_weight = request.form.get('item_weight')
        load_count = request.form.get('item_count')
        with open('data/action_list.csv', mode = 'a', newline='') as csvfile:
            file_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            file_writer.writerow([load_name,load_count,'Load','N/A',load_weight])
            
    csvfile = open('data/action_list.csv')
    data = list(csv.reader(csvfile,delimiter=","))
    data.pop(0)
    row = len(data)

    return render_template('load.html', data = data, row = row, user = current_user)

@tables.route("/", methods = ['GET','POST'])
def table():
    global current_user
    global moves
    global ship
    global item
    refresh_ship()
    # item = ship.ship_state
    row = len(item)
    col = len(item[0])
    color = ["rgb(44, 174, 214)", "red"] 
    loads = [i.name for i in ship.loads]
    print(moves)
    return render_template(
        "table.html",
        item=item,
        color=color,
        row=row,
        col=col,
        moves=moves,
        loads = loads,
        user = current_user,
    )

@notes.route("/" , methods = ['GET','POST'])
def note():
    global current_user
    global log

    if request.method == 'POST':
        user_note = request.form.get('user_note')
        # user added note
        print(user_note)
        log.writecomment(user_note)
    return render_template("notes.html",user = current_user)

@log.route("/",methods = ['GET','POST'])
def build_log():
    global log
    if request.method == 'POST':
        log_year = request.form.get('log_year')

        print(log_year)
        return redirect('/')


    return render_template("log.html",user = current_user)