from flask import Flask, render_template, request, jsonify
from src.Line import Line, get_lines_list

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def dashboard():
    return render_template('index.html')

@app.route('/placeholder')
def placeholder():
    return render_template('placeholder.html')

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

if __name__ == '__main__':
    app.run(port = 8000, debug = True)