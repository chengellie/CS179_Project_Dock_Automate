from flask import Blueprint, render_template, json, request, redirect
import csv
from ship import Ship
from util import *
from search import *
import os
import sys
import copy


home_page = Blueprint("home_page", __name__)
selection_1 = Blueprint("selection_1", __name__)
tables = Blueprint("tables", __name__)
unloading = Blueprint("unloading", __name__)
loading = Blueprint("loading", __name__)
notes = Blueprint('notes',__name__)

current_user = ''
current_ship = ''
moves = []
ship = ''
item = ''

def refresh_ship():
    global ship
    global item
    ship = create_ship(
        "ShipCase/ShipCase2.txt",
    )
    item = copy.deepcopy(ship.ship_state)

def to_html_elememts(moves):
    for j in range(len(moves)):
            first = True
            for i, ls in enumerate(moves[j]):
                if first and ls[0] < 0:
                    moves[j][i] = "add"
                elif ls[0] < 0:
                    moves[j][i] = "remove"
                else:
                    moves[j][i] = "#ship_" + str(ls[0]) + "_" + str(ls[1])
                first = False

def build_moves(path):
    global moves
    i=0
    while i < len(path):
        start = path[i]
        print(start)
        end = path[i+1]
        print(end)
        moves.append(ship.get_moves(start,end))
        ship.add_cntr(ship.remove_cntr(start[1]), end[1])
        i+=2
        
    

@home_page.route("/", methods = ['GET','POST'])
def home():
    global ship
    global item
    refresh_ship()
    csvfile = open("data/action_list.csv", "w")
    csvfile.truncate()
    csvfile.close()
    with open('data/action_list.csv', mode = 'a', newline='') as csvfile:
            file_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            file_writer.writerow(['name','qty','type','coords','weight'])

    global current_user
    if request.method == 'POST':
        global current_user
        current_user = request.form.get('current_user')
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
            moves.append([[0, 4], [0, 5], [0, 6], [1, 6], [2, 6], [1, 6], [0, 6], [-10, 6]])
            moves.append(ship.get_moves([1, 4], [6, 6]))
            print("load/unload selected")

        elif request.form['submit_button'] == 'balance':
            # moves.append(ship.get_moves([0, 4], [6, 6]))
            # moves = [[[0, 4], [0, 5], [0, 6], [1, 6], [2, 6], [1, 6], [0, 6], [-10, 6]]]
            # moves.append(ship.get_moves([1, 4], [5, 6]))
            solution = uniform_cost_balance(ship,"cntr-cross")
            path = solution.moves
            print(path)
            build_moves(path)

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
    print(moves)
    return render_template(
        "table.html",
        item=item,
        color=color,
        row=row,
        col=col,
        moves=moves,
        user = current_user,
    )

@notes.route("/" , methods = ['GET','POST'])
def note():
    global current_user
    if request.method == 'POST':
        user_note = request.form.get('user_note')
        print(user_note)
    return render_template("notes.html",user = current_user)
