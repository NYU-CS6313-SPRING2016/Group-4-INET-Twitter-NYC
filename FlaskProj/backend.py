# -*- coding: utf-8 -*-
from flask import Flask, jsonify, render_template, request
import get_data
# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

import get_data

app = Flask(__name__)
        
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/data')
def data():
	get_data.get_data()
	

if __name__ == '__main__':
    app.run()
