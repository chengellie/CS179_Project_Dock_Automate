from flask import Blueprint, render_template

home_page = Blueprint('home_page', __name__)
tables = Blueprint('tables', __name__)


@home_page.route('/')
def home():
    return render_template('home.html')

@tables.route('/')
def table():
    return render_template('table.html')