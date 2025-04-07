from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from queries import loop_filter_ingredients, print_view
import json
import os
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"


if __name__ == '__main__':
	app.run(debug = True)