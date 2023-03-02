from flask import Blueprint, render_template, json, request, redirect
import csv
from ship import Ship
from shiputil import *
import os
import sys


home_page = Blueprint("home_page", __name__)
selection_1 = Blueprint("selection_1", __name__)
tables = Blueprint("tables", __name__)
unloading = Blueprint("unloading", __name__)

current_user = ''
current_ship = ''

def create_ship(manifest_filename, op_filename):
    """Input filename of manifest, parses file contents. Returns ship object."""
    # https://www.pythontutorial.net/python-basics/python-read-text-file/
    with open(manifest_filename) as f:
        manifest_cntnt = [line for line in f.readlines()]
    with open(op_filename) as f:
        loads = f.readline().strip().split(",")
        unloads = f.readline().strip().split(",")
    ret = Ship(manifest_cntnt, loads, unloads)
    return ret


@home_page.route("/", methods = ['GET','POST'])
def home():
    if request.method == 'POST':
        global current_user
        current_user = request.form.get('current_user')
        return redirect('/home-selection')
    return render_template("home.html")

@selection_1.route("/", methods = ['GET','POST'])
def selection1():
    global current_user
    csvfile = open('data/action_list.csv')
    data = list(csv.reader(csvfile,delimiter=","))
    row = len(data)
    return render_template("selection1.html", data = data, row = row, user = current_user)

@unloading.route("/", methods = ['GET','POST'])
def unload():
    global current_user
    ship = create_ship("ShipCase/ShipCase1.txt", "load_unload.txt")
    item = ship.ship_state
    if request.method == 'POST':
        unload = request.form.getlist('unload')
        with open('data/action_list.csv', mode = 'a') as csvfile:
            file_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for i in unload:
                file_writer.writerow([i,1,'Unload'])

    csvfile = open('data/action_list.csv')
    data = list(csv.reader(csvfile,delimiter=","))
    row = len(data)

    return render_template("unload.html", content = item, data = data, row = row, user = current_user)

@tables.route("/")
def table():
    global current_user
    ship = create_ship("ShipCase/ShipCase1.txt", "load_unload.txt")
    item = ship.ship_state
    row = len(item)
    col = len(item[0])
    color = ["rgb(44, 174, 214)", "red"]
    at = ["ship_7_1", "ship_6_1"]
    go = ["ship_6_1", "ship_5_1"]
    moves = get_moves(ship, [7, 1], [7, 4])
    for i, ls in enumerate(moves):
        moves[i] = "#ship_" + str(moves[i][0]) + "_" + str(moves[i][1])
    print(moves)
    # moves = ["ship_7_1", "ship_6_1", "ship_5_1"]
    return render_template(
        "table.html",
        item=item,
        color=color,
        row=row,
        col=col,
        at=at,
        go=go,
        moves=moves,
        user = current_user,
    )
