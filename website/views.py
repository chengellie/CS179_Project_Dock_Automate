from flask import Blueprint, render_template, json
from ship import Ship

home_page = Blueprint('home_page', __name__)
tables = Blueprint('tables', __name__)

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

@home_page.route('/')
def home():
    return render_template('home.html')

@tables.route('/')
def table():
    ship = create_ship("ShipCase1.txt", "load_unload.txt")
    item = ship.ship_state
    row = len(item)
    col = len(item[0])
    color = ['rgb(44, 174, 214)','red']
    at = ['ship_7_1','ship_6_1']
    go = ['ship_6_1','ship_5_1']
    return render_template('table.html',item = item, color = color, row = row, col = col, at = at, go = go)