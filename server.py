from flask import Flask, render_template, request, redirect, url_for, jsonify
from csv import DictReader
from typing import List, Dict
from src.Line import Line

app = Flask(__name__)

@app.route('/line_status/<string:line_name>')
def line_status_display(line_name: str):
    display_name = request.args.get('display_name', line_name)

    line: Line = Line(line_name, display_name)
    try:
        line.cache_status()
    except Exception:
        return render_template('line_status/line_not_found.html', line_name = line_name), 404
    
    return render_template('line_status/line_status.html', line = line)

@app.route('/lines')
def get_lines():
    return jsonify(get_lines_list())

@app.route('/line_statuses')
def line_statuses():
    lines = get_lines_list()
    return(render_template('line_status/line_statuses.html', lines = lines))

def get_lines_list() -> List[Dict[str, str]]:
    with open('data/lines.csv', 'r') as csvfile:
        reader = DictReader(csvfile, delimiter=',')
        return list(reader)

if __name__ == '__main__':
    app.run(port = 8000, debug = True)