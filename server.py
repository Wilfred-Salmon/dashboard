from flask import Flask, render_template, request, redirect, url_for, jsonify
from src.Line import Line

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect(url_for('different_page', name = request.form.get("some stuff")))
    
    return render_template('index.html')

@app.route('/test/')
@app.route('/test/<string:name>')
def different_page(name = None):
    return render_template('test_name.html', name=name)

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
    return jsonify([
        {"display_name":"Victoria" , "id": "victoria"},
        {"display_name":"District" , "id": "district"},
        {"display_name":"Circle" , "id": "circle"},
        {"display_name":"Hammersmith & City" , "id": "hammersmith-city"},
        {"display_name":"Piccadilly" , "id": "piccadilly"},
        {"display_name":"Metropolitan" , "id": "metropolitan"}
    ])

@app.route('/line_statuses')
def line_statuses():
    return(render_template('line_status/line_statuses.html'))

if __name__ == '__main__':
    app.run(port=8000, debug=True)