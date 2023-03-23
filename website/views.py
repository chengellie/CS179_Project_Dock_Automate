from flask import Blueprint, render_template, json, request, redirect
import csv
from ship import Ship
from util import *
import os
import sys


home_page = Blueprint("home_page", __name__)
selection_1 = Blueprint("selection_1", __name__)
tables = Blueprint("tables", __name__)
unloading = Blueprint("unloading", __name__)
loading = Blueprint("loading", __name__)
notes = Blueprint('notes',__name__)

current_user = ''
current_ship = ''


# def create_ship(manifest_filename, op_filename):
#     """Input filename of manifest, parses file contents. Returns ship object."""
#     # https://www.pythontutorial.net/python-basics/python-read-text-file/
#     with open(manifest_filename) as f:
#         manifest_cntnt = [line for line in f.readlines()]
#     with open(op_filename) as f:
#         loads = f.readline().strip().split(",")
#         unloads = f.readline().strip().split(",")
#     ret = create_ship(
#         "ShipCase/ShipCase4.txt",
#         "load_unload.txt",
#         "OUTBOUNDShipCase/OUTBOUNDshipcasetest.txt",
#     )
#     return ret

@home_page.route("/", methods = ['GET','POST'])
def home():
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
    global current_user
    csvfile = open('data/action_list.csv')
    data = list(csv.reader(csvfile,delimiter=","))
    data.pop(0)
    row = len(data)
    return render_template("selection1.html", data = data, row = row, user = current_user)

@unloading.route("/", methods = ['GET','POST'])
def unload():
    global current_user
    ship = create_ship(
        "ShipCase/ShipCase4.txt",
        "load_unload.txt",
        "OUTBOUNDShipCase/OUTBOUNDshipcasetest.txt",
    )
    item = ship.ship_state
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
    ship = create_ship(
        "ShipCase/ShipCase4.txt",
        "load_unload.txt",
        "OUTBOUNDShipCase/OUTBOUNDshipcasetest.txt",
    )
    item = ship.ship_state
    row = len(item)
    col = len(item[0])
    color = ["rgb(44, 174, 214)", "red"]
    moves = []
    moves.append(ship.get_moves([0, 4], [6, 6]))
    moves.append(ship.get_moves([1, 4], [5, 6]))
    for j in range(len(moves)):
        for i, ls in enumerate(moves[j]):
            moves[j][i] = "#ship_" + str(ls[0]) + "_" + str(ls[1])
    # moves = ["ship_7_1", "ship_6_1", "ship_5_1"]
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
    if request.method == 'POST':
        user_note = request.form.get('user_note')
        print(user_note)
    return render_template("notes.html")
