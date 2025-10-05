from flask import Flask, render_template, request, redirect, url_for, jsonify
from pandas import read_csv
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
    return jsonify(read_csv('data/lines.csv', sep = ", ").to_dict(orient='records'))

@app.route('/line_statuses')
def line_statuses():
    return(render_template('line_status/line_statuses.html'))

if __name__ == '__main__':
    app.run(port=8000, debug=True)